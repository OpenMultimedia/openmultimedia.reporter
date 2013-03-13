# -*- coding: utf-8 -*-

import hashlib
import logging

from five import grok

from zope.component import getUtility

from zope.i18n import translate

from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from openmultimedia.reporter.config import PROJECTNAME
from openmultimedia.reporter.content.anonreport import IAnonReport
from openmultimedia.reporter.interfaces import IUpload

from openmultimedia.reporter import _

logger = logging.getLogger(PROJECTNAME)


class ProcessedResultView(grok.View):
    grok.context(Interface)
    grok.name("processed_result")
    grok.require('zope2.AccessContentsInformation')

    def render(self):

        key = self.request.get('key', None)

        if key:
            logger.info("Got: %s as key" % key)
            utility = getUtility(IUpload)
            security_key = utility.get_security_key()
            id = self.context.file_id

            m = hashlib.md5()

            m.update(security_key + id)
            digest = m.hexdigest()

            logger.info("Digest: %s " % digest)
            if digest == key:
                logger.info("They match. Valid request found.")
                msg_type = self.request.get('type', None)
                if msg_type == 'error':
                    logger.info("An error ocurred in the remote system when processing the media for %s." % self.context.absolute_url())
                    # Do nothing for now...
                elif msg_type == 'success':
                    logger.info("Media has finished processing, we need to change the object's workflow.")
                    workflow = getToolByName(self.context, 'portal_workflow')
                    workflow.doActionFor(self.context, 'submit')
                    logger.info("Object %s has been successfuly moved to 'pending revision' state." % self.context.absolute_url())
                else:
                    logger.info("No message type specified. Leaving.")

            else:
                logger.info("They do not match. This was a bad request.")

        else:
            logger.info("Got no key. Bad request.")

        return ""


class UpdateLocalFile(grok.View):
    grok.context(IAnonReport)
    grok.name("update-local-file")
    grok.require('zope2.AccessContentsInformation')

    def render(self):
        self.context.update_local_file()
        return self.request.RESPONSE.redirect(self.context.absolute_url())


class RenderUploadWidgetJS(grok.View):
    grok.context(Interface)
    grok.name("render-upload-js.js")
    grok.require('zope2.View')

    # JavaScript template
    js_template_input = """\
        (function($) {
            function endsWith(str, suffix) {
                return str.indexOf(suffix, str.length - suffix.length) !== -1;
            }

            function renderUploadWidget(){

                $("#formfield-form-widgets-file_type").css("display", "none");

                OMUpload.setup({
                element: $('#%(id_uploader)s')[0],
                autoUpload: true,
                multiple:false,
                callbacks: {
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
                    }
                });

                if ($('#form-widgets-file_id').val() != ""){
                    $("#formfield-%(id)s .formHelp").text("%(already_uploaded)s" );
                }
            }
            $().ready(renderUploadWidget);
        })(jQuery);
        """

    def render(self):
        widget_id = self.request.get('widget_id')

        if widget_id:
            setHeader = self.request.response.setHeader
            setHeader('Content-Type', 'text/javascript')

            upload_utility = getUtility(IUpload)
            url = upload_utility.upload_url()
            # XXX: Workaround for translating the JS strings
            # XXX: We need to get the lang from the request, instead of like this.
            upload_error = _(u"Error uploading file, please try again or use a diferent file")
            upload_error = translate(upload_error, domain='openmultimedia.reporter', target_language='es')
            upload_success = _(u"File uploaded correctly")
            upload_success = translate(upload_success, domain='openmultimedia.reporter', target_language='es')
            already_uploaded = _(u"Your file was already uploaded, no need to do it again.")
            already_uploaded = translate(already_uploaded, domain='openmultimedia.reporter', target_language='es')

            return self.js_template_input % dict(id=widget_id,
                                                 id_uploader=widget_id + '-uploader',
                                                 upload_url=url,
                                                 upload_error=upload_error,
                                                 upload_success=upload_success,
                                                 already_uploaded=already_uploaded)
