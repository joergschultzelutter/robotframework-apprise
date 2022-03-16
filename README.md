# robotframework-apprise
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![CodeQL](https://github.com/joergschultzelutter/robotframework-apprise/actions/workflows/codeql.yml/badge.svg)](https://github.com/joergschultzelutter/robotframework-apprise/actions/workflows/codeql.yml)

```robotframework-apprise``` is a [Robot Framework](https://www.robotframework.org) keyword collection for the [Apprise](https://github.com/caronc/apprise) push message library. It enables Robot Framework users to send push/email messages to every message service supported by Apprise.

![transmit](https://github.com/joergschultzelutter/robotframework-apprise/blob/master/img/message.jpg?raw=true)

## Installation

The easiest way is to install this package is from pypi:

    pip install robotframework-apprise

## Robot Framework Library Example

In order to run the example code, you need to provide at least one valid target messenger. Have a look at [Apprise's list of supported messenger platforms](https://github.com/caronc/apprise/wiki)

- [send_apprise_message.robot](https://github.com/joergschultzelutter/robotframework-apprise/blob/master/test/send_apprise_message.robot)

## Library usage and supported keywords

| Keyword                                             | Description                                                                                                                                                                                                                          |
|-----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ``Send Apprise Message``                            | Sends a push message through Apprise                                                                                                                                                                                                 |
| ``Set Clients`` and ``Set Attachments``             | Sets a new value list and replace the previous values                                                                                                                                                                                |
| ``Add Client`` and ``Add Attachment``               | Adds a value to an existing list                                                                                                                                                                                                     |
| ``Remove Client`` and ``Remove Attachment``         | Removes a value from an existing list (if present). Trying to remove a non-existing entry will NOT result in an error                                                                                                                |
| ``Clear All Clients`` and ``Clear All Attachments`` | Completely removes the current values from the respective list                                                                                                                                                                       |
| ``Set Attachment Delimiter``                        | Optional delimiter reconfiguration - see details below                                                                                                                                                                               |
| ``Set Notify Type``                                 | Sets one of Apprise's [supported notify types](https://github.com/caronc/apprise/wiki/Development_API#message-types-and-themes). Valid values are ``info``,``success``,``warning``, and ``failure``. Default notify type is ``info`` |
| ``Set Body Format``                                 | Sets one of Apprise's [supported body formats](https://github.com/caronc/apprise/wiki/Development_API#notify--send-notifications). Valid values are ``html``,``text``, and ``markdown``. Default body format is ``html``             |
| ``Set Config File``                                 | Allows you to specify a single Apprise [config file](https://github.com/caronc/apprise#configuration-files) in YAML or Text format                                                                                                   |

Both ``clients`` and ``attachments`` options can be passed as a ``List`` type variable __or__ as a ``string``. If you use a ``string``, the default delimiter is a comma ``,``. Use the ``Set Attachment Delimiter`` keyword in case you need to use a different delimiter for your attachments.

All ``Set ...`` keywords provide corresponding ``Get ...`` keywords.

``Attachments`` are purely optional. Providing at least one ``Client`` is mandatory, though.

Examples:

```robot
# Send a message with one client and a List which contains our images
@{IMAGE_LIST}=          Create List     http://www.mysite.com/image1.jpg    http://www.mysite.com/image2.jpg
Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    clients=<apprise_client>     attachments=${IMAGE_LIST}
```

```robot
# Send a message with one client. Our attachments use a comma-separated string (default)
Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    clients=<apprise_client>     attachments=http://www.mysite.com/image1.jpg,http://www.mysite.com/image2.jpg
```

```robot
# Send a message with one client. Our attachments use a custom delimiter ^
Set Attachment Delimiter    ^
Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    clients=<apprise_client>     attachments=http://www.mysite.com/image1.jpg^http://www.mysite.com/image2.jpg
```

```robot
# Send a message with one client and a List which contains our images
@{IMAGE_LIST}=          Create List     http://www.mysite.com/image1.jpg    http://www.mysite.com/image2.jpg
Set Test Variable       ${CONFIG_FILE}  config.yaml
Send Apprise Message    title=Robot Framework Apprise Demo   body=Connect to Apprise with your Robot Framework Tests!    config_file=${CONFIG_FILE}     attachments=${IMAGE_LIST}
```

## Known issues

- The current version of this library does not support Apprise's whole feature set. Options such as tagging are not implemented (but may work if you use a [config file](https://github.com/caronc/apprise#configuration-files)-based setting)
- Unlike the original Apprise API, only one YAML config file is currently supported with this Robot Framework keyword library.
