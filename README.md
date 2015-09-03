# Preface #

This document describes the xlr-teamcity-plugin implementation.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

A plugin to trigger builds in TeamCity. Currently a simple implementation which only supports triggering a build using the TeamCity buildConfID and returns the build number.

## Installation ##

Place the latest released version under the `plugins` dir.

## Types ##

+ Build 
  * `server` - TeamCity server definition (see below)
  * `username` - Used to override the TeamCity username - optional 
  * `password` - Used to override the TeamCity password - optional
  * `buildConfID` - The buildConfID for the TeamCity build job, usually found in the settings screen for the build job.
  * `buildNumber` - Output field where the build number will be set on successful completion
+ Server - In the XL Release Configuration screen
  * `name` - Friendly name for this TeamCity server
  * `URL` - URL to the TeamCity server, include port here
  * `username` - Default username for TeamCity
  * `password` - Password for the default user
  * `proxyHost` - Proxy host if required
  * `proxyPort` - Proxy port if required
