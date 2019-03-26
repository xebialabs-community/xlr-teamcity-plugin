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
import logging

import teamcity
from teamcity import TeamCityClient

reload(teamcity)

logger = logging.getLogger("TeamCity")
logger.info("Executing %s" % task.getTaskType())

teamcity_client = TeamCityClient(teamcityServer, username=None, password=None, logger=logger)
response = teamcity_client.teamcity_wait_for_build(locals())

if response['state'] == 'finished':
    buildNumber = response['number']
    # Have a build completed
    if response['status'] == 'SUCCESS':
        print('Build successful - build ' + str(buildNumber))
        sys.exit(0)
    else:
        print('Build failed - build ' + str(buildNumber))
        print(response)
        sys.exit(1)
else:
    if 'waitReason' in response.keys():
        task.setStatusLine(
            'Build is ' + response['state'] + \
            '.  ' + response['waitReason'] + '...'
        )
        task.schedule("teamcity/Build.wait-for-build.py", pollInterval)
    else:
        task.setStatusLine('Build is ' + response['state'] + '...')
        task.schedule("teamcity/Build.wait-for-build.py", pollInterval)
