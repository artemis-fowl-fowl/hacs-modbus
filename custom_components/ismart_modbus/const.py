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

# Fonction pour décoder les chaînes en adresses
def decode_input(input_str):
    if input_str.startswith("I"):
        return 0x550 + int(input_str[1:]) - 1
    elif input_str.startswith("X"):
        return 0x560 + int(input_str[1:]) - 1
    else:
        raise ValueError(f"Input string '{input_str}' non valide.")
        
# Exemple d'utilisation
# print(decode_input("I1"))  # Renvoie 0x550
# print(decode_input("X12"))  # Renvoie 0x56B

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

    # ### input sur MemState non pris en charge pour le moment
    #{"name": "Scooter", "device_id": 5, "input": "M8", "output": "Q5", "type": "switch"},
    #{"name": "Zoé", "device_id": 5, "input": "M9", "output": "Q6", "type": "switch"},
    #{"name": "Heures_creuses", "device_id": 5, "input": "I6", "output": "M10", "type": "switch"},


    {"name": "Cabanon", "device_id": 5, "input": "X3", "output": "Y3", "type": "light"},
    
    # ### Output sur MemState non pris en charge pour le moment
    #{"name": "Alarme", "device_id": 5, "input": "I10", "output": "M04", "type": "switch"},
]

COVER_DEVICES = [
    # ===== VOLETS ROULANTS (Device 3) =====
    {"name": "Parents", "device_id": 3, "up": "I2", "down": "I1", "opening": "Q2", "closing": "Q1", "device_class": "shade"},
    {"name": "Gabriel", "device_id": 3, "up": "I4", "down": "I3", "opening": "Q4", "closing": "Q3", "device_class": "shade"},
    {"name": "Paul_W", "device_id": 3, "up": "I6", "down": "I5", "opening": "Q6", "closing": "Q5", "device_class": "shade"},
    {"name": "Paul_S", "device_id": 3, "up": "I8", "down": "I7", "opening": "Q8", "closing": "Q7", "device_class": "shade"},
    {"name": "Sophie", "device_id": 3, "up": "X2", "down": "X1", "opening": "Y2", "closing": "Y1", "device_class": "shade"},
    {"name": "Mezzanine", "device_id": 3, "up": "X4", "down": "X3", "opening": "Y4", "closing": "Y3", "device_class": "shade"},
    {"name": "Velux", "device_id": 3, "up": "X6", "down": "X5", "opening": "Y6", "closing": "Y5", "device_class": "shade"},

    # ===== VOLETS ROULANTS (Device 4) =====
    {"name": "Cathedrale", "device_id": 4, "up": "I2", "down": "I1", "opening": "Q2", "closing": "Q1", "device_class": "shade"},
    {"name": "Buanderie", "device_id": 4, "up": "I4", "down": "I3", "opening": "Q4", "closing": "Q3", "device_class": "shade"},
    {"name": "Cuisine", "device_id": 4, "up": "I6", "down": "I5", "opening": "Q6", "closing": "Q5", "device_class": "shade"},
    {"name": "Sejour W", "device_id": 4, "up": "I8", "down": "I7", "opening": "Q8", "closing": "Q7", "device_class": "shade"},
    {"name": "Sejour S", "device_id": 4, "up": "X2", "down": "X1", "opening": "Y2", "closing": "Y1", "device_class": "shade"},
    {"name": "Escalier", "device_id": 4, "up": "X4", "down": "X3", "opening": "Y4", "closing": "Y3", "device_class": "shade"},
    
    # ===== DIVERS (Device 5) =====
    # Adaptation un peu délicate peut être créer un autre objet pour les portes de garage ?
    {"name": "Garage", "device_id": 5, "up": "I5", "down": "I5", "opening": "Y2", "closing": "Y2", "opened": "M6", "closed": "M7", "device_class": "garage"},

    # Portail: commandes: Y4 ouverture partielle, Y3 ouvre / stop / ferme, demande vérouillage: X3
    #          retours: Run sur M01, Closed sur M2, Locked sur M3

]
