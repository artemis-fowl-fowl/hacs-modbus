"""Config flow pour iSMART Modbus (série RS485)."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_SERIAL_PORT,
    CONF_BAUDRATE,
    CONF_TIMEOUT,
    DEFAULT_SERIAL_PORT,
    DEFAULT_BAUDRATE,
    DEFAULT_TIMEOUT,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ISmartModbusConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow pour iSMART Modbus en mode série RS485."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Étape utilisateur : demander port série, baudrate, timeout."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input.get(CONF_SERIAL_PORT, DEFAULT_SERIAL_PORT))
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Required(CONF_SERIAL_PORT, default=DEFAULT_SERIAL_PORT): str,
            vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): int,
            vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): vol.Coerce(float),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={}
        )
