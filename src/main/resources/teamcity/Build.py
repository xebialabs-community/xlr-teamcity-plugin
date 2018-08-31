#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, time, ast, re
from xml.etree import ElementTree as ET
from httputil.HttpRequest import HttpRequest

poll_interval = 5

httpRequest = HttpRequest(teamcityServer, username, password)

queueBuildURL = 'httpAuth/app/rest/buildQueue'

buildBody = '<build><buildType id="' + buildID + '"/></build>'
if len(buildProperties) > 0:
    propXML = "<properties>"
    for k in buildProperties.keys():
       propXML = "%s<property name=\"%s\" value=\"%s\"/>" % ( propXML, k, buildProperties[k] )
    propXML = "%s</properties>" % propXML
else:
    print "nothing to do here"
    propXML = ""

buildBody = '<build><buildType id="%s"/>%s</build>' % ( buildID, propXML )


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
