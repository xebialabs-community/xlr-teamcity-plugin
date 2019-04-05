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

from dateutil.parser import parse
from teamcity import TeamCityClient

logger = logging.getLogger("TeamCity")
logger.info("Executing BuildConfigurationsStatusTile")
data = {}
if teamcityServer:
    teamcity_client = TeamCityClient(
        teamcityServer, username=None, password=None, logger=logger)
    response = teamcity_client.get_build_configuration_statuses(locals())

    project_statuses = []
    project_names = []
    for build_configuration in response['buildType']:
        project_name = build_configuration["projectName"]
        project_id = build_configuration["projectId"]
        if project_name not in project_names:
            project_names.append(project_name)
            project_statuses.append({"name": project_name, "statusUrl": "%s/app/rest/builds/aggregated/strob:(buildType:(project:(id:%s)))/statusIcon.svg" %
                                     (teamcityServer["url"], project_id), "statuses": []})

        project_status = None
        for pstatus in project_statuses:
            if pstatus["name"] == project_name:
                project_status = pstatus
                break

        if filter == "All" or (filter == "Success" and len(build_configuration["builds"]["build"]) > 0 and build_configuration['builds']['build'][0]['status'] == "SUCCESS") or (filter == "Failed" and len(build_configuration["builds"]["build"]) > 0 and build_configuration['builds']['build'][0]['status'] != "SUCCESS"):
            if len(build_configuration["builds"]["build"]) == 0:
                project_status["statuses"].append({"name": build_configuration['name'], "status": "No Info",
                                 "statusText": "No builds to display", "problemOccurrences": {},
                                 "testOccurrences": {}, "finishDate": "N/A",
                                 "statusUrl": "%s/app/rest/builds/buildType:(id:%s)/statusIcon" % (teamcityServer["url"], build_configuration['id'])})
            else:
                build_problem_occurrences = teamcity_client.get_build_problem_occurrences(
                    build_configuration['builds']['build'][0]['id'])
                build_test_occurrences = teamcity_client.get_build_test_occurrences(
                    build_configuration['builds']['build'][0]['id'])
                build_log = teamcity_client.get_build_log(build_configuration['builds']['build'][0]['id'])
                processed_build_log = ''.join([line for line in build_log.split('\n') if "]W:" in line or "]E:" in line])
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
                project_status["statuses"].append({"name": build_configuration['name'], "status": build_configuration['builds']['build'][0]['status'],
                                 "statusText": build_configuration['builds']['build'][0]['statusText'],
                                 "finishDate": parse(build_configuration['builds']['build'][0]['finishDate']).strftime("%a, %d %b %Y %H:%M:%S") if "finishDate" in build_configuration['builds']['build'][0] else "N/A",
                                 "problemOccurrences": build_problem_occurrences, "testOccurrences": build_test_occurrences,
                                 "buildLog": processed_build_log,
                                 "statusUrl": "%s/app/rest/builds/buildType:(id:%s)/statusIcon" % (teamcityServer["url"], build_configuration['id']),
                                 "buildLogUrl": "%s/downloadBuildLog.html?buildId=%s" % (teamcityServer["url"], build_configuration['builds']['build'][0]['id'])})
    data = {"projectStatuses": project_statuses}
