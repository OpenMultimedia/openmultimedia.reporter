
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

from openmultimedia.reporter import _


class UploadWidget(TextWidget):
    """Input type upload widget implementation."""
    input_template = ViewPageTemplateFile('upload_input.pt')
    display_template = ViewPageTemplateFile('upload_display.pt')

    klass = u'upload-widget'

    # JavaScript template
    js_template_input = """\
    (function($) {
        function endsWith(str, suffix) {
            return str.indexOf(suffix, str.length - suffix.length) !== -1;
        }

        $().ready(function() {
        $("#formfield-form-widgets-file_type").css("display", "none");
        $('#%(id)s').css('display','none');
         var uploader = new qq.FileUploader({
             element: $('#%(id_uploader)s')[0],
             action: '%(upload_url)s',
             debug: true,
             onComplete: function(id, filename, result) {
               if (result['status'] === "success") {
                 regex = "^[a-zA-Z0-9]+\.[a-zA-Z]{3}$";
                 var file_id = result['id'];
                 $('#%(id)s').val(file_id);
                 $('#%(id_uploader)s').css("display", "none");
                 $("#formfield-%(id)s .formHelp").text("%(upload_success)s: " + filename);
                 if(endsWith(filename,"jpg") || endsWith(filename,"gif") ||
                 endsWith(filename,"png") || endsWith(filename,"jpeg") ||
                 endsWith(filename,"JPG") || endsWith(filename,"GIF") ||
                  endsWith(filename,"PNG") || endsWith(filename,"JPEG")) {
                    $("#form-widgets-file_type").val("image");
                 } else { $("#form-widgets-file_type").val("video");}
               } else {
                $("#formfield-%(id)s .fieldErrorBox").text("%(upload_error)s");
               }
             }
         });
         
        if ($('#form-widgets-file_id').val() != ""){
            $("#formfield-%(id)s .formHelp").text("%(already_uploaded)s" );
        }

        });
    })(jQuery);
    """

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

    def js_input(self):
        upload_utility = getUtility(IUpload)
        url = upload_utility.upload_url()
        upload_error = _(u"Error uploading file, please try again or use a diferent file")
        upload_success = _(u"File uploaded correctly")
        already_uploaded = _(u"Your file was already uploaded, no need to do it again.")
        return self.js_template_input % dict(id=self.id,
                                             id_uploader=self.uploader_id(),
                                             upload_url=url,
                                             upload_error=upload_error,
                                             upload_success=upload_success,
                                             already_uploaded=already_uploaded)

    def js_display(self):
        upload_utility = getUtility(IUpload)
        url = upload_utility.upload_url()
        return self.js_template_display % dict(upload_url=url)

    def uploader_id(self):
        return self.id + "-uploader"

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
