"""Constantes pour l'intégration iSMART Modbus."""

DOMAIN = "ismart_modbus"
DEFAULT_NAME = "iSMART Modbus"

# Configuration
CONF_HOST = "host"
CONF_PORT = "port"
CONF_LIGHTS = "lights"
CONF_LIGHT_DEVICE = "device"
CONF_LIGHT_INDEX = "index"
CONF_LIGHT_ADDR = "addr"

# Valeurs par défaut
DEFAULT_PORT = 2080
DEFAULT_TIMEOUT = 2

# États
STATE_OFF = 0
STATE_ON = 1
STATE_ERROR = -1
