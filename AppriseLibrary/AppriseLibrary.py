#!/opt/local/bin/python3
#
# Robot Framework Keyword library wrapper for
# https://github.com/caronc/apprise
# Author: Joerg Schultze-Lutter, 2022
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from robot.api.deco import library, keyword
import apprise
import logging
import copy
import os.path
from enum import Enum

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)

__version__ = "0.3.0"
__author__ = "Joerg Schultze-Lutter"


# Enum which contains Apprise's notification types
# Yes - they are strings but let's stay future proof here
class AppriseNotificationType(Enum):
    info = apprise.NotifyType.INFO
    success = apprise.NotifyType.SUCCESS
    warning = apprise.NotifyType.WARNING
    failure = apprise.NotifyType.FAILURE


# Enum which contains Apprise's supported message body formats
class AppriseBodyFormat(Enum):
    html = apprise.NotifyFormat.HTML
    text = apprise.NotifyFormat.TEXT
    markdown = apprise.NotifyFormat.MARKDOWN


@library(scope="GLOBAL", auto_keywords=True)
class AppriseLibrary:

    # These are Apprise's default parameters
    DEFAULT_TITLE = ""
    DEFAULT_BODY = ""
    DEFAULT_ATTACHMENT_DELIMITER = ","
    DEFAULT_CONFIG_FILE = ""
    DEFAULT_NOTIFY_TYPE = apprise.NotifyType.INFO
    DEFAULT_BODY_FORMAT = apprise.NotifyFormat.HTML

    # Class-internal Apprise parameters
    __title = None
    __body = None
    __clients = None
    __attachments = None
    __attachment_delimiter = None
    __config_file = None
    __notify_type = None
    __body_format = None

    # __instance represents the Apprise core object
    __apprise_instance = None

    def __init__(
        self,
        config_file=DEFAULT_CONFIG_FILE,
        title: str = DEFAULT_TITLE,
        body: int = DEFAULT_BODY,
        clients: list = None,
        attachments: list = None,
        attachment_delimiter: str = DEFAULT_ATTACHMENT_DELIMITER,
        notify_type: str = DEFAULT_NOTIFY_TYPE,
        body_format: str = DEFAULT_BODY_FORMAT,
    ):
        self.__config_file = config_file
        self.__title = title
        self.__body = body
        self.__apprise_instance = None
        self.__attachment_delimiter = attachment_delimiter
        self.__clients = self.__transform_apprise_clients(clients=clients)
        self.__attachments = self.__transform_apprise_attachments(
            attachments=attachments
        )
        self.__notify_type = self.__transform_notify_type(notify_type=notify_type)
        self.__body_format = self.__transform_body_format(body_format=body_format)

    def __transform_apprise_clients(self, clients: object):
        # we will either accept a list item or a string
        if not clients:
            return []
        if not isinstance(clients, (list, str)):
            raise TypeError("Apprise 'clients' parameter can either be string or list")

        # if we deal with a string, split it up and return it as a list
        if isinstance(clients, str):
            return clients.split(",")
        else:
            return clients

    def __transform_apprise_attachments(self, attachments: object):
        # we will either accept a list item or a string
        if not attachments:
            return []
        if not isinstance(attachments, (list, str)):
            raise TypeError(
                "Apprise 'attachments' parameter can either be string or list"
            )

        # if we deal with a string, split it up and return it as a list
        if isinstance(attachments, str):
            return attachments.split(self.attachment_delimiter)
        else:
            return attachments

    def __transform_notify_type(self, notify_type: str):

        if not notify_type:
            raise ValueError("No value for 'notify_type' has been specified")

        # Convert to lower case and check if it exists in our enum
        __nt = notify_type.lower()
        if __nt not in AppriseNotificationType.__members__:
            raise ValueError("Unsupported value for 'notify_type' has been specified")

        # enum exists, let's get the value
        return AppriseNotificationType[__nt].value

    def __transform_body_format(self, body_format: str):

        if not body_format:
            raise ValueError("No value for 'body_format' has been specified")

        # Convert to lower case and check if it exists in our enum
        __bf = body_format.lower()
        if __bf not in AppriseBodyFormat.__members__:
            raise ValueError("Unsupported value for 'body_format' has been specified")

        # enum exists, let's get the value
        return AppriseBodyFormat[__bf].value

    # Python "Getter" methods
    #
    # Note that adding an additional Robot decorator (@keyword) will not
    # cause an error but the keyword will not be recognized later on
    # Therefore, Robot-specific "getter" keywords are required
    @property
    def config_file(self):
        return self.__config_file

    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body

    @property
    def attachment_delimiter(self):
        return self.__attachment_delimiter

    @property
    def clients(self):
        return self.__clients

    @property
    def attachments(self):
        return self.__attachments

    @property
    def apprise_instance(self):
        return self.__apprise_instance

    @property
    def notify_type(self):
        return self.__notify_type

    @property
    def body_format(self):
        return self.__body_format

    # Python "Setter" methods
    #
    # Note that adding an additional Robot decorator (@keyword) will not
    # cause an error but the keyword will not be recognized later on
    # Therefore, Robot-specific "setter" keywords are required

    @config_file.setter
    def config_file(self, config_file: str):
        if not config_file:
            raise ValueError("No value for 'config_file' has been specified")
        self.__config_file = config_file

    @title.setter
    def title(self, title: str):
        if not title:
            raise ValueError("No value for 'title' has been specified")
        self.__title = title

    @body.setter
    def body(self, body: str):
        if not body:
            raise ValueError("No value for 'body' has been specified")
        self.__body = body

    @attachment_delimiter.setter
    def attachment_delimiter(self, attachment_delimiter: str):
        if not attachment_delimiter:
            raise ValueError("No value for 'attachment_delimiter' has been specified")
        if len(attachment_delimiter) != 1:
            raise ValueError("'delimiter' needs to be exactly one character")
        self.__attachment_delimiter = attachment_delimiter

    @attachments.setter
    def attachments(self, attachments: object):
        if not attachments:
            return
        self.__attachments = self.__transform_apprise_attachments(
            attachments=attachments
        )

    @clients.setter
    def clients(self, clients: object):
        self.__clients = self.__transform_apprise_clients(clients=clients)

    @apprise_instance.setter
    def apprise_instance(self, apprise_instance: object):
        # Value can be "None". Therefore,
        # we simply accept the value "as is"
        self.__apprise_instance = apprise_instance

    @notify_type.setter
    def notify_type(self, notify_type: str):
        self.__notify_type = self.__transform_notify_type(notify_type=notify_type)

    @body_format.setter
    def body_format(self, body_format: str):
        self.__body_format = self.__transform_body_format(body_format=body_format)

    #
    # Robot-specific "getter" keywords
    #
    @keyword("Get Config File")
    def get_config_file(self):
        return self.config_file

    @keyword("Get Title")
    def get_title(self):
        return self.title

    @keyword("Get Body")
    def get_body(self):
        return self.body

    @keyword("Get Attachment Delimiter")
    def get_attachment_delimiter(self):
        return self.attachment_delimiter

    @keyword("Get Clients")
    def get_clients(self):
        return self.clients

    @keyword("Get Attachments")
    def get_attachments(self):
        return self.attachments

    @keyword("Get Notify Type")
    def get_notify_type(self):
        return self.notify_type

    @keyword("Get Body Format")
    def get_body_format(self):
        return self.body_format

    #
    # Robot-specific "setter" keywords
    #
    @keyword("Set Config File")
    def set_config_file(self, config_file: str = None):
        logger.debug(msg="Setting 'config_file' attribute")
        self.config_file = config_file

    @keyword("Set Title")
    def set_title(self, title: str = None):
        logger.debug(msg="Setting 'title' attribute")
        self.title = title

    @keyword("Set Body")
    def set_body(self, body: str = None):
        logger.debug(msg="Setting 'body' attribute")
        self.body = body

    @keyword("Set Attachment Delimiter")
    def set_attachment_delimiter(self, attachment_delimiter: str = None):
        logger.debug(msg="Setting 'attachment_delimiter' attribute")
        self.attachment_delimiter = attachment_delimiter

    @keyword("Set Notify Type")
    def set_notify_type(self, notify_type: str = None):
        self.notify_type = self.__transform_notify_type(notify_type=notify_type)

    @keyword("Set Body Format")
    def set_body_format(self, body_format: str = None):
        self.body_format = self.__transform_body_format(body_format=body_format)

    @keyword("Set Clients")
    def set_clients(self, clients: object):
        logger.debug(msg="Setting 'clients' attribute")
        self.__clients = self.__transform_apprise_clients(clients=clients)

    @keyword("Set Attachments")
    def set_attachments(self, attachments: object):
        logger.debug(msg="Setting 'attachments' attribute")
        self.__attachments = self.__transform_apprise_attachments(
            attachments=attachments
        )

    @keyword("Add Client")
    def add_client(self, client: str):
        logger.debug(msg=f"Adding Apprise client '{client}'")
        if client not in self.clients:
            self.clients.append(client)

    @keyword("Add Attachment")
    def add_attachment(self, attachment: str):
        logger.debug(msg=f"Adding attachment '{attachment}'")
        if attachment not in self.attachment:
            self.attachments.append(attachment)

    @keyword("Remove Client")
    def remove_client(self, client: str):
        logger.debug(msg=f"Removing client '{client}' (if present)")
        if client in self.clients:
            self.clients.remove(client)

    @keyword("Remove Attachment")
    def remove_attachment(self, attachment: str):
        logger.debug(msg=f"Removing attachment '{attachment}' (if present)")
        if attachment in self.attachment:
            self.attachments.remove(attachment)

    @keyword("Clear All Clients")
    def clear_all_clients(self):
        logger.debug(msg="Clearing all clients")
        self.clients.clear()

    @keyword("Clear All Attachments")
    def clear_all_attachments(self):
        logger.debug(msg=f"Clearing all Attachments")
        self.attachments.clear()

    @keyword("Create Apprise Instance")
    def create_apprise_instance(self):
        self.apprise_instance = apprise.Apprise()

    @keyword("Send Apprise Message")
    def send_apprise_message(
        self,
        title: str = None,
        body: str = None,
        clients=None,
        attachments=None,
        config_file=None,
        notify_type=None,
        body_format=None,
    ):
        # This is our Apprise config item in case
        # the user has specified a config file
        _apprise_config = None

        # We don't have an instance yet?
        if not self.apprise_instance:
            logger.debug(msg="Apprise instance not defined; creating it for the user")
            self.apprise_instance = apprise.Apprise()

        # Overwrite the initial config file name in case the user has
        # specified a different one
        if config_file and config_file != "":
            self.config_file = config_file

        # Now check if we need to create the Apprise config object
        if self.config_file and self.config_file != "":
            # Does the file exist?
            if os.path.isfile(self.config_file):
                # File exists; create the config object and then
                # add the config file to the config object
                _apprise_config = apprise.AppriseConfig()
                _apprise_config.add(self.config_file)
            else:
                logger.debug(
                    msg=f"Config file '{self.config_file}' does not exist; ignoring config file reference"
                )

        # clear everything that we have in our instance
        self.apprise_instance.clear()

        # If user has submitted clients, discard our list
        # and replace it with the user's list
        if clients:
            self.clients = self.__transform_apprise_clients(clients)

        # If user has submitted attachments, discard our list
        # and replace it with the user's list
        if attachments:
            self.attachments = self.__transform_apprise_attachments(attachments)

        # If user has submitted a notify type, look it up
        if notify_type:
            self.notify_type = self.__transform_notify_type(notify_type=notify_type)

        # If user has submitted a body format, look it up
        if body_format:
            self.body_format = self.__transform_body_format(body_format=body_format)

        # Check if we have received at least one client
        if (self.clients and len(self.clients) < 1) and not _apprise_config:
            raise ValueError(
                "You need to specify at least one target client or an Apprise config file"
            )

        # Process our single client URLs
        # If we have no config file/object , add the clients directly to Apprise
        # otherwise, add the config data to the config object and
        # later on add the config object to Apprise
        for client in self.clients:
            if not _apprise_config:
                logger.debug(msg=f"Attaching client '{client}'")
                self.apprise_instance.add(client)
            else:
                logger.debug(
                    msg=f"Attaching client '{client}' on top of config file configuration"
                )
                _apprise_config.add(client)

        # Prepare the attachments (if present at all)
        self.attachments = (
            copy.deepcopy(attachments)
            if attachments
            else copy.deepcopy(self.attachments)
        )

        # add the config object in case we have enriched it
        if _apprise_config:
            self.apprise_instance.add(_apprise_config)

        # Update title and body in case the user has submitted new values
        self.title = title if title else self.title
        self.body = body if body else self.body

        # send the content to Apprise
        logger.debug(
            msg=f"Sending message with type '{self.notify_type}' and format '{self.body_format}'"
        )

        result = self.apprise_instance.notify(
            title=self.title,
            body=self.body,
            attach=self.attachments,
            notify_type=self.notify_type,
            body_format=self.body_format,
        )
        return result


if __name__ == "__main__":
    pass
