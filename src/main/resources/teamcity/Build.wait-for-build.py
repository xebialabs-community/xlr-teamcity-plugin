#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest
from teamcity.util import error

request = HttpRequest(teamcityServer, username, password)
statusURL = 'httpAuth/app/rest/buildQueue/taskId:' + str(taskID)
status_response = request.get(statusURL, contentType='application/json')

if not status_response.isSuccessful():
    error(
        'Request failed - couldn\'t poll for status of build from task ID ' + taskID,
        status_response
    )

resp = json.loads(status_response.response)

if resp['state'] == 'finished':
    buildNumber = resp['number']
    # Have a build completed
    if resp['status'] == 'SUCCESS':
        print('Build successful - build ' + str(buildNumber))
        sys.exit(0)
    else:
        print('Build failed - build ' + str(buildNumber))
        print(status_response.getResponse())
        sys.exit(1)
else:
    if 'waitReason' in resp.keys():
        task.setStatusLine(
            'Build is ' + resp['state'] + \
            '.  ' + resp['waitReason'] + '...'
        )
        task.schedule("teamcity/Build.wait-for-build.py", pollInterval)
    else:
        task.setStatusLine('Build is ' + resp['state'] + '...')
        task.schedule("teamcity/Build.wait-for-build.py", pollInterval)
