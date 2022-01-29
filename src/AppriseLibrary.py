#!/opt/local/bin/python3
#
# Robot Framework Keyword library wrapper for
# https://github.com/rossengeorgiev/aprs-python
# Author: Joerg Schultze-Lutter, 2021
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
from robot.api.logger import librarylogger as logger
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

    # Class-internal Apprise parameters
    __apprise_title = None
    __apprise_body = None
    __apprise_clients = None
    __apprise_attachments = None

    # This is our Apprise object
    __apprise_instance = None

    def __init__(
        self,
        apprise_title: str = DEFAULT_TITLE,
        apprise_body: int = DEFAULT_BODY,
        apprise_clients: list = DEFAULT_CLIENTS,
        apprise_attachments: list = DEFAULT_ATTACHMENTS,
    ):
        self.__apprise_title = apprise_title
        self.__apprise_body = apprise_body
        self.__apprise_instance = None
        self.__apprise_clients = self.__transform_apprise_clients(
            apprise_clients=apprise_clients
        )
        self.__apprise_attachments = self.__transform_apprise_attachments(
            apprise_attachments=apprise_attachments
        )

    def __transform_apprise_clients(self, apprise_clients: object):
        # we will either accept a list item or a string
        if not isinstance(apprise_clients, (list, str)):
            raise TypeError("Apprise 'clients' parameter can either be string or list")

        # if we deal with a string, split it up and return it as a list
        if isinstance(apprise_clients, str):
            return apprise_clients.split(",")
        else:
            return apprise_clients

    def __transform_apprise_attachments(self, apprise_attachments: object):
        # we will either accept a list item or a string
        if not isinstance(apprise_attachments, (list, str)):
            raise TypeError(
                "Apprise 'attachments' parameter can either be string or list"
            )

        # if we deal with a string, split it up and return it as a list
        if isinstance(apprise_attachments, str):
            return apprise_attachments.split(",")
        else:
            return apprise_attachments

    # Python "Getter" methods
    #
    # Note that adding an additional Robot decorator (@keyword) will not
    # cause an error but the keyword will not be recognized later on
    # Therefore, Robot-specific "getter" keywords are required
    @property
    def apprise_title(self):
        return self.__apprise_title

    @property
    def apprise_body(self):
        return self.__apprise_body

    @property
    def apprise_clients(self):
        return self.__apprise_clients

    @property
    def apprise_attachments(self):
        return self.__apprise_attachments

    @property
    def apprise_instance(self):
        return self.__apprise_instance

    # Python "Setter" methods
    #
    # Note that adding an additional Robot decorator (@keyword) will not
    # cause an error but the keyword will not be recognized later on
    # Therefore, Robot-specific "setter" keywords are required

    @apprise_title.setter
    def apprise_title(self, apprise_title: str):
        if not apprise_title:
            raise ValueError("No value for 'title' has been specified")
        self.__apprise_title = apprise_title

    @apprise_body.setter
    def apprise_body(self, apprise_body: str):
        if not apprise_body:
            raise ValueError("No value for 'body' has been specified")
        self.__apprise_body = apprise_body

    @apprise_attachments.setter
    def apprise_attachments(self, apprise_attachments: object):
        if not apprise_attachments:
            return
        self.__apprise_attachments = self.__transform_apprise_attachments(
            apprise_attachments=apprise_attachments
        )

    @apprise_clients.setter
    def apprise_clients(self, apprise_clients: object):
        if not apprise_clients:
            raise ValueError("No value for 'clients' has been specified")
        self.__apprise_clients = self.__transform_apprise_clients(
            apprise_clients=apprise_clients
        )

    @apprise_instance.setter
    def apprise_instance(self, apprise_instance: object):
        # Value can be "None". Therefore,
        # we simply accept the value "as is"
        self.__apprise_instance = apprise_instance

    #
    # Robot-specific "getter" keywords
    #
    @keyword("Get Apprise Title")
    def get_apprise_title(self):
        return self.apprise_title

    @keyword("Get Apprise Body")
    def get_apprise_body(self):
        return self.apprise_body

    @keyword("Get Apprise Clients")
    def get_apprise_clients(self):
        return self.apprise_clients

    @keyword("Get Apprise Attachments")
    def get_apprise_attachments(self):
        return self.apprise_attachments

    #
    # Robot-specific "setter" keywords
    #
    @keyword("Set Apprise Title")
    def set_apprise_title(self, apprise_title: str = None):
        logger.debug(msg="Setting 'title' attribute")
        self.apprise_title = apprise_title

    @keyword("Set Apprise Body")
    def set_apprise_body(self, apprise_body: str = None):
        logger.debug(msg="Setting 'body' attribute")
        self.apprise_body = apprise_body

    @keyword("Set Apprise Clients")
    def set_apprise_clients(self, apprise_clients: object):
        logger.debug(msg="Setting 'clients' attribute")
        self.__apprise_clients = self.__transform_apprise_clients(
            apprise_clients=apprise_clients
        )

    @keyword("Set Apprise Attachments")
    def set_apprise_attachments(self, apprise_attachments: object):
        logger.debug(msg="Setting 'attachments' attribute")
        self.__apprise_clients = self.__transform_apprise_attachments(
            apprise_attachments=apprise_attachments
        )

    @keyword("Add Apprise Client")
    def add_apprise_client(self, apprise_client: str):
        logger.debug(msg=f"Adding Apprise client '{apprise_client}'")
        if apprise_client not in self.apprise_clients:
            self.apprise_clients.append(apprise_client)

    @keyword("Add Apprise Attachment")
    def add_apprise_attachment(self, apprise_attachment: str):
        logger.debug(msg=f"Adding Apprise attachment '{apprise_attachment}'")
        if apprise_attachment not in self.apprise_attachment:
            self.apprise_attachments.append(apprise_attachment)

    @keyword("Remove Apprise Client")
    def remove_apprise_client(self, apprise_client: str):
        logger.debug(msg=f"Removing Apprise client '{apprise_client}' (if present)")
        if apprise_client in self.apprise_clients:
            self.apprise_clients.remove(apprise_client)

    @keyword("Remove Apprise Attachment")
    def remove_apprise_attachment(self, apprise_attachment: str):
        logger.debug(
            msg=f"Adding Apprise attachment '{apprise_attachment}' (if present)"
        )
        if apprise_attachment in self.apprise_attachment:
            self.apprise_attachments.remove(apprise_attachment)

    @keyword("Clear Apprise Clients")
    def clear_apprise_clients(self):
        logger.debug(msg=f"Clearing all Apprise clients")
        self.apprise_clients.clear()

    @keyword("Clear Apprise Attachments")
    def clear_apprise_attachments(self):
        logger.debug(msg=f"Clearing all Apprise Attachments")
        self.apprise_attachments.clear()

    @keyword("Create Apprise Instance")
    def create_apprise_instance(self):
        self.apprise_instance = apprise.Apprise()

    @keyword("Send Apprise Message")
    def send_apprise_message(
        self,
        apprise_title: str = None,
        apprise_body: str = None,
        apprise_clients: str = None,
        apprise_attachments: list = None,
    ):
        if not self.apprise_instance:
            logger.debug(msg="Apprise instance not defined; creating it for the user")
            self.apprise_instance = apprise.Apprise()

        # clear everything that we have in our instance
        self.apprise_instance.clear()

        # If user has submitted clients, discard our list
        # and replace it with the user's list
        if apprise_clients:
            self.apprise_clients = self.__transform_apprise_clients(apprise_clients)

        # If user has submitted attachments, discard our list
        # and replace it with the user's list
        if apprise_attachments:
            self.apprise_attachments = self.__transform_apprise_attachments(apprise_attachments)

        # Attach the clients
        for client in self.apprise_clients:
            logger.debug(msg=f"Attaching client '{client}'")
            self.apprise_instance.add(client)

        # Prepare the attachments (if present at all)
        self.apprise_attachments = (
            copy.deepcopy(apprise_attachments)
            if apprise_attachments
            else copy.deepcopy(self.apprise_attachments)
        )

        # Update title and body in case the user has submitted new values
        self.apprise_title = apprise_title if apprise_title else self.apprise_title
        self.apprise_body = apprise_body if apprise_body else self.apprise_body

        # send the content to Apprise
        logger.debug(msg="Sending message")
        result = self.apprise_instance.notify(
            title=self.apprise_title,
            body=self.apprise_body,
            attach=self.apprise_attachments,
        )

        if not result:
            return "FAIL"
        else:
            return "PASS"

if __name__ == "__main__":
    pass
