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
from robot.api.logger import librarylogger as robotlogger
import apprise
import logging
import copy

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)

__version__ = "0.1.0"
__author__ = "Joerg Schultze-Lutter"


@library(scope="GLOBAL", auto_keywords=True)
class AppriseLibrary:

    # These are Apprise's default parameters
    DEFAULT_TITLE = ""
    DEFAULT_BODY = ""
    DEFAULT_CLIENTS = []
    DEFAULT_ATTACHMENTS = []
    DEFAULT_DELIMITER = ","

    # Class-internal Apprise parameters
    __title = None
    __body = None
    __clients = None
    __attachments = None
    __delimiter = None

    # This is our Apprise object
    __instance = None

    def __init__(
        self,
        title: str = DEFAULT_TITLE,
        body: int = DEFAULT_BODY,
        clients: list = DEFAULT_CLIENTS,
        attachments: list = DEFAULT_ATTACHMENTS,
        delimiter: str = DEFAULT_DELIMITER,
    ):
        self.__title = title
        self.__body = body
        self.__instance = None
        self.__delimiter = delimiter
        self.__clients = self.__transform_apprise_clients(clients=clients)
        self.__attachments = self.__transform_apprise_attachments(
            attachments=attachments
        )

    def __transform_apprise_clients(self, clients: object):
        # we will either accept a list item or a string
        if not isinstance(clients, (list, str)):
            raise TypeError("Apprise 'clients' parameter can either be string or list")

        # if we deal with a string, split it up and return it as a list
        if isinstance(clients, str):
            return clients.split(self.delimiter)
        else:
            return clients

    def __transform_apprise_attachments(self, attachments: object):
        # we will either accept a list item or a string
        if not isinstance(attachments, (list, str)):
            raise TypeError(
                "Apprise 'attachments' parameter can either be string or list"
            )

        # if we deal with a string, split it up and return it as a list
        if isinstance(attachments, str):
            return attachments.split(self.delimiter)
        else:
            return attachments

    # Python "Getter" methods
    #
    # Note that adding an additional Robot decorator (@keyword) will not
    # cause an error but the keyword will not be recognized later on
    # Therefore, Robot-specific "getter" keywords are required
    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body

    @property
    def delimiter(self):
        return self.__delimiter

    @property
    def clients(self):
        return self.__clients

    @property
    def attachments(self):
        return self.__attachments

    @property
    def instance(self):
        return self.__instance

    # Python "Setter" methods
    #
    # Note that adding an additional Robot decorator (@keyword) will not
    # cause an error but the keyword will not be recognized later on
    # Therefore, Robot-specific "setter" keywords are required

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

    @delimiter.setter
    def delimiter(self, delimiter: str):
        if not delimiter:
            raise ValueError("No value for 'delimiter' has been specified")
        if len(delimiter) != 1:
            raise ValueError("'delimiter' needs to be exactly one character")
        self.__delimiter = delimiter

    @attachments.setter
    def attachments(self, attachments: object):
        if not attachments:
            return
        self.__attachments = self.__transform_apprise_attachments(
            attachments=attachments
        )

    @clients.setter
    def clients(self, clients: object):
        if not clients:
            raise ValueError("No value for 'clients' has been specified")
        self.__clients = self.__transform_apprise_clients(clients=clients)

    @instance.setter
    def instance(self, instance: object):
        # Value can be "None". Therefore,
        # we simply accept the value "as is"
        self.__instance = instance

    #
    # Robot-specific "getter" keywords
    #
    @keyword("Get Title")
    def get_title(self):
        return self.title

    @keyword("Get Body")
    def get_body(self):
        return self.body

    @keyword("Get Delimiter")
    def get_delimiter(self):
        return self.delimiter

    @keyword("Get Clients")
    def get_clients(self):
        return self.clients

    @keyword("Get Attachments")
    def get_attachments(self):
        return self.attachments

    #
    # Robot-specific "setter" keywords
    #
    @keyword("Set Title")
    def set_title(self, title: str = None):
        logger.debug(msg="Setting 'title' attribute")
        self.title = title

    @keyword("Set Body")
    def set_body(self, body: str = None):
        logger.debug(msg="Setting 'body' attribute")
        self.body = body

    @keyword("Set Delimiter")
    def set_delimiter(self, delimiter: str = None):
        logger.debug(msg="Setting 'delimiter' attribute")
        self.delimiter = delimiter

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
        self.instance = apprise.Apprise()

    @keyword("Send Apprise Message")
    def send_apprise_message(
        self,
        title: str = None,
        body: str = None,
        clients=None,
        attachments=None,
    ):
        if not self.instance:
            logger.debug(msg="Apprise instance not defined; creating it for the user")
            self.instance = apprise.Apprise()

        # clear everything that we have in our instance
        self.instance.clear()

        # If user has submitted clients, discard our list
        # and replace it with the user's list
        if clients:
            self.clients = self.__transform_apprise_clients(clients)

        # If user has submitted attachments, discard our list
        # and replace it with the user's list
        if attachments:
            self.attachments = self.__transform_apprise_attachments(attachments)

        # Check if we have received at least one client
        if len(self.clients) < 1:
            raise ValueError("You need to specify at least one target client")

        # Attach the clients
        for client in self.clients:
            logger.debug(msg=f"Attaching client '{client}'")
            self.instance.add(client)

        # Prepare the attachments (if present at all)
        self.attachments = (
            copy.deepcopy(attachments)
            if attachments
            else copy.deepcopy(self.attachments)
        )

        # Update title and body in case the user has submitted new values
        self.title = title if title else self.title
        self.body = body if body else self.body

        # send the content to Apprise
        logger.debug(msg="Sending message")

        result = self.instance.notify(
            title=self.title,
            body=self.body,
            attach=self.attachments,
        )
        return result


if __name__ == "__main__":
    pass
