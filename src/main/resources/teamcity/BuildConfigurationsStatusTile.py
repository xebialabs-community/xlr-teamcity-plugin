#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import logging

import teamcity
from teamcity import TeamCityClient

logger = logging.getLogger("TeamCity")
logger.info("Executing BuildConfigurationsStatusTile")
data = {}
if teamcityServer:
    teamcity_client = TeamCityClient(
        teamcityServer, username=None, password=None, logger=logger)
    response = teamcity_client.get_build_configuration_statuses(locals())

    statuses = []
    project_name = ""
    for build_configuration in response['buildType']:
        project_name = build_configuration["projectName"]
        if filter == "All" or (filter == "Success" and len(build_configuration["builds"]["build"]) > 0 and build_configuration['builds']['build'][0]['status'] == "SUCCESS") or (filter == "Failed" and len(build_configuration["builds"]["build"]) > 0 and build_configuration['builds']['build'][0]['status'] != "SUCCESS"):
            if len(build_configuration["builds"]["build"]) == 0:
                statuses.append({"name": build_configuration['name'], "status": "No Info",
                                "statusText": "No builds to display", "problemOccurrences": {},
                                "testOccurrences": {},
                                "url": "%s/app/rest/builds/buildType:(id:%s)/statusIcon" % (teamcityServer["url"], build_configuration['id'])})
            else:
                build_problem_occurrences = teamcity_client.get_build_problem_occurrences(
                    build_configuration['builds']['build'][0]['id'])
                build_test_occurrences = teamcity_client.get_build_test_occurrences(
                    build_configuration['builds']['build'][0]['id'])
                successCount = 0
                failureCount = 0
                if build_test_occurrences["count"] > 0:
                    for test_occurrence in build_test_occurrences["testOccurrence"]:
                        if test_occurrence["status"] == "SUCCESS":
                            successCount += 1
                        else:
                            failureCount += 1
                build_test_occurrences["successCount"] = successCount
                build_test_occurrences["failureCount"] = failureCount
                statuses.append({"name": build_configuration['name'], "status": build_configuration['builds']['build'][0]['status'],
                                "statusText": build_configuration['builds']['build'][0]['statusText'], "problemOccurrences": build_problem_occurrences,
                                "testOccurrences": build_test_occurrences,
                                "statusUrl": "%s/app/rest/builds/buildType:(id:%s)/statusIcon" % (teamcityServer["url"], build_configuration['id']),
                                "buildLogUrl": "%s/downloadBuildLog.html?buildId=%s" % (teamcityServer["url"], build_configuration['builds']['build'][0]['id'])})
    projectStatus = {"name": project_name,
                     "statusUrl": "%s/app/rest/builds/aggregated/strob:(buildType:(project:(id:%s)))/statusIcon.svg" % (teamcityServer["url"], project)}
    data = {"statuses": statuses, "projectStatus": projectStatus}
