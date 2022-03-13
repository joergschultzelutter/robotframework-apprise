# This is a simple robot which sends a push message through Apprise
# Author: Joerg Schultze-Lutter
# https://www.github.com/joergschultzelutter/robotframework-apprise

*** Settings ***
Library			  AppriseLibrary

*** Variables ***

# This is a list of images that we are giong to transmit as attachments
@{IMAGE_LIST}     https://miro.medium.com/max/553/1*wnMQPTmEsIq0TiRgfX4hig.png   https://raw.githubusercontent.com/caronc/apprise/master/apprise/assets/themes/default/apprise-logo.png

# This variable holds 1..n Apprise messenger configurations. You can either use
# string variables or list variables for submitting the configuration
#
# Option 1 - submit as a comma-separated string
#            Examples:
#                       ${CLIENT_LIST}      tgram://bottoken/ChatID
#                       ${CLIENT_LIST}      tgram://bottoken/ChatID,prowl://apikey/providerkey,msteams://TokenA/TokenB/TokenC/
# Option 2 - submit as a List item
#            Example:   @{CLIENT_LIST}      tgram://bottoken/ChatID     prowl://apikey/providerkey      msteams://TokenA/TokenB/TokenC/
#
# Apprise messenger account configurations - see https://github.com/caronc/apprise
#
${CLIENT_LIST}    CONFIGURE_THIS

#
# You can also specify a single Apprise configuration file as config source
# Details: see https://github.com/caronc/apprise/wiki/config
#
${CONFIG_FILE}    config.yaml

*** Test Cases ***
Send Apprise Message using Apprise client config list
    [Documentation]         Send Apprise Message using Apprise client config list
    Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    clients=${CLIENT_LIST}     attachments=${IMAGE_LIST}

Send Apprise Message using Apprise YAML config file
    [Documentation]         Send Apprise Message using Apprise YAML config file
    Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    config_file=${CONFIG_FILE}     attachments=${IMAGE_LIST}
