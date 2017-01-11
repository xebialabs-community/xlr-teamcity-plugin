#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, ast, re
from xml.etree import ElementTree as ET
from httputil.HttpRequest import HttpRequest

httpRequest = HttpRequest(teamcityServer, username, password)
urlPrefix = 'httpAuth/app/rest/'
nonAgentUrl = urlPrefix + 'agents?locator=connected:true,authorized:false'
agentUrl = urlPrefix + 'agents'

request = httpRequest.get(agentUrl,contentType='application/xml')

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

request2 = httpRequest.get(nonAgentUrl,contentType='application/xml')

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