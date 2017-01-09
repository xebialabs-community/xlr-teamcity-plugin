#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, ast, re
from httputil.HttpRequest import HttpRequest

httpRequest = HttpRequest(teamcityServer, username, password)
urlPrefix = 'httpAuth/app/rest/'
agentUrl = urlPrefix + 'agentPools/id:'+poolId +'/agents'
body = "<agent id='" + agentId + "'/>"
queue_response = httpRequest.post(agentUrl,body,contentType='application/xml')

if queue_response.isSuccessful():
    print(queue_response.getResponse())
    
else:
    print("isNotSuccessful")
    raise Exception(queue_response.getResponse())