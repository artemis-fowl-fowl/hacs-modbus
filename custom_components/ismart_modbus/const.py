"""Constantes pour l'intégration iSMART Modbus."""

DOMAIN = "ismart_modbus"
DEFAULT_NAME = "iSMART Modbus"

"""Configuration réseau (HTTP) et mapping iSMART."""

# Configuration réseau (serveur maison iSMART)
CONF_HOST = "host"
CONF_NET_PORT = "net_port"
CONF_MODE = "mode"  # legacy (2080 getState/writeCoil) | rest (2081 Flask)

# Valeurs par défaut réseau
DEFAULT_HOST = "192.168.1.11"
DEFAULT_NET_PORT = 2081
DEFAULT_MODE = "rest"

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
        "rest_name": "gabriel",
        "type": "switch",
    },
    "lit": {
        "name": "Lit Gabriel",
        "device": 4,
        "coil": 0x2C14,  # Adresse originale
        "rest_name": "lit_gabriel",
        "type": "switch",
    },
    "volet_up": {
        "name": "Volet Gabriel Montée",
        "device": 3,
        "coil": 0x2C03,  # Adresse originale
        "rest_name": "gabriel",
        "type": "switch",
    },
    "volet_down": {
        "name": "Volet Gabriel Descente",
        "device": 3,
        "coil": 0x2C02,  # Adresse originale
        "rest_name": "gabriel",
        "type": "switch",
    },
}

# Tous les appareils (extensible)
ALL_ROOMS = {
    "gabriel": GABRIEL_DEVICES,
    # Ajoute d'autres salles au besoin
}
