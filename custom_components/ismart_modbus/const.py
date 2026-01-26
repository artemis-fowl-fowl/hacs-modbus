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
SWITCH_DEVICES = [
    # ===== LUMIERES ETAGE (Device 1) =====
    {"name": "Parents", "device_id": 1, "input": "I1", "output": "Q1", "device_class": "light"},
    {"name": "Dressing", "device_id": 1, "input": "I2", "output": "Q2", "device_class": "light"},
    {"name": "Gabriel", "device_id": 1, "input": "I3", "output": "Q3", "device_class": "light"},
    {"name": "Paul", "device_id": 1, "input": "I4", "output": "Q4", "device_class": "light"},
    {"name": "Sophie", "device_id": 1, "input": "I5", "output": "Q5", "device_class": "light"},
    {"name": "SDB", "device_id": 1, "input": "I6", "output": "Q6", "device_class": "light"},
    {"name": "SDB_miroir", "device_id": 1, "input": "I7", "output": "Q7", "device_class": "light"},
    {"name": "SDB_douche", "device_id": 1, "input": "I8", "output": "Q8", "device_class": "light"},

    {"name": "Grenier", "device_id": 1, "input": "X1", "output": "Y1", "device_class": "light"},
    {"name": "Couloir", "device_id": 1, "input": "X2", "output": "Y2", "device_class": "light"},
    {"name": "Mezzanine", "device_id": 1, "input": "X3", "output": "Y3", "device_class": "light"},
    {"name": "Sejour", "device_id": 1, "input": "X4", "output": "Y4", "device_class": "light"},
    {"name": "Passerelle Sud", "device_id": 1, "input": "X5", "output": "Y5", "device_class": "light"},
    {"name": "SDJ", "device_id": 1, "input": "X6", "output": "Y6", "device_class": "light"},
    {"name": "wc_etage_lumiere", "device_id": 1, "input": "X7", "output": "Y7", "device_class": "light"},

    # ===== LUMIERES RDC (Device 2) =====
    {"name": "Salon1", "device_id": 2, "input": "I1", "output": "Q1", "device_class": "light"},
    {"name": "Salon2", "device_id": 2, "input": "I2", "output": "Q2", "device_class": "light"},
    {"name": "Cuisine", "device_id": 2, "input": "I3", "output": "Q3", "device_class": "light"},
    {"name": "Ilot", "device_id": 2, "input": "I4", "output": "Q4", "device_class": "light"},
    {"name": "Evier", "device_id": 2, "input": "I5", "output": "Q5", "device_class": "light"},
    {"name": "Terrasse", "device_id": 2, "input": "I6", "output": "Q6", "device_class": "light"},
    {"name": "Buanderie", "device_id": 2, "input": "I7", "output": "Q7", "device_class": "light"},
    {"name": "Buanderie_miroir", "device_id": 2, "input": "I8", "output": "Q8", "device_class": "light"},

    {"name": "WC_rdc", "device_id": 2, "input": "X1", "output": "Y1", "device_class": "light"},
    {"name": "Hall", "device_id": 2, "input": "X2", "output": "Y2", "device_class": "light"},
    {"name": "Cellier", "device_id": 2, "input": "X3", "output": "Y3", "device_class": "light"},
    {"name": "Atelier", "device_id": 2, "input": "X4", "output": "Y4", "device_class": "light"},
    {"name": "Preau", "device_id": 2, "input": "X5", "output": "Y5", "device_class": "light"},
    {"name": "Garage", "device_id": 2, "input": "X6", "output": "Y5", "device_class": "light"},
    {"name": "Cave", "device_id": 2, "input": "X7", "output": "Y5", "device_class": "light"},
    {"name": "Cour", "device_id": 2, "input": "X8", "output": "Y8", "device_class": "light"},
    
    # ===== LUMIERES DIVERS (Device 3) =====
    {"name": "Aurélien", "device_id": 3, "input": "X7", "output": "Y5", "device_class": "light"},
    {"name": "Aline", "device_id": 3, "input": "X8", "output": "Y8", "device_class": "light"},

    # ===== LUMIERES DIVERS (Device 4) =====
    {"name": "Sejour_1", "device_id": 4, "input": "X3", "output": "Y3", "device_class": "light"},
    {"name": "Sejour_2", "device_id": 4, "input": "X4", "output": "Y4", "device_class": "light"},
    {"name": "Gabriel_lit", "device_id": 4, "input": "X5", "output": "Y5", "device_class": "light"},
    {"name": "Paul_lit", "device_id": 4, "input": "X6", "output": "Y6", "device_class": "light"},
    {"name": "Sophie_lit", "device_id": 4, "input": "X7", "output": "Y7", "device_class": "light"},

    # ===== DIVERS (Device 5) =====
    {"name": "Salon_lampe", "device_id": 5, "input": "X1", "output": "Y1", "device_class": "light"},
    {"name": "Ampli", "device_id": 5, "input": "X2", "output": "Y2", "device_class": "switch"},
    {"name": "Cabanon", "device_id": 5, "input": "X3", "output": "Y3", "device_class": "light"},
    # A vérifier il y a le portail sur Pompe ??!!
    #{"name": "Pompe", "device_id": 5, "input": "X4", "output": "Y4", "device_class": "switch"},
    #{"name": "Electrovanne_1", "device_id": 5, "input": "X5", "output": "Y5", "device_class": "switch"},
    #{"name": "Electrovanne_2", "device_id": 5, "input": "X6", "output": "Y6", "device_class": "switch"},
    {"name": "SDB_radiateur", "device_id": 4, "input": "X8", "output": "Y8", "device_class": "switch"},
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
    {"name": "Sejour S1", "device_id": 4, "up": "X2", "down": "X1", "opening": "Y2", "closing": "Y1", "device_class": "shade"},
    {"name": "Sejour S2", "device_id": 4, "up": "X4", "down": "X3", "opening": "Y4", "closing": "Y3", "device_class": "shade"},
]
