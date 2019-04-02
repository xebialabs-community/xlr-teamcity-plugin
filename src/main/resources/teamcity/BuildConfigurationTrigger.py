import logging
from teamcity import TeamCityClient

logger = logging.getLogger("TeamCity")
logger.info("Executing BuildConfigurationTrigger")

teamcity_client = TeamCityClient(teamcityServer, username=None, password=None, logger=logger)

response = teamcity_client.get_latest_successful_build(buildConfigurationId)

if len(response["build"]) == 1:
    # raise Exception("updating triggerstate with %s" % str(response["build"][0]["number"]))
    triggerState = str(response["build"][0]["number"])
    buildNumber = triggerState