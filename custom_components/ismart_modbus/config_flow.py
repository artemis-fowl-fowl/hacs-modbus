"""Config flow pour iSMART Modbus."""

import json
import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_LIGHTS,
    DEFAULT_PORT,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ISmartModbusConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow pour iSMART Modbus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Gestion de l'étape utilisateur."""
        errors = {}

        if user_input is not None:
            # Vérifier s'il y a déjà une config
            await self.async_set_unique_id(user_input.get(CONF_HOST, DEFAULT_NAME))
            self._abort_if_unique_id_configured()

            # Tester la connexion
            try:
                host = user_input[CONF_HOST]
                port = user_input.get(CONF_PORT, DEFAULT_PORT)
                url = f"http://{host}:{port}/getState"

                session = async_get_clientsession(self.hass)
                async with session.get(url, timeout=DEFAULT_TIMEOUT) as resp:
                    if resp.status != 200:
                        errors["base"] = "connection_error"
                        _LOGGER.error(f"Erreur de connexion: {resp.status}")
                    else:
                        return await self.async_step_lights(user_input)
            except aiohttp.ClientError as err:
                errors["base"] = "connection_error"
                _LOGGER.error(f"Erreur de connexion: {err}")
            except Exception as err:
                errors["base"] = "connection_error"
                _LOGGER.error(f"Erreur: {err}")

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def async_step_lights(
        self, user_input: Dict[str, Any]
    ) -> FlowResult:
        """Gestion de l'étape configuration des lampes."""
        errors = {}

        if "lights_json" in self.hass.data.get("user_input", {}):
            lights_input = self.hass.data["user_input"]["lights_json"]
        else:
            lights_input = None

        if lights_input is not None:
            try:
                lights = json.loads(lights_input)
                if not isinstance(lights, list):
                    errors["base"] = "invalid_json"
                else:
                    user_input[CONF_LIGHTS] = lights
                    user_input[CONF_NAME] = user_input.get(CONF_NAME, DEFAULT_NAME)
                    return self.async_create_entry(
                        title=user_input[CONF_NAME], data=user_input
                    )
            except json.JSONDecodeError:
                errors["base"] = "invalid_json"
                _LOGGER.error("JSON invalide pour les lampes")

        return self.async_show_form(
            step_id="lights",
            data_schema=vol.Schema(
                {
                    vol.Required("lights_json"): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "example": json.dumps(
                    [
                        {
                            "name": "Parents",
                            "device": 1,
                            "index": 0,
                            "addr": "0x2C00",
                        }
                    ],
                    indent=2,
                )
            },
        )

    async def async_step_import(self, import_data: Dict[str, Any]) -> FlowResult:
        """Importer une configuration."""
        return await self.async_step_user(import_data)
