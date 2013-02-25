
from zope.component import adapter
from zope.component import getUtility

from zope.interface import implementer

from zope.schema.interfaces import IField

from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IFieldWidget

from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from openmultimedia.reporter.interfaces import IUpload


class UploadWidget(TextWidget):
    """Input type upload widget implementation."""
    input_template = ViewPageTemplateFile('upload_input.pt')
    display_template = ViewPageTemplateFile('upload_display.pt')

    klass = u'upload-widget'

    js_template_display = """\
    (function($) {
        $().ready(function() {
         $(".download-upload-widget").click(function() {
           var value = $(this).attr("file_value");
           $("#download_frame").attr("src", "%(upload_url)s" + value);
         });
        });
    })(jQuery);
    """

    def uploader_id(self):
        return self.id + "-uploader"

    def js_display(self):
        upload_utility = getUtility(IUpload)
        url = upload_utility.upload_url()
        return self.js_template_display % dict(upload_url=url)

    def render(self):
        if self.mode == DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def UploadFieldWidget(field, request):
    """IFieldWidget factory for UploadWidget."""
    return FieldWidget(field, UploadWidget(request))
