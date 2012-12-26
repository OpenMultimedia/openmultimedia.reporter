# -*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel

from openmultimedia.reporter.interfaces import IReporterSettings
from openmultimedia.reporter import _


class ReporterSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IReporterSettings
    label = _(u'I Report Settings')
    description = _(u'Here you can modify the settings for openmultimedia.reporter.')


class ReporterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ReporterSettingsEditForm
