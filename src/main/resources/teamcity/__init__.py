#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import tempfile

from com.xebialabs.xlr.ssl import LoaderUtil
from java.nio.file import Files, Paths, StandardCopyOption

import requests
from requests.auth import HTTPBasicAuth


def set_ca_bundle_path():
    ca_bundle_path = extract_file_from_jar("requests/cacert.pem")
    os.environ['REQUESTS_CA_BUNDLE'] = ca_bundle_path


def extract_file_from_jar(config_file):
    file_url = LoaderUtil.getResourceBySelfClassLoader(config_file)
    if file_url:
        tmp_file, tmp_abs_path = tempfile.mkstemp()
        tmp_file.close()
        Files.copy(file_url.openStream(), Paths.get(
            tmp_abs_path), StandardCopyOption.REPLACE_EXISTING)
        return tmp_abs_path
    else:
        return None


if 'REQUESTS_CA_BUNDLE' not in os.environ:
    set_ca_bundle_path()


class TeamCityClient(object):
    def __init__(self, configuration, username, password, logger=None):
        self.logger = logger
        self.logger.info("Initializing TeamCityClient object")
        self.host = configuration["url"]
        self.username = username if username else configuration["username"]
        self.password = password if password else configuration["password"]
        self.proxy_host = configuration["proxyHost"]
        self.proxy_port = configuration["proxyPort"]
        self.proxy_username = configuration["proxyUsername"]
        self.proxy_password = configuration["proxyPassword"]
        # TODO support proxy authentication and https proxies?
        self.proxy = None
        if configuration['proxyHost']:
            self.proxy = {'http': '%s:%s' % (
                configuration['proxyHost'], configuration['proxyPort'])}
        self.logger.info("Exiting __init__()")

    def teamcity_getagents(self, variables):
        request_url = self.host + "/app/rest/agents"
        payload = {'locator': 'authorized:any'}
        response = requests.get(request_url, params=payload, headers={'Accept': 'application/json'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()
        result = {}
        for agent in response.json()['agent']:
            result[agent['name']] = agent['id']
        variables['agents'] = result

    def teamcity_authorizeagent(self, variables):
        request_url = self.host + "/app/rest/agents/id:" + \
            variables['agentId'] + "/authorized"
        content = '' + str(variables['agentEnabled']).lower()
        response = requests.put(request_url, data=content, headers={'Content-Type': 'text/plain'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()

    def teamcity_enableagent(self, variables):
        request_url = self.host + "/app/rest/agents/id:" + \
            variables['agentId'] + "/enabledInfo"
        content = {"comment": {"text": "%s" %
                               variables["comment"]}, "status": variables["agentEnabled"]}
        response = requests.put(request_url, json=content, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()

    def teamcity_deleteagent(self, variables):
        request_url = self.host + "/app/rest/agents/id:" + variables['agentId']
        response = requests.delete(request_url,  headers={'Accept': 'application/json'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()

    def teamcity_getpools(self, variables):
        request_url = self.host + "/app/rest/agentPools"
        response = self._get_response(request_url)
        result = {}
        for pool in response['agentPool']:
            result[pool['name']] = pool['id']
        variables['pools'] = result

    def teamcity_assigntopool(self,variables):
        request_url = self.host + "/app/rest/agentPools/id:" + variables["poolId"] + "/agents"
        content = {"id":"%s" % variables["agentId"]}
        response = requests.post(request_url, json=content, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()

    def teamcity_build(self,variables):
        request_url = self.host + "/app/rest/buildQueue"
        content = {'buildType': { 'id': variables['buildID'] }}
        if len(variables['buildProperties']) > 0:
            content['properties'] = {"property": []}
            for prop in variables['buildProperties'].keys():
                content["properties"]["property"].append(
                {
                    "name": prop,
                    "value": variables['buildProperties'][prop]
                }
                )
        response = requests.post(request_url, json=content, headers={'Accept':'application/json','Content-Type': 'application/json'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()
        return response.json()

    def teamcity_wait_for_build(self,variables):
        request_url = self.host + "/app/rest/buildQueue/taskId:" + str(variables['taskID'])
        return self._get_response(request_url)

    def get_build_configuration_statuses(self, variables):
        request_url = self.host + "/app/rest/buildTypes?locator=affectedProject:(id:%s)&fields=buildType(id,name,projectName,projectId,builds($locator(running:any,canceled:any,count:1),build(id,number,status,statusText,finishDate)))" % variables['project']
        return self._get_response(request_url)

    def get_build_problem_occurrences(self, build_id):
        request_url = self.host + "/app/rest/problemOccurrences?locator=build:%s&fields=count,problemOccurrence(id,details)" % build_id
        return self._get_response(request_url)

    def get_build_test_occurrences(self, build_id):
        request_url = self.host + "/app/rest/testOccurrences?locator=build:%s&fields=count,testOccurrence(id,status,details)" % build_id
        return self._get_response(request_url)
    
    def get_build_log(self, build_id):
        request_url = self.host + "/downloadBuildLog.html?buildId=%s" % build_id
        response = requests.get(request_url, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()
        return response.text


    def get_latest_successful_build(self, build_configuration_id):
        request_url = self.host + "/app/rest/builds/?locator=buildType:(id:%s),status:SUCCESS,count:1&fields=build(number,status)" % build_configuration_id
        return self._get_response(request_url)


    def _get_response(self, request_url):
        response = requests.get(request_url, headers={'Accept': 'application/json'}, auth=HTTPBasicAuth(self.username, self.password),
                                proxies=self.proxy, verify=False)
        response.raise_for_status()
        return response.json()


