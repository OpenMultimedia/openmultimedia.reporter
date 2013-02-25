# -*- coding: utf-8 -*-

import math

from five import grok

from zope.security import checkPermission

from plone.directives import dexterity, form

from plone.namedfile.interfaces import HAVE_BLOBS

if HAVE_BLOBS:  # pragma: no cover
    from plone.namedfile.field import NamedBlobImage
else:  # pragma: no cover
    from plone.namedfile.field import NamedImage

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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

class View(dexterity.DisplayForm):
    grok.context(IIReport)
    grok.require('zope2.View')

    batch_size = 5

    def update(self):
        self.actual = 0
        self.total = 0
        publics = self.get_published_reports()
        self.total = int(math.ceil(len(publics) / self.batch_size)) - 1
        if 'action' in self.request.keys():
            action = self.request['action']
            if action == 'next':
                self.actual = int(self.request['actual'])
                if len(publics[(self.actual + 1) * int(self.batch_size):(self.actual + 2) * int(self.batch_size)]) > 0:
                    self.actual += 1
            elif action == 'prev':
                self.actual = int(self.request['actual'])
                if self.actual > 0:
                    self.actual -= 1

        self.publics = publics[self.actual * int(self.batch_size):(self.actual + 1) * int(self.batch_size)]
        self.main_report_new = None
        if self.publics:
            self.main_report_new = self.publics[0]

    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/ireport_view.pt')
        return pt(self)

    def can_add_reports(self):
        return checkPermission('openmultimedia.reporter.anonreportAddable',
                               self.context)

    def can_edit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def _get_catalog_results(self, state=None):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "openmultimedia.reporter.anonreport"
        path = '/'.join(self.context.getPhysicalPath())
        sort_on = 'effective'
        sort_order = 'reverse'

        query = {'portal_type': ct,
                 'sort_on': sort_on,
                 'sort_order': sort_order,
                 'path': path}

        if state:
            query['review_state'] = state

        results = pc(**query)

        return results

    def get_published_reports(self):
        reports = self._get_catalog_results('published')
        return reports


class ListadoReportView(View):
    grok.require('cmf.ModifyPortalContent')
    grok.name('listado-report')

    batch_size = 20

    def update(self):
        self.actual = 0
        self.total = 0
        publics = self.get_non_published_reports()
        self.total = int(math.ceil(len(publics) / self.batch_size)) - 1

        if 'action' in self.request.keys():
            action = self.request['action']
            if action == 'next':
                self.actual = int(self.request['actual'])
                if len(publics[(self.actual + 1) * int(self.batch_size):(self.actual + 2) * int(self.batch_size)]) > 0:
                    self.actual += 1
            elif action == 'prev':
                self.actual = int(self.request['actual'])
                if self.actual > 0:
                    self.actual -= 1
        self.publics = publics[self.actual * int(self.batch_size):(self.actual + 1) * int(self.batch_size)]

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
