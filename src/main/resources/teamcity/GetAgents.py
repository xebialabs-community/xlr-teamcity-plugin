#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from xml.etree import ElementTree as ET
from httputil.HttpRequest import HttpRequest

httpRequest = HttpRequest(teamcityServer, username, password)
urlPrefix = 'httpAuth/app/rest/'
nonAgentUrl = urlPrefix + 'agents?locator=connected:true,authorized:false'
agentUrl = urlPrefix + 'agents'

request = httpRequest.get(agentUrl, contentType='application/xml')

if request.isSuccessful():
    print("isSuccessful")
    print(request.getResponse())
    xml = (request.getResponse())
    agents = {}
    xml = (request.getResponse())
    root = ET.fromstring(xml)
    for child in root:
        agents[child.attrib['name']] = child.attrib['id']

else:
    print("isNotSuccessful")
    raise Exception(request.getResponse())

request2 = httpRequest.get(nonAgentUrl, contentType='application/xml')

if request2.isSuccessful():
    print("isSuccessful")
    print(request2.getResponse())
    xml = (request2.getResponse())
    xml = (request2.getResponse())
    root = ET.fromstring(xml)
    for child in root:
        agents[child.attrib['name']] = child.attrib['id']

else:
    print("isNotSuccessful")
    raise Exception(request2.getResponse())
