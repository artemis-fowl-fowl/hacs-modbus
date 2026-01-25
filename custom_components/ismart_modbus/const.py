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
DEFAULT_TIMEOUT = 0.1  # Augmenté à 100ms pour éviter collisions RS485

# Tous les dispositifs de la maison
LIGHT_DEVICES = [
    # ===== LUMIERES ETAGE (Device 1) =====
    {"name": "parents", "device_id": 1, "coil": 0x0550, "bit_position": 0, "device_class": "light"},
        
    # ===== LUMIERES RDC (Device 2) =====
    {"name": "atelier", "device_id": 2, "coil": 0x0563, "bit_position": 11, "device_class": "light"},
]
COVER_DEVICES = [
    # ===== VOLETS ROULANTS (Device 3) =====
    {"name": "parents", "device_id": 3, "up_coil": 0x2C01, "down_coil": 0x2C00, "up_bit": 1, "down_bit": 0, "open_bit": 9, "closed_bit": 8, "device_class": "cover"},
    {"name": "buanderie", "device_id": 4, "up_coil": 0x2C03, "down_coil": 0x2C02, "up_bit": 3, "down_bit": 2, "open_bit": 103, "closed_bit": 102, "device_class": "cover"},
]

GABRIEL_DEVICES = [
    # ===== LUMIERES ETAGE (Device 1) =====
    {"name": "parents_lumiere", "device_id": 1, "coil": 0x2C00, "device_class": "light"},
    {"name": "dressing_lumiere", "device_id": 1, "coil": 0x2C01, "device_class": "light"},
    {"name": "gabriel_lumiere", "device_id": 1, "coil": 0x2C02, "device_class": "light"},
    {"name": "paul_lumiere", "device_id": 1, "coil": 0x2C03, "device_class": "light"},
    {"name": "sophie_lumiere", "device_id": 1, "coil": 0x2C04, "device_class": "light"},
    {"name": "sdb_lumiere", "device_id": 1, "coil": 0x2C05, "device_class": "light"},
    {"name": "sdb_miroir", "device_id": 1, "coil": 0x2C06, "device_class": "light"},
    {"name": "sdb_douche", "device_id": 1, "coil": 0x2C07, "device_class": "light"},
    {"name": "grenier_lumiere", "device_id": 1, "coil": 0x2C08, "device_class": "light"},
    {"name": "couloir_lumiere", "device_id": 1, "coil": 0x2C11, "device_class": "light"},
    {"name": "mezzanine_lumiere", "device_id": 1, "coil": 0x2C12, "device_class": "light"},
    {"name": "sejour_lumiere", "device_id": 1, "coil": 0x2C13, "device_class": "light"},
    {"name": "pass_s_lumiere", "device_id": 1, "coil": 0x2C14, "device_class": "light"},
    {"name": "sdj_lumiere", "device_id": 1, "coil": 0x2C16, "device_class": "light"},
    {"name": "wc_etage_lumiere", "device_id": 1, "coil": 0x2C17, "device_class": "light"},
    
    # ===== LUMIERES RDC (Device 2) =====
    {"name": "salon1_lumiere", "device_id": 2, "coil": 0x2C00, "device_class": "light"},
    {"name": "salon2_lumiere", "device_id": 2, "coil": 0x2C01, "device_class": "light"},
    {"name": "cuisine_lumiere", "device_id": 2, "coil": 0x2C02, "device_class": "light"},
    {"name": "ilot_lumiere", "device_id": 2, "coil": 0x2C03, "device_class": "light"},
    {"name": "evier_lumiere", "device_id": 2, "coil": 0x2C04, "device_class": "light"},
    {"name": "terrasse_lumiere", "device_id": 2, "coil": 0x2C05, "device_class": "light"},
    {"name": "buanderie_lumiere", "device_id": 2, "coil": 0x2C06, "device_class": "light"},
    {"name": "buanderie_miroir", "device_id": 2, "coil": 0x2C07, "device_class": "light"},
    {"name": "wc_rdc_lumiere", "device_id": 2, "coil": 0x2C08, "device_class": "light"},
    {"name": "hall_lumiere", "device_id": 2, "coil": 0x2C11, "device_class": "light"},
    {"name": "cellier_lumiere", "device_id": 2, "coil": 0x2C12, "device_class": "light"},
    {"name": "atelier_lumiere", "device_id": 2, "coil": 0x2C13, "device_class": "light"},
    {"name": "preau_lumiere", "device_id": 2, "coil": 0x2C14, "device_class": "light"},
    {"name": "garage_lumiere", "device_id": 2, "coil": 0x2C15, "device_class": "light"},
    {"name": "cave_lumiere", "device_id": 2, "coil": 0x2C16, "device_class": "light"},
    {"name": "cour_lumiere", "device_id": 2, "coil": 0x2C17, "device_class": "light"},
    
    # ===== VOLETS ROULANTS (Device 3) =====
    {"name": "volet_parents_down", "device_id": 3, "coil": 0x2C00, "device_class": "shutter"},
    {"name": "volet_parents_up", "device_id": 3, "coil": 0x2C01, "device_class": "shutter"},
    {"name": "volet_gabriel_down", "device_id": 3, "coil": 0x2C02, "device_class": "shutter"},
    {"name": "volet_gabriel_up", "device_id": 3, "coil": 0x2C03, "device_class": "shutter"},
    {"name": "volet_paul_w_down", "device_id": 3, "coil": 0x2C04, "device_class": "shutter"},
    {"name": "volet_paul_w_up", "device_id": 3, "coil": 0x2C05, "device_class": "shutter"},
    {"name": "volet_paul_s_down", "device_id": 3, "coil": 0x2C06, "device_class": "shutter"},
    {"name": "volet_paul_s_up", "device_id": 3, "coil": 0x2C07, "device_class": "shutter"},
    {"name": "volet_sophie_down", "device_id": 3, "coil": 0x2C08, "device_class": "shutter"},
    {"name": "volet_sophie_up", "device_id": 3, "coil": 0x2C09, "device_class": "shutter"},
    {"name": "volet_mezz_down", "device_id": 3, "coil": 0x2C12, "device_class": "shutter"},
    {"name": "volet_mezz_up", "device_id": 3, "coil": 0x2C13, "device_class": "shutter"},
    {"name": "volet_velux_down", "device_id": 3, "coil": 0x2C14, "device_class": "shutter"},
    {"name": "volet_velux_up", "device_id": 3, "coil": 0x2C15, "device_class": "shutter"},
    {"name": "lit_aurel", "device_id": 3, "coil": 0x2C16, "device_class": "light"},
    {"name": "lit_aline", "device_id": 3, "coil": 0x2C17, "device_class": "light"},
    
    # ===== AUTRES (Device 4) =====
    {"name": "volet_cathedrale_down", "device_id": 4, "coil": 0x2C00, "device_class": "shutter"},
    {"name": "volet_cathedrale_up", "device_id": 4, "coil": 0x2C01, "device_class": "shutter"},
    {"name": "sejour_a_lumiere", "device_id": 4, "coil": 0x2C12, "device_class": "light"},
    {"name": "sejour_b_lumiere", "device_id": 4, "coil": 0x2C13, "device_class": "light"},
    {"name": "gabriel_lit", "device_id": 4, "coil": 0x2C14, "device_class": "light"},
    {"name": "paul_lit", "device_id": 4, "coil": 0x2C15, "device_class": "light"},
    {"name": "sophie_lit", "device_id": 4, "coil": 0x2C16, "device_class": "light"},
    {"name": "sdb_radiateur", "device_id": 4, "coil": 0x2C17, "device_class": "switch"},
    
    # ===== EXTERIEURS ET EQUIPEMENTS (Device 5) =====
    {"name": "salon_a_lumiere", "device_id": 5, "coil": 0x2C00, "device_class": "light"},
    {"name": "ampli", "device_id": 5, "coil": 0x2C01, "device_class": "switch"},
    {"name": "cabanon_lumiere", "device_id": 5, "coil": 0x2C02, "device_class": "light"},
    {"name": "pompe", "device_id": 5, "coil": 0x2C03, "device_class": "switch"},
    {"name": "electrovanne_1", "device_id": 5, "coil": 0x2C04, "device_class": "switch"},
    {"name": "electrovanne_2", "device_id": 5, "coil": 0x2C05, "device_class": "switch"},
]
