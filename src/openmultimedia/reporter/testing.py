# -*- coding: utf-8 -*-
import cgi
import json
import logging
import os
import sys
import SimpleHTTPServer
import SocketServer

from thread import start_new_thread

from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):  # pragma: no cover

    def do_GET(self):  # flake8: noqa
        try:
            path, rest = self.path.split('?')

        except ValueError:
            path = self.path

        if path == '/imagen.png':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()

            curdir = os.path.dirname(__file__)
            filename = os.path.join(curdir, "tests", "binaries", "imagen.png")
            img = open(filename)

            self.wfile.write(img.read())
            img.close()

            self.wfile.close()

        elif path == '/non-existing.png':
            self.send_response(404)

        elif path == '/imagen/anonreport-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/callback-test-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "callback-test-valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/remote-process-success-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "remote-process-success-valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/workflow-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "workflow-valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/clip/None':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "clip-none-valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/test-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "valid-slug",
                        "publicado": True}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/test-unpublished-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "valid-slug",
                        "publicado": False}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/test-error-slug':
            self.send_response(400)

        elif path == '/imagen/test-invalid-response':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()

            # Invalid JSON
            self.wfile.write('{"slug": "valid-slug", publicado: False}')
            self.wfile.close()

        elif path == '/clip/test-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "valid-slug",
                        "publicado": True}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/clip/test-unpublished-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "valid-slug",
                        "publicado": False}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/clip/test-error-slug':
            self.send_response(400)

        elif path == '/clip/test-invalid-response':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()

            # Invalid JSON
            self.wfile.write('{"slug": "valid-slug", publicado: False}')
            self.wfile.close()

        elif path == '/clip/videoreport-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "clip-videoreport-valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/ireport-valid-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "ireport-valid-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/imagen.png",
                        "thumbnail_pequeno": "http://localhost:15555/imagen.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        elif path == '/imagen/error-handling-non-existing-image-slug':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            response = {"slug": "error-handling-non-existing-image-slug",
                        "publicado": True,
                        "archivo_url": "http://localhost:15555/clips/video.mp4",
                        "thumbnail_grande": "http://localhost:15555/non-existing.png",
                        "thumbnail_pequeno": "http://localhost:15555/non-existing.png"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

        else:
            # import pdb;pdb.set_trace()
            pass

        return

    def do_PUT(self):
        if 'valid-slug' in self.path:
            self.send_response(200)

        elif 'error-slug' in self.path:
            self.send_response(400)

        return

    def do_POST(self):  # flake8: noqa
        content_type = self.headers.get('Content-Type', None)

        content = cgi.FieldStorage(fp=self.rfile,
                                   headers=self.headers,
                                   environ={'REQUEST_METHOD': 'POST',
                                            'CONTENT_TYPE': content_type, })

        if self.path == '/upload':
            if content.value == 'invalid':
                self.send_response(400)

            if content.value == 'valid':
                self.send_response(200)
                self.send_header("id", "my-file-id")
                self.end_headers()

        elif self.path == '/imagen':
            if 'archivo' in content:
                if content['archivo'].value == 'anonreport-invalid-id':
                    self.send_response(400)
                elif content['archivo'].value == 'anonreport-valid-id-no-slug':
                    self.send_response(200)
                elif content['archivo'].value == 'anonreport-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "anonreport-valid-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'invalid-id':
                    self.send_response(400)
                elif content['archivo'].value == 'valid-id-no-slug':
                    self.send_response(200)
                elif content['archivo'].value == 'valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "valid-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'callback-test-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "callback-test-valid-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'remote-process-fail-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "remote-process-fail-valid-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'remote-process-success-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "remote-process-success-valid-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'workflow-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "workflow-valid-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'error-handling-non-existing-image':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "error-handling-non-existing-image-slug"}')
                    self.wfile.close()

                elif content['archivo'].value == 'ireport-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "ireport-valid-slug"}')
                    self.wfile.close()

            else:
                if content['titulo'].value == 'error':
                    self.send_response(400)
                else:
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "valid-slug"}')
                    self.wfile.close()

        elif self.path == '/clip':
            if 'archivo' in content:
                if content['archivo'].value == 'videoreport-invalid-id':
                    self.send_response(400)
                elif content['archivo'].value == 'videoreport-valid-id-no-slug':
                    self.send_response(200)
                elif content['archivo'].value == 'videoreport-valid-id':
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "videoreport-valid-slug"}')
                    self.wfile.close()

            else:
                if content['titulo'].value == 'error':
                    self.send_response(400)
                else:
                    self.send_response(200)

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.end_headers()

                    self.wfile.write('{"slug": "valid-slug"}')
                    self.wfile.close()

        return


class LoggingMsgHandler(logging.Handler):
    """A logs handler that will just store them in an
    internal list
    """

    def __init__(self):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        logging.Handler.__init__(self)
        self.msgs = []

    # def flush(self):
    #     """
    #     Flushes the stream.
    #     """
    #     if self.stream and hasattr(self.stream, "flush"):
    #         self.stream.flush()

    def emit(self, record):
        """
        """
        msg = self.format(record)
        self.msgs.append(msg)

    def clearMsgs(self):
        """ Clear the msgs list
        """
        self.msgs = []


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def startSimpleHTTPServer(self):  # pragma: no cover
        PORT = 15555

        try:
            httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
        except:
            print "\n***************************************************************"
            print "*Internal server could not be started, please run tests again.*"
            print "***************************************************************"
            sys.exit(1)

        print "\nserving internal server at port", PORT
        httpd.serve_forever()

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.reporter
        self.loadZCML(package=openmultimedia.reporter)

    def setUpPloneSite(self, portal):
        # Start our internal server
        self.multimedia_server = start_new_thread(self.startSimpleHTTPServer, ())

        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'openmultimedia.reporter:default')

        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('simple_publication_workflow')

        self.applyProfile(portal, 'openmultimedia.reporter:test_fixture')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='openmultimedia.reporter:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='openmultimedia.reporter:Functional',
)
