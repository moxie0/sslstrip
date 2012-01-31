# Copyright (c) 2004-2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import logging

class ResponseTamperer:

    '''
    ResponseTamperer allows to modify responses to clients.
    '''

    _instance          = None

    _default_config = {"enabled": False}

    def __init__(self):
        self.config       = ResponseTamperer._default_config

    def getLogLevel(self):
        return logging.DEBUG

    def setConfigFile(self, configFile):
        logging.log(self.getLogLevel(), "Reading tamper config file: %s"  % (configFile))
        self.config.update(self.parseConfig(configFile))
        if self.isEnabled():
          logging.log(self.getLogLevel(), "Tampering enabled.")

    def parseConfig(self, configFile):
        # todo read config file
        readConfig = {"enabled": True}
        return readConfig

    def isEnabled(self):
        return self.config["enabled"]

    def tamper(self, url, data, headers, req_headers):
        if not self.isEnabled():
          return data

        # headers manipulation - see http://twistedmatrix.com/documents/10.1.0/api/twisted.web.http_headers.Headers.html
        # setting headers
        #headers.setRawHeaders("X-aaa", ["aaa"])
        # getting headers
        #headers.getRawHeaders("Content-Type")

        return data

    def getInstance():
        if ResponseTamperer._instance == None:
            ResponseTamperer._instance = ResponseTamperer()

        return ResponseTamperer._instance

    getInstance = staticmethod(getInstance)
