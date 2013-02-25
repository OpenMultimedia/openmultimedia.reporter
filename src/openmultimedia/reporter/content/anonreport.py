# -*- coding: utf-8 -*-

import logging
import os
import urllib2

from zope import schema
from zope.interface import implements
from zope.interface import Invalid
from zope.component import getUtility
from zope.component import getMultiAdapter

from z3c.form import button
from z3c.form.interfaces import ActionExecutionError

from five import grok

from z3c.form.interfaces import IEditForm, IDisplayForm

from plone.dexterity.content import Item
from plone.directives import dexterity, form

from plone import namedfile

from plone.namedfile.interfaces import HAVE_BLOBS

if HAVE_BLOBS:  # pragma: no cover
    from plone.namedfile.field import NamedBlobImage
else:  # pragma: no cover
    from plone.namedfile.field import NamedImage

from Products.CMFCore.interfaces import IActionSucceededEvent

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from collective.prettydate.interfaces import IPrettyDate

from openmultimedia.api.interfaces import IVideoAPI

from openmultimedia.reporter.config import PROJECTNAME

from openmultimedia.reporter.interfaces import IUpload
from openmultimedia.reporter.widgets.upload_widget import UploadFieldWidget

from openmultimedia.reporter import _

logger = logging.getLogger(PROJECTNAME)


class IAnonReport(form.Schema):
    """
    A report that any site visitor can add.
    """

    form.omitted(IEditForm, 'name')
    name = schema.TextLine(
        title=_(u'Name'),
        description=_(u'help_name', default=u'Enter your name.'),
        default=u'',
        required=True
    )

    form.omitted(IEditForm, 'country')
    country = schema.TextLine(
        title=_(u'Country'),
        description=_(u'help_country', default=u'Enter your country.'),
        default=u'',
        required=True
    )

    dexterity.write_permission(file_id='openmultimedia.reporter.anonreportAddable')
    form.widget(file_id=UploadFieldWidget)
    file_id = schema.Text(
        title=_(u'File'),
        description=_(u'upload video or image'),
        required=True,
    )

    dexterity.write_permission(file_slug='openmultimedia.reporter.anonreportAddable')
    form.omitted('file_slug')
    file_slug = schema.Text(required=False)

    date = schema.Datetime(
        title=_(u'Date'),
        description=_(u'help_date',
                      default=(u'Enter here the date in which this photo '
                               'or video was taken.')),
        required=True,
    )

    dexterity.write_permission(file_type='openmultimedia.reporter.anonreportAddable')
    form.omitted(IDisplayForm, 'file_type')
    file_type = schema.TextLine(required=False)

    form.omitted('video_file')
    video_file = schema.Text(required=False)

    form.omitted('image_file')
    if HAVE_BLOBS:  # pragma: no cover
        image_file = NamedBlobImage(required=False)
    else:  # pragma: no cover
        image_file = NamedImage(required=False)

    form.omitted('image_preview')
    if HAVE_BLOBS:  # pragma: no cover
        image_preview = NamedBlobImage(required=False)
    else:  # pragma: no cover
        image_preview = NamedImage(required=False)


class AnonReport(Item):
    """

    """
    implements(IAnonReport)

    def is_image(self):
        return self.file_type == 'image'

    def get_status(self):
        workflowTool = getToolByName(self, "portal_workflow")
        chain = workflowTool.getChainForPortalType(self.portal_type)
        status = workflowTool.getStatusOf(chain[0], self)
        state = status["review_state"]
        return state

    def get_date(self):
        date_utility = getUtility(IPrettyDate)
        return date_utility.date(self.date)

    def is_published_ct(self):
        return self.get_status() == "published"

    def generate_callback_url(self, container):
        # Para poder testear que la correcta callback_url se esta
        # generando, vamos a tener este metodo en el content type

        url = "%s/@@processed_result" % self.__of__(container).absolute_url()

        return url

    def update_local_file(self):
        logger.info("About to update local data for %s" % self.absolute_url())
        upload_utility = getUtility(IUpload)
        response, content = upload_utility.get_structure(
            self.file_slug, self.file_type)
        if response['status'] == '200' and content:
            # We got a valid response, let's store local info for the report
            if not self.is_image() and 'archivo_url' in content:
                # This is a video
                self.video_file = content['archivo_url']
                logger.info("Saved %s as video file" % self.video_file)
            else:
                # This is an image
                self.store_remote_image_locally(content['thumbnail_grande'], 'image_file')
                logger.info("Saved %s as image file" % self.image_file)

            # Finally, let's store the preview image, for both image and videos
            self.store_remote_image_locally(content['thumbnail_pequeno'], 'image_preview')
            logger.info("Saved %s as preview image file" % self.image_file)

    def store_remote_image_locally(self, url, field):
        """ Convenience method to get a remote image and store
        it in some local field
        """
        try:
            logger.info("Getting: %s" % url)
            data = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            logger.info("There was an error when contacting the remote server: %s" % e.msg)
            data = None

        if data:
            filename = os.path.basename(url)
            if HAVE_BLOBS:  # pragma: no cover
                setattr(self, field, namedfile.NamedBlobImage(data.read(), filename=filename))
            else:  # pragma: no cover
                setattr(self, field, namedfile.NamedImage(data.read(), filename=filename))

        else:
            setattr(self, field, data)

    def has_media(self):
        has_media = False

        if self.is_image():
            has_media = self.image_file is not None
        else:
            has_media = self.video_file is not None

        return has_media

    def get_video_widget_url(self):
        video_api = getUtility(IVideoAPI)
        logger.info("Trying to get the video widget for %s" % self.video_file)
        url = video_api.get_video_widget_url('',
                                             400,
                                             {'archivo_url': self.video_file})
        logger.info("Got %s" % url)
        return url

    def render_preview_image(self):
        if not self.image_preview:
            scales = getMultiAdapter((self.aq_parent, self.REQUEST), name="images")
            tag = scales.tag('default_preview', scale="preview")
        else:
            scales = getMultiAdapter((self, self.REQUEST), name="images")
            tag = scales.tag('image_preview', scale="preview")
            
        return tag


class Add(dexterity.AddForm):
    """ Default edit for Ideas
    """
    grok.name('openmultimedia.reporter.anonreport')
    grok.context(IAnonReport)

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        obj = self.createAndAdd(data)
        if obj is None:
            raise ActionExecutionError(Invalid(
                _(u"Error creating the report, please try again")))

        body = {}
        if 'file_type' in data and data['file_type']:
            file_type = data['file_type']
        else:
            self.context.manage_delObjects(obj.id)
            raise ActionExecutionError(Invalid(_(u"Error creating the "
                                                 "report, please try again")))

        if 'IBasic.title' in data:
            body['titulo'] = data['IBasic.title'].encode("utf-8", "ignore")

        if 'file_id' in data and data['file_id']:
            body['archivo'] = data['file_id']

        body['tipo'] = 'soy-reportero'

        callback_url = obj.generate_callback_url(self.context)
        body['callback'] = callback_url

        upload_utility = getUtility(IUpload)
        response, content = upload_utility.create_structure(body, file_type)

        if 'status' not in response.keys() or response['status'] != '200':
            logger.info("Invalid response from server: %s" % response)
            self.context.manage_delObjects(obj.id)
            raise ActionExecutionError(Invalid(_(u"Error creating the "
                                                 "report, please try again")))

        if content and "slug" in content:
            slug = content['slug']
        else:
            logger.info("No slug provided: %s" % content)
            self.context.manage_delObjects(obj.id)
            raise ActionExecutionError(Invalid(_(u"Error creating the "
                                                 "report, please try again")))

        obj.file_slug = slug
        obj.reindexObject()
        self._finishedAdd = True
        IStatusMessage(self.request).addStatusMessage(_(u"Item created"),
                                                      "info")

        self.request.RESPONSE.redirect(self.context.absolute_url())

        return obj


class View(dexterity.DisplayForm):
    grok.context(IAnonReport)
    grok.require('zope2.View')

    def render(self):
        pt = ViewPageTemplateFile('ianonreport_templates/ianonreport_view.pt')
        return pt(self)


@grok.subscribe(IAnonReport, IActionSucceededEvent)
def fetch_content_on_submit(report, event):
    if event.action == "submit":
        report.update_local_file()
