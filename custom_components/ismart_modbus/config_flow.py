"""Config flow pour iSMART Modbus (réseau HTTP)."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_HOST,
    CONF_NET_PORT,
    CONF_MODE,
    DEFAULT_HOST,
    DEFAULT_NET_PORT,
    DEFAULT_MODE,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ISmartModbusConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow pour iSMART Modbus en mode réseau (serveur iSMART)."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Étape utilisateur : demander hôte, port, mode réseau."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input.get(CONF_HOST, DEFAULT_HOST))
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
            vol.Required(CONF_NET_PORT, default=DEFAULT_NET_PORT): int,
            vol.Required(CONF_MODE, default=DEFAULT_MODE): vol.In(["rest", "legacy"]),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={}
        )
