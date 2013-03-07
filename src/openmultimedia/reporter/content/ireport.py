# -*- coding: utf-8 -*-

from five import grok

from zope.component import getMultiAdapter, getUtility

from zope.security import checkPermission

from plone.app.layout.globals.interfaces import IViewView

from plone.app.textfield import RichText

from plone.directives import dexterity, form
from plone.registry.interfaces import IRegistry
from plone.namedfile.interfaces import HAVE_BLOBS

if HAVE_BLOBS:  # pragma: no cover
    from plone.namedfile.field import NamedBlobImage
else:  # pragma: no cover
    from plone.namedfile.field import NamedImage

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from openmultimedia.reporter.interfaces import IReporterSettings
from openmultimedia.reporter import _


class IIReport(form.Schema):
    """
    A section that contains reports
    """

    if HAVE_BLOBS:  # pragma: no cover
        default_preview = NamedBlobImage(title=_(u"Default preview"),
                                         description=_(u"Use this image if there's no preview."),
                                         required=False)
    else:  # pragma: no cover
        default_preview = NamedImage(title=_(u"Default preview"),
                                     description=_(u"Use this image if there's no preview."),
                                     required=False)

    disclaimer = RichText(
        title=_(u'Disclaimer'),
        description=_(u'help_disclaimer', default=u'Enter disclaimer here.'),
        required=False
    )


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i: i + n]


class View(dexterity.DisplayForm):
    grok.context(IIReport)
    grok.require('zope2.View')

    def render(self):
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        if portal_state.anonymous():
            redirect_to = '/i-report'
        else:
            redirect_to = '/listado-report'

        return self.request.response.redirect(self.context.absolute_url()+redirect_to)

class IReportView(dexterity.DisplayForm):
    grok.context(IIReport)
    grok.require('zope2.View')
    grok.name('i-report')
    grok.implements(IViewView)

    def update(self):
        self.actual = 0
        self.total = 0
        publics = self.get_published_reports()
        self.publics = chunks(publics[:20], 2)
        self.main_report_new = None
        if publics:
            self.main_report_new = publics[0]

    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/ireport_view.pt')

        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        if portal_state.anonymous():
            self.request.set('disable_border', 1)

        return pt(self)

    def can_add_reports(self):
        return checkPermission('openmultimedia.reporter.anonreportAddable',
                               self.context)

    def can_edit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def _get_catalog_results(self, state=None, search=None):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "openmultimedia.reporter.anonreport"
        path = '/'.join(self.context.getPhysicalPath())
        sort_on = 'effective'
        sort_order = 'reverse'

        query = {'portal_type': ct,
                 'sort_on': sort_on,
                 'sort_order': sort_order,
                 'path': path}
        if search:
            query['SearchableText'] = search

        if state:
            query['review_state'] = state

        results = pc(**query)

        return results

    def get_published_reports(self):
        reports = self._get_catalog_results('published')
        return reports

    def get_published_reports_search(self, title):
        reports = self._get_catalog_results('published', title)
        return reports

    def get_batch(self):
        #cannot put it on top of file grok error :S
        from Products.CMFPlone import Batch
        return Batch


class ListadoReportView(IReportView):
    grok.require('cmf.ModifyPortalContent')
    grok.name('listado-report')

    def get_reports(self, wf_state):
        reports = self._get_catalog_results(wf_state)
        return reports

    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/listadoreport_view.pt')
        return pt(self)

    def get_non_published_reports(self):
        pc = getToolByName(self.context, 'portal_catalog')
        ct = "openmultimedia.reporter.anonreport"
        path = '/'.join(self.context.getPhysicalPath())
        sort_on = 'Date'
        sort_order = 'reverse'
        states = ['pending', 'private', 'rejected']
        filters = {'review_state': {'operator': 'or', 'query': states},
                   'portal_type': ct,
                   'path': path,
                   'sort_on': sort_on,
                   'sort_order': sort_order}
        reports = pc.searchResults(filters)
        return reports

    def js_update(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IReporterSettings)
        seconds = 10
        if settings.seconds:
            seconds = settings.seconds

        js = """
            $(document).ready(function() {
                setInterval(intervalSetUpdate, %s000);
            });
        """ % seconds

        return js


class ListadoReportPublishedView(IReportView):
    grok.require('zope2.View')
    grok.name('listado-report-published')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        if portal_state.anonymous():
            self.request.set('disable_border', 1)
        self.search = self.request.get('search-report', None)
        self.publics = self.get_published_reports_search(self.search)

    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/listado_published.pt')
        return pt(self)


class DisclaimerView(dexterity.DisplayForm):
    grok.context(IIReport)
    grok.require('zope2.View')
    grok.name('disclaimer-view')

    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/disclaimer_view.pt')
        return pt(self)
