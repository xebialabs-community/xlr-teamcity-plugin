#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, time
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest
from teamcity.util import error

poll_interval = 5

request = HttpRequest(teamcityServer, username, password)

queueBuildURL = 'httpAuth/app/rest/buildQueue'

buildBody = {
    'buildType': {
        'id': buildId
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

queue_response = request.post(queueBuildURL, buildBody, contentType='application/json')

if queue_response.isSuccessful():
    # polls until the job completes
    resp = json.loads(queue_response.response)
    runID = resp['id']
    statusURL = 'httpAuth/app/rest/buildQueue/taskId:' + runID
    while True:
        time.sleep(poll_interval)
        status_response = request.get(statusURL, contentType='application/xml')
        if status_response.isSuccessful():
            resp = json.loads(status_response.response)
            if resp['state'] == 'finished':
                # Have a build completed
                if resp['status'] == 'SUCCESS':
                    buildNumber = resp['number']
                    print('Build successful with build number: ' + buildNumber)
                    sys.exit(0)
                else:
                    print('Build failed, run ID: ' + runID)
                    print(status_response.getResponse())
                    sys.exit(1)
            else:
                print('Waiting for buildID: ' + buildID + ' to start/finish')
                continue
        else:
            error('Status request failed', status_response)
else:
    error('Queuing failed for buildID: ' + buildID, queue_response)
