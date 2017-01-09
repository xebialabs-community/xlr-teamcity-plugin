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
poolUrl = urlPrefix + 'agentPools'
request = httpRequest.get(poolUrl,contentType='application/xml')

if request.isSuccessful():
    print(request.getResponse())
    pools = {}
    xml = (request.getResponse())
    root = ET.fromstring(xml)
    for child in root:
    	pools[child.attrib['name']] = child.attrib['id']

else:
    print("isNotSuccessful")
    raise Exception(request.getResponse())