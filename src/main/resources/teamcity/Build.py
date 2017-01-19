#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, ast, re
from xml.etree import ElementTree as ET
from httputil.HttpRequest import HttpRequest

poll_interval = 5

httpRequest = HttpRequest(teamcityServer, username, password)

queueBuildURL = 'httpAuth/app/rest/buildQueue'
buildBody = '<build><buildType id="' + buildID + '"/></build>'

queue_response = httpRequest.post(queueBuildURL, buildBody, contentType='application/xml')

if queue_response.isSuccessful():
    # polls until the job completes
    root = ET.fromstring(queue_response.getResponse())
    runID = root.attrib['id']
    statusURL = 'httpAuth/app/rest/buildQueue/taskId:' + runID
    while True:
        time.sleep(poll_interval)
        status_response = httpRequest.get(statusURL, contentType='application/xml')
        if status_response.isSuccessful():
            root = ET.fromstring(status_response.getResponse())
            if root.attrib['state'] == 'finished':
                # Have a build completed
                if root.attrib['status'] == 'SUCCESS':
                    buildNumber = root.attrib['number']
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
            print('Status request failed')
            sys.exit(1)
else:
    print('Queuing failed for buildID: ' + buildID)
    sys.exit(1)

