#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, ast, re
from httputil.HttpRequest import HttpRequest

httpRequest = HttpRequest(teamcityServer, username, password)
urlPrefix = 'httpAuth/app/rest/'
authUrl = urlPrefix + 'agents/id:' + agentId + '/enabledInfo'
body = "<enabledInfo status='"+ str(agentEnabled).lower() +"'><comment><text>"+comment+"</text></comment></enabledInfo>"
amend_response = httpRequest.put(authUrl,body,contentType='application/xml')

if amend_response.isSuccessful():
    print("isSuccessful")
    print(amend_response.getResponse())
    
else:
    print("isNotSuccessful")
    raise Exception(amend_response.getResponse())