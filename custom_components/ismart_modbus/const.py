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

# Mapping device → slave ID (device du script JS = slave Modbus direct)
DEVICE_TO_SLAVE = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
}

# Appareils Gabriel
GABRIEL_DEVICES = {
    "lumiere": {
        "name": "Lumière Gabriel",
        "device": 1,
        "coil": 0x2C02,  # Adresse originale du script JS
        "type": "switch",
    },
    "lit": {
        "name": "Lit Gabriel",
        "device": 4,
        "coil": 0x2C14,  # Adresse originale
        "type": "switch",
    },
    "volet_up": {
        "name": "Volet Gabriel Montée",
        "device": 3,
        "coil": 0x2C03,  # Adresse originale
        "type": "switch",
    },
    "volet_down": {
        "name": "Volet Gabriel Descente",
        "device": 3,
        "coil": 0x2C02,  # Adresse originale
        "type": "switch",
    },
}

# Tous les appareils (extensible)
ALL_ROOMS = {
    "gabriel": GABRIEL_DEVICES,
    # Ajoute d'autres salles au besoin
}
