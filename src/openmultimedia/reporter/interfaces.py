# -*- coding: utf-8 -*-

from zope import schema

from zope.interface import Interface

from openmultimedia.reporter import _


class IReporterSettings(Interface):
    """ Interface for the control panel form.
    """

    upload_location = schema.TextLine(
        title=_(u'Upload url'),
        default=u"upload",
        required=True)

    image_notify = schema.TextLine(
        title=_(u'Image notify'),
        default=u'imagen',
        required=True)

    video_notify = schema.TextLine(
        title=_(u'Video notify'),
        default=u'clip',
        required=True)

    security_key = schema.TextLine(
        title=_(u'Security key'),
        default=u'k4}"-^30C$:3l04$(/<5"7*6|Ie"6x',
        required=True)

    key = schema.TextLine(
        title=_(u'Upload key'),
        default=u'telesursoyreporteroplonepruebas',
        required=True)

    seconds = schema.Int(
        title=_(u'Number of seconds to wait to update the content lists'),
        required=False,
    )


class IUpload(Interface):
    """
    Utility that will handle the upload of media to an external service
    """
