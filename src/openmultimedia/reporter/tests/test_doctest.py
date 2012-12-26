# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from openmultimedia.reporter.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/anonreport.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/anonreport_video.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/ireport.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/listado_report.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/remote_process_fail.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/remote_process_success.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/invalid_callback_url.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/workflow.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('tests/proper_error_handling.txt',
                                     package='openmultimedia.reporter'),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
