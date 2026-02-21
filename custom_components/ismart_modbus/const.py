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

SCAN_INTERVAL = 2   # Intervalle de polling pour les automates et EM111

""" EM111 registers:
0x0000: Tension sur 32bits (Volts * 10)     (16bits auraient été suffisants car la tension ne pourra atteindre 6553.5V)
0x0002: Courant sur 32bits (Ampères * 100)  (16bits auraient été suffisants car le courant ne pourra atteindre 655.35A)
0x0004: Puissance sur 32bits (Watts * 10)
0x0006: Puissance apparente sur 32bits (VA * 10)
0x0008: Puissance réactive sur 32bits (VAR * 10)
0x000A: Puissance moyenne sur 32bits (Watts * 10)
0x000C: Puissance moyenne crête sur 32bits (Watts * 10)
0x000E: Facteur de puissance sur 16bits (PF * 1000)
0x000F: Fréquence sur 16bits (Hz * 10)
0x0010: Energie totale sur 32bits (kWh * 10)
0x0302: Version code sur 16bits (0 -> A)
0x0303: Revision code sur 16bits (0 -> 0)
"""
EM111_DEVICES = [
    #{"name": "Panneaux solaires", "device_id": 10},
    {"name": "Scooter", "device_id": 11},
    {"name": "ECS", "device_id": 12},
    #{"name": "Zoé", "device_id": 13},
]

ISMART_DEVICES = [1,2,3,4,5]    # device id des 5 automates iSMART.

# Tous les dispositifs de la maison
DEVICES = [
    # ===== LUMIERES ETAGE (Device 1) =====
    {"name": "Parents", "device_id": 1, "input": "I1", "output": "Q1", "type": "light"},
    {"name": "Dressing", "device_id": 1, "input": "I2", "output": "Q2", "type": "light"},
    {"name": "Gabriel", "device_id": 1, "input": "I3", "output": "Q3", "type": "light"},
    {"name": "Paul", "device_id": 1, "input": "I4", "output": "Q4", "type": "light"},
    {"name": "Sophie", "device_id": 1, "input": "I5", "output": "Q5", "type": "light"},
    {"name": "SDB", "device_id": 1, "input": "I6", "output": "Q6", "type": "light"},
    {"name": "SDB_miroir", "device_id": 1, "input": "I7", "output": "Q7", "type": "light"},
    {"name": "SDB_douche", "device_id": 1, "input": "I8", "output": "Q8", "type": "light"},

    {"name": "Grenier", "device_id": 1, "input": "X1", "output": "Y1", "type": "light"},
    {"name": "Couloir", "device_id": 1, "input": "X2", "output": "Y2", "type": "light"},
    {"name": "Mezzanine", "device_id": 1, "input": "X3", "output": "Y3", "type": "light"},
    {"name": "Sejour", "device_id": 1, "input": "X4", "output": "Y4", "type": "light"},

    {"name": "Passerelle", "device_id": 1, "input": "X5", "output": "Y5", "type": "light"},
    {"name": "SDJ", "device_id": 1, "input": "X6", "output": "Y6", "type": "light"},
    {"name": "WC_etage", "device_id": 1, "input": "X7", "output": "Y7", "type": "light"},

    # ===== LUMIERES RDC (Device 2) =====
    {"name": "Salon1", "device_id": 2, "input": "I1", "output": "Q1", "type": "light"},
    {"name": "Salon2", "device_id": 2, "input": "I2", "output": "Q2", "type": "light"},
    {"name": "Cuisine", "device_id": 2, "input": "I3", "output": "Q3", "type": "light"},
    {"name": "Ilot", "device_id": 2, "input": "I4", "output": "Q4", "type": "light"},
    {"name": "Evier", "device_id": 2, "input": "I5", "output": "Q5", "type": "light"},
    {"name": "Terrasse", "device_id": 2, "input": "I6", "output": "Q6", "type": "light"},
    {"name": "Buanderie", "device_id": 2, "input": "I7", "output": "Q7", "type": "light"},
    {"name": "Buanderie_miroir", "device_id": 2, "input": "I8", "output": "Q8", "type": "light"},

    {"name": "WC_RDC", "device_id": 2, "input": "X1", "output": "Y1", "type": "light"},
    {"name": "Hall", "device_id": 2, "input": "X2", "output": "Y2", "type": "light"},
    {"name": "Cellier", "device_id": 2, "input": "X3", "output": "Y3", "type": "light"},
    {"name": "Atelier", "device_id": 2, "input": "X4", "output": "Y4", "type": "light"},
    {"name": "Preau", "device_id": 2, "input": "X5", "output": "Y5", "type": "light"},
    {"name": "Garage", "device_id": 2, "input": "X6", "output": "Y5", "type": "light"},
    {"name": "Cave", "device_id": 2, "input": "X7", "output": "Y5", "type": "light"},
    {"name": "Cour", "device_id": 2, "input": "X8", "output": "Y8", "type": "light"},
    
    # ===== LUMIERES DIVERS (Device 3) =====
    {"name": "Aurélien", "device_id": 3, "input": "X7", "output": "Y5", "type": "light"},
    {"name": "Aline", "device_id": 3, "input": "X8", "output": "Y8", "type": "light"},

    # ===== LUMIERES DIVERS (Device 4) =====
    {"name": "Gabriel_lit", "device_id": 4, "input": "X5", "output": "Y5", "type": "light"},
    {"name": "Paul_lit", "device_id": 4, "input": "X6", "output": "Y6", "type": "light"},
    {"name": "Sophie_lit", "device_id": 4, "input": "X7", "output": "Y7", "type": "light"},
    {"name": "Sejour ?", "device_id": 4, "input": "X7", "output": "Y7", "type": "light"},


    # ===== DIVERS (Device 5) =====
    {"name": "Apoint", "device_id": 5, "input": "I1", "output": "Q1", "type": "light"},
    {"name": "Ampli", "device_id": 5, "input": "I2", "output": "Q2", "type": "switch"},
    {"name": "Electrovanne_1", "device_id": 5, "input": "I3", "output": "Q3", "type": "switch"},
    {"name": "Electrovanne_2", "device_id": 5, "input": "I4", "output": "Q4", "type": "switch"},
    {"name": "SDB_radiateur", "device_id": 5, "input": "I7", "output": "Q7", "type": "switch"},

    {"name": "Scooter", "device_id": 5, "input": "M8", "output": "Q5", "type": "switch"},
    {"name": "Zoé", "device_id": 5, "input": "M9", "output": "Q6", "type": "switch"},
    {"name": "Heures_creuses", "device_id": 5, "input": "I6", "output": "M10", "type": "switch"},


    {"name": "Cabanon", "device_id": 5, "input": "X3", "output": "Y3", "type": "light"},
    
    {"name": "Ouverture partielle", "device_id": 5, "input": "M11", "type": "button"},
    {"name": "Verrouillage", "device_id": 5, "input": "X3", "type": "button"},
    {"name": "Portail verrouillé", "device_id": 5, "output": "M3", "type": "button"},
    # ### Output sur MemState non pris en charge pour le moment
    #{"name": "Alarme", "device_id": 5, "input": "I10", "output": "M04", "type": "switch"},
]

COVER_DEVICES = [
    # ===== VOLETS ROULANTS (Device 3) =====
    {"name": "Parents", "device_id": 3, "up": "I2", "down": "I1", "opening": "Q2", "closing": "Q1", "opened": "M2", "closed": "M1","type": "shutter"},
    {"name": "Gabriel", "device_id": 3, "up": "I4", "down": "I3", "opening": "Q4", "closing": "Q3", "opened": "M4", "closed": "M3", "type": "shutter"},
    {"name": "Paul_W", "device_id": 3, "up": "I6", "down": "I5", "opening": "Q6", "closing": "Q5", "opened": "M6", "closed": "M5", "type": "shutter"},
    {"name": "Paul_S", "device_id": 3, "up": "I8", "down": "I7", "opening": "Q8", "closing": "Q7", "opened": "M8", "closed": "M7", "type": "shutter"},
    {"name": "Sophie", "device_id": 3, "up": "X2", "down": "X1", "opening": "Y2", "closing": "Y1", "opened": "M10", "closed": "M9", "type": "shutter"},
    {"name": "Mezzanine", "device_id": 3, "up": "X4", "down": "X3", "opening": "Y4", "closing": "Y3", "opened": "M12", "closed": "M11", "type": "shutter"},
    {"name": "Velux", "device_id": 3, "up": "X6", "down": "X5", "opening": "Y6", "closing": "Y5", "opened": "M14", "closed": "M13", "type": "shutter"},

    # ===== VOLETS ROULANTS (Device 4) =====
    {"name": "Cathedrale", "device_id": 4, "up": "I2", "down": "I1", "opening": "Q2", "closing": "Q1", "opened": "M2", "closed": "M1", "type": "shutter"},
    {"name": "Buanderie", "device_id": 4, "up": "I4", "down": "I3", "opening": "Q4", "closing": "Q3", "opened": "M4", "closed": "M3", "type": "shutter"},
    {"name": "Cuisine", "device_id": 4, "up": "I6", "down": "I5", "opening": "Q6", "closing": "Q5", "opened": "M6", "closed": "M5", "type": "shutter"},
    {"name": "Sejour W", "device_id": 4, "up": "I8", "down": "I7", "opening": "Q8", "closing": "Q7", "opened": "M8", "closed": "M7", "type": "shutter"},
    {"name": "Sejour S", "device_id": 4, "up": "X2", "down": "X1", "opening": "Y2", "closing": "Y1", "opened": "M10", "closed": "M9", "type": "shutter"},
    {"name": "Escalier", "device_id": 4, "up": "X4", "down": "X3", "opening": "Y4", "closing": "Y3", "opened": "M12", "closed": "M11", "type": "shutter"},
    
    # ===== DIVERS (Device 5) =====
    # Adaptation un peu délicate peut être créer un autre objet pour les portes de garage ?
    {"name": "Garage", "device_id": 5, "move": "I5", "opened": "M6", "closed": "M7", "type": "garage"},

    # Portail: commandes: X4 ouverture partielle, X1 ouvre / stop / ferme, demande vérouillage: X3
    #          retours: Run sur M01, Closed sur M2, Locked sur M3
    {"name": "Portail", "device_id": 5, "move": "M12", "lock": "X3", "partial": "M11", "moving" : "M1", "closed": "M2", "locked": "M3", "type": "gate"},

]
