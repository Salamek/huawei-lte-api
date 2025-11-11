from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class OnlineUpdate(ApiGroup):
    def check_new_version(self) -> GetResponseType:
        """
        Check for a new version of the firmware.

        :return: New version information.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> new_version_info = online_update.check_new_version()
        >>> print(new_version_info)
        """
        return self._session.get("online-update/check-new-version")

    def set_check_new_version(self) -> SetResponseType:
        """
        Set the check for a new version of the firmware.

        :return: Set response type.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> response = online_update.set_check_new_version()
        >>> print(response)
        """
        return self._session.post_set("online-update/check-new-version")

    def status(self) -> GetResponseType:
        """
        Get the status of the online update.

        :return: Online update status.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> update_status = online_update.status()
        >>> print(update_status)
        """
        return self._session.get("online-update/status")

    def url_list(self) -> GetResponseType:
        """
        Get the list of URLs for the online update.

        :return: List of URLs.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> url_list = online_update.url_list()
        >>> print(url_list)
        """
        return self._session.get("online-update/url-list")

    def ack_newversion(self) -> GetResponseType:
        """
        Acknowledge the new version of the firmware.

        :return: Acknowledgement response.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> ack_response = online_update.ack_newversion()
        >>> print(ack_response)
        """
        return self._session.get("online-update/ack-newversion")

    def set_ack_newversion(self) -> SetResponseType:
        """
        Set the acknowledgement for the new version of the firmware.

        :return: Set response type.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> response = online_update.set_ack_newversion()
        >>> print(response)
        """
        return self._session.post_set("online-update/ack-newversion", {
            "userAckNewVersion": 0,
        })

    def cancel_downloading(self) -> GetResponseType:
        """
        Cancel the downloading of the firmware update.

        Invoking this method is known to cause some devices to reboot.

        :return: Cancel downloading response.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> cancel_response = online_update.cancel_downloading()
        >>> print(cancel_response)
        """
        return self._session.get("online-update/cancel-downloading")

    def set_cancel_downloading(self) -> SetResponseType:
        """
        Set the cancel downloading of the firmware update.

        :return: Set response type.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> response = online_update.set_cancel_downloading()
        >>> print(response)
        """
        return self._session.post_set("online-update/cancel-downloading")

    def upgrade_messagebox(self) -> GetResponseType:
        """
        Get the upgrade message box.

        :return: Upgrade message box.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> messagebox = online_update.upgrade_messagebox()
        >>> print(messagebox)
        """
        return self._session.get("online-update/upgrade-messagebox")

    def set_upgrade_messagebox(self, messagebox: str) -> SetResponseType:
        """
        Set the upgrade message box.

        :param messagebox: Message box content.
        :return: Set response type.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> response = online_update.set_upgrade_messagebox(messagebox="Upgrade available")
        >>> print(response)
        """
        return self._session.post_set("online-update/upgrade-messagebox", {
            "messagebox": messagebox,
        })

    def configuration(self) -> GetResponseType:
        """
        Get the online update configuration.

        :return: Online update configuration.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> config = online_update.configuration()
        >>> print(config)
        """
        return self._session.get("online-update/configuration")

    def autoupdate_config(self) -> GetResponseType:
        """
        Get the auto-update configuration.

        :return: Auto-update configuration.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> autoupdate_config = online_update.autoupdate_config()
        >>> print(autoupdate_config)
        """
        return self._session.get("online-update/autoupdate-config")

    def set_autoupdate_config(self, autoupdate: bool) -> SetResponseType:
        """
        Set the auto-update configuration.

        :param autoupdate: Boolean indicating whether to enable auto-update.
        :return: Set response type.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> response = online_update.set_autoupdate_config(autoupdate=True)
        >>> print(response)
        """
        return self._session.post_set("online-update/autoupdate-config",
                                      {"auto_update": int(autoupdate is True), "ui_download": 0})

    def redirect_cancel(self) -> GetResponseType:
        """
        Cancel the redirection.

        :return: Cancel redirection response.

        Usage example:
        >>> online_update = OnlineUpdate(session)
        >>> cancel_response = online_update.redirect_cancel()
        >>> print(cancel_response)
        """
        return self._session.get("online-update/redirect_cancel")
