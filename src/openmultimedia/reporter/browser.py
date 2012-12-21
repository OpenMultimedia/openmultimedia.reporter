# -*- coding: utf-8 -*-

import hashlib
import logging

from five import grok

from zope.component import getUtility

from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from openmultimedia.reporter.config import PROJECTNAME
from openmultimedia.reporter.interfaces import IUpload


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
