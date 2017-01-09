# Preface #

This document describes the xlr-teamcity-plugin implementation.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

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

+ Get Agents
Outputs a Map of Agent Names and IDs
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  
+ Get Pools
Outputs a Map of Pool Names and IDs
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  
+ Assign to Pool
Assigns an Agent to a Pool
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  * `poolId` - ID of the Pool
  
+ Authorize Agent
Sets an Agent's authorized state
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  * `agentEnabled` - boolean - whether the Agent should be Authorized or not

+ Authorize Agent
Sets an Agent's enabled state
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `agentId` - ID of the Agent
  * `agentEnabled` - boolean - whether the Agent should be Enabled or not

+ Delete Agent
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
