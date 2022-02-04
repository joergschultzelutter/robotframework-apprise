# This is a simple robot which sends a push message through Apprise
# Author: Joerg Schultze-Lutter
# https://www.github.com/joergschultzelutter/robotframework-apprise

*** Settings ***
Library			  AppriseLibrary.py

*** Variables ***
@{IMAGE_LIST}     https://miro.medium.com/max/553/1*wnMQPTmEsIq0TiRgfX4hig.png   https://raw.githubusercontent.com/caronc/apprise/master/apprise/assets/themes/default/apprise-logo.png
${CLIENT}         CONFIGURE_THIS_SETTING_WITH_AT_LEAST_ONE_VALID_APPRISE_ACCOUNT
${CONFIG_FILE}    config.yaml

*** Test Cases ***
Send Message Through Apprise
        Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    clients=${CLIENT}     attachments=${IMAGE_LIST}
        Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    config_file=${CONFIG_FILE}     attachments=${IMAGE_LIST}
