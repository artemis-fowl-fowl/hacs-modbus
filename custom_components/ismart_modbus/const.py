"""Constantes pour l'intégration iSMART Modbus."""

DOMAIN = "ismart_modbus"
DEFAULT_NAME = "iSMART Modbus"

"""Configuration série RS485 et mapping iSMART."""

# Configuration série
CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_TIMEOUT = "timeout"

# Valeurs par défaut
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 38400
DEFAULT_TIMEOUT = 0.03

# Appareils Gabriel (liste pour faciliter l'utilisation)
GABRIEL_DEVICES = [
    {
        "name": "gabriel_lumiere",
        "device_id": 1,
        "coil": 0x2C02,
        "device_class": "light",
    },
    {
        "name": "gabriel_lit",
        "device_id": 4,
        "coil": 0x2C14,
        "device_class": "light",
    },
    {
        "name": "gabriel_volet_up",
        "device_id": 3,
        "coil": 0x2C03,
        "device_class": "shutter",
    },
    {
        "name": "gabriel_volet_down",
        "device_id": 3,
        "coil": 0x2C02,
        "device_class": "shutter",
    },
]
