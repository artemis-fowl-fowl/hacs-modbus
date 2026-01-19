"""Constantes pour l'intégration iSMART Modbus."""

DOMAIN = "ismart_modbus"
DEFAULT_NAME = "iSMART Modbus"

# Configuration Modbus RTU/RS-485
CONF_PORT = "port"
CONF_BAUDRATE = "baudrate"
CONF_METHOD = "method"

# Valeurs par défaut (RTU/RS-485)
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 38400
DEFAULT_METHOD = "rtu"
DEFAULT_STOPBITS = 1
DEFAULT_BYTESIZE = 8
DEFAULT_PARITY = "N"

# Mapping device → slave ID (device est "slave - 1" dans le script JS original)
# Ex: device=1 → slave=2, device=3 → slave=4, etc.
DEVICE_TO_SLAVE = {
    1: 2,
    2: 2,
    3: 4,
    4: 5,
    5: 6,
}

# Appareils Gabriel (exemple complet pour chambre Gabriel)
GABRIEL_DEVICES = {
    "lumiere": {
        "name": "Lumière Gabriel",
        "device": 1,
        "coil": 0x2C02,
        "type": "switch",
    },
    "lit": {
        "name": "Lit Gabriel",
        "device": 4,
        "coil": 0x2C14,
        "type": "switch",
    },
    "volet_up": {
        "name": "Volet Gabriel Montée",
        "device": 3,
        "coil": 0x2C03,
        "type": "switch",
    },
    "volet_down": {
        "name": "Volet Gabriel Descente",
        "device": 3,
        "coil": 0x2C02,
        "type": "switch",
    },
}

# Tous les appareils (extensible)
ALL_ROOMS = {
    "gabriel": GABRIEL_DEVICES,
    # Ajoute d'autres salles au besoin
}
