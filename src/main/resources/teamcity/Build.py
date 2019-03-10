#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest
from teamcity.util import error

request = HttpRequest(teamcityServer, username, password)

queueBuildURL = 'httpAuth/app/rest/buildQueue'

buildBody = {
    'buildType': {
        'id': buildID
    },
}

if len(buildProperties) > 0:
    buildBody['properties'] = {"property": []}
    for prop in buildProperties.keys():
        buildBody["properties"]["property"].append(
            {
                "name": prop,
                "value": buildProperties[prop]
            }
        )

queue_response = request.post(queueBuildURL, json.dumps(buildBody), contentType='application/json')

if not queue_response.isSuccessful():
    error('Queuing failed for build configuration ID ' + buildID, queue_response)
resp = json.loads(queue_response.response)
taskID = str(resp['id'])
task.schedule('teamcity/Build.wait-for-build.py')
