# Preface #

This document describes the xlr-teamcity-plugin implementation.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

[![Build Status][xlr-teamcity-travis-image] ][xlr-teamcity-travis-url]
[![Build Status][xlr-teamcity-codacy-image] ][xlr-teamcity-codacy-url]
[![Build Status][xlr-teamcity-code-climate-image] ][xlr-teamcity-code-climate-url]


[xlr-teamcity-travis-image]: https://travis-ci.org/xebialabs-community/xlr-teamcity-plugin.svg?branch=master
[xlr-teamcity-travis-url]: https://travis-ci.org/xebialabs-community/xlr-teamcity-plugin
[xlr-teamcity-codacy-image]: https://api.codacy.com/project/badge/Grade/b78313b1eb1b4b058dc4512b4d48c26f
[xlr-teamcity-codacy-url]: https://www.codacy.com/app/rvanstone/xlr-teamcity-plugin
[xlr-teamcity-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-teamcity-plugin/badges/gpa.svg
[xlr-teamcity-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-teamcity-plugin


# Overview #

A plugin to trigger builds in TeamCity. Latest version implements Agent and Pool manipulation, meaning that when provisoning build machines you can get them assigned to the correct pools.

## Installation ##

Place the latest released version under the `plugins` dir.

## Types ##

+ Build 
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `buildConfID` - The buildConfID for the TeamCity build job, usually found in the settings screen for the build job.
  * `buildNumber` - Output field where the build number will be set on successful completion

+ Get Agents: 
  Outputs a Map of Agent Names and IDs
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  
+ Get Pools: 
  Outputs a Map of Pool Names and IDs
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  
+ Assign to Pool: 
  Assigns an Agent to a Pool

  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  * `poolId` - ID of the Pool
  
+ Authorize Agent: 
  Sets an Agent's authorized state
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  * `agentEnabled` - boolean - whether the Agent should be Authorized or not

+ Authorize Agent:
  Sets an Agent's enabled state
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  * `agentEnabled` - boolean - whether the Agent should be Enabled or not

+ Delete Agent:
  Removes an Agent. Service must be stopped on the server
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  
+ Server - In the XL Release Configuration screen
  * `name` - Friendly name for this TeamCity server
  * `URL` - URL to the TeamCity server, include port here
  * `username` - Default username for TeamCity
  * `password` - Password for the default user
  * `proxyHost` - Proxy host if required
  * `proxyPort` - Proxy port if required
