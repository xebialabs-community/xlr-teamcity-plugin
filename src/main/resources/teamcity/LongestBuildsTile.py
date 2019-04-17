#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from dateutil.parser import parse
from operator import itemgetter
from org.slf4j import LoggerFactory
from teamcity import TeamCityClient

import teamcity
reload(teamcity)

logger = LoggerFactory.getLogger("com.xebialabs")
logger.info("Executing LongestBuildsTile")

builds = []
if teamcityServer:
    teamcity_client = TeamCityClient(
        teamcityServer, username=None, password=None, logger=logger)
    response = teamcity_client.get_builds(locals())
    for build in response['build']:
        start_dt = parse(build['startDate'])
        finish_dt = parse(build['finishDate'])
        delta = finish_dt.getTime() - start_dt.getTime()
        builds.append([delta//1000,build['buildTypeId'],build['number']])
    sorted_builds = sorted(builds, key=itemgetter(0))
    sorted_builds.insert(0,["time","buildConfiguration","number"])
    data = {"builds" : sorted_builds[:11]}
    

