# XLR TeamCity Plugin

[![Build Status][xlr-teamcity-plugin-travis-image] ][xlr-teamcity-plugin-travis-url]
[![Build Status][xlr-teamcity-plugin-codacy-image] ][xlr-teamcity-plugin-codacy-url]
[![Build Status][xlr-teamcity-plugin-code-climate-image] ][xlr-teamcity-plugin-code-climate-url]
[![License: MIT][xlr-teamcity-plugin-license-image] ][xlr-teamcity-plugin-license-url]
[![Github All Releases][xlr-teamcity-plugin-downloads-image] ](<>)
[![Known Vulnerabilities][xlr-teamcity-plugin-snyk-image] ][xlr-teamcity-plugin-snyk-url]

## Overview

A plugin to trigger builds in TeamCity. Latest version implements Agent and Pool manipulation, meaning that when provisoning build machines you can get them assigned to the correct pools.

## Installation

Place the latest released version under the `plugins` dir.

## Types

-   Build

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional
    -   `buildConfID` - The buildConfID for the TeamCity build job, usually found in the settings screen for the build job.
    -   `buildProperties` - A set of key value pairs to submit to configure the build job
    -   `buildNumber` - Output field where the build number will be set on successful completion

-   Get Agents:
    Outputs a Map of Agent Names and IDs

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional

-   Get Pools:
    Outputs a Map of Pool Names and IDs

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional

-   Assign to Pool:
    Assigns an Agent to a Pool

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional
    -   `agentId` - ID of the Agent
    -   `poolId` - ID of the Pool

-   Authorize Agent:
    Sets an Agent's authorized state

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional
    -   `agentId` - ID of the Agent
    -   `agentEnabled` - boolean - whether the Agent should be Authorized or not

-   Authorize Agent:
    Sets an Agent's enabled state

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional
    -   `agentId` - ID of the Agent
    -   `agentEnabled` - boolean - whether the Agent should be Enabled or not

-   Delete Agent:
    Removes an Agent. Service must be stopped on the server

    -   `server` - TeamCity server definition (see below)
    -   `username` - Used to override the TeamCity username - optional
    -   `password` - Used to override the TeamCity password - optional
    -   `agentId` - ID of the Agent

-   Server - In the XL Release Configuration screen
    -   `name` - Friendly name for this TeamCity server
    -   `URL` - URL to the TeamCity server, include port here
    -   `username` - Default username for TeamCity
    -   `password` - Password for the default user
    -   `proxyHost` - Proxy host if required
    -   `proxyPort` - Proxy port if required

## Tiles

-   BuildConfigurationsStatusTile: Displays the build status for all Build Types within a certain project. Remark: The rendering of the status images is browser based.


[xlr-teamcity-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-teamcity-plugin.svg?branch=master

[xlr-teamcity-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-teamcity-plugin

[xlr-teamcity-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/bfdb81824a9c47bea2b3a4b62b120c52

[xlr-teamcity-plugin-codacy-url]: https://www.codacy.com/app/xebialabs-community/xlr-teamcity-plugin

[xlr-teamcity-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-teamcity-plugin/badges/gpa.svg

[xlr-teamcity-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-teamcity-plugin

[xlr-teamcity-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg

[xlr-teamcity-plugin-license-url]: https://opensource.org/licenses/MIT

[xlr-teamcity-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-teamcity-plugin/total.svg

[xlr-teamcity-plugin-snyk-image]: https://snyk.io/test/github/xebialabs-community/xlr-teamcity-plugin/badge.svg

[xlr-teamcity-plugin-snyk-url]: https://snyk.io/test/github/xebialabs-community/xlr-teamcity-plugin
