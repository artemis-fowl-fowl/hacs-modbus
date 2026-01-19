# Configuration iSMART Modbus - Guide complet

## Installation dans Home Assistant

### Étape 1 : Préparer le repository pour HACS

1. Poussez votre repository sur GitHub avec la structure suivante:
```
.github/
  workflows/
    hassfest.yaml
    validate.yaml
custom_components/
  ismart_modbus/
    __init__.py
    config_flow.py
    const.py
    light.py
    manifest.json
    strings.json
    README.md
hacs.json
README.md
```

2. Votre repository doit être public pour que HACS le détecte

### Étape 2 : Ajouter à HACS

1. Dans Home Assistant, ouvrez HACS
2. Cliquez sur ⋯ > Custom repositories
3. Ajoutez: `https://github.com/VOTRE_USERNAME/VOTRE_REPO`
4. Sélectionnez "Integration" comme type
5. Cliquez "Create"
6. Cherchez "iSMART Modbus" et installez

### Étape 3 : Configurer l'intégration

#### Méthode 1 : Via l'UI Home Assistant (Recommandé)

1. Allez à Paramètres > Appareils et services > Créer une intégration
2. Cherchez "iSMART Modbus"
3. Entrez votre serveur: `192.168.1.11`
4. Entrez le port: `2080`
5. À l'étape suivante, entrez vos lampes au format JSON

## Configuration des lampes (JSON)

Basez-vous sur votre `scripts.js`. Voici comment mapper vos lampes :

### Lampes à index < 100 (outState)

Ces lampes lisent leur état dans le tableau `outState`:

```json
[
  {"name": "Parents", "device": 1, "index": 0, "addr": "0x2C00"},
  {"name": "Dressing", "device": 1, "index": 1, "addr": "0x2C01"},
  {"name": "Gabriel", "device": 1, "index": 2, "addr": "0x2C02"},
  {"name": "Salon 1", "device": 2, "index": 0, "addr": "0x2C00"},
  {"name": "Cuisine", "device": 2, "index": 2, "addr": "0x2C02"}
]
```

### Lampes à index >= 100 (memState)

Ces lampes lisent leur état dans le tableau `memState` avec `index - 100`:

```json
[
  {"name": "Arrosage auto", "device": 5, "index": 109, "addr": "0x0549"},
  {"name": "Prise charge Scooter", "device": 5, "index": 107, "addr": "0x0547"},
  {"name": "Borne charge VE", "device": 5, "index": 108, "addr": "0x0548"}
]
```

## Configuration complète

Voici un exemple complet avec vos lampes :

```json
[
  {"name": "Parents", "device": 1, "index": 0, "addr": "0x2C00"},
  {"name": "Dressing", "device": 1, "index": 1, "addr": "0x2C01"},
  {"name": "Gabriel", "device": 1, "index": 2, "addr": "0x2C02"},
  {"name": "Paul", "device": 1, "index": 3, "addr": "0x2C03"},
  {"name": "Sophie", "device": 1, "index": 4, "addr": "0x2C04"},
  {"name": "SDB", "device": 1, "index": 5, "addr": "0x2C05"},
  {"name": "Miroir SDB", "device": 1, "index": 6, "addr": "0x2C06"},
  {"name": "Douche", "device": 1, "index": 7, "addr": "0x2C07"},
  {"name": "Grenier", "device": 1, "index": 8, "addr": "0x2C10"},
  {"name": "Couloir", "device": 1, "index": 9, "addr": "0x2C11"},
  {"name": "Mezzanine", "device": 1, "index": 10, "addr": "0x2C12"},
  {"name": "Sejour", "device": 1, "index": 11, "addr": "0x2C13"},
  {"name": "Passerelle", "device": 1, "index": 12, "addr": "0x2C14"},
  {"name": "Cabanon", "device": 1, "index": 13, "addr": "0x2C15"},
  {"name": "SDJ", "device": 1, "index": 14, "addr": "0x2C16"},
  {"name": "WC Etage", "device": 1, "index": 15, "addr": "0x2C17"},
  {"name": "Salon 1", "device": 2, "index": 0, "addr": "0x2C00"},
  {"name": "Salon 2", "device": 2, "index": 1, "addr": "0x2C01"},
  {"name": "Cuisine", "device": 2, "index": 2, "addr": "0x2C02"},
  {"name": "Ilot", "device": 2, "index": 3, "addr": "0x2C03"},
  {"name": "Evier", "device": 2, "index": 4, "addr": "0x2C04"},
  {"name": "Terrasse", "device": 2, "index": 5, "addr": "0x2C05"},
  {"name": "Buanderie", "device": 2, "index": 6, "addr": "0x2C06"},
  {"name": "Miroir RDC", "device": 2, "index": 7, "addr": "0x2C07"},
  {"name": "WC RDC", "device": 2, "index": 8, "addr": "0x2C10"},
  {"name": "Hall", "device": 2, "index": 9, "addr": "0x2C11"},
  {"name": "Cellier", "device": 2, "index": 10, "addr": "0x2C12"},
  {"name": "Atelier", "device": 2, "index": 11, "addr": "0x2C13"},
  {"name": "Preau", "device": 2, "index": 12, "addr": "0x2C14"},
  {"name": "Garage", "device": 2, "index": 13, "addr": "0x2C15"},
  {"name": "Cave", "device": 2, "index": 14, "addr": "0x2C16"},
  {"name": "Cour", "device": 2, "index": 15, "addr": "0x2C17"},
  {"name": "Lit Aurel", "device": 3, "index": 14, "addr": "0x2C16"},
  {"name": "Lit Aline", "device": 3, "index": 15, "addr": "0x2C17"},
  {"name": "Sejour.A", "device": 4, "index": 10, "addr": "0x2C12"},
  {"name": "Sejour.B", "device": 4, "index": 11, "addr": "0x2C13"},
  {"name": "Lit Gabriel", "device": 4, "index": 12, "addr": "0x2C14"},
  {"name": "Lit Paul", "device": 4, "index": 13, "addr": "0x2C15"},
  {"name": "Lit Sophie", "device": 4, "index": 14, "addr": "0x2C16"},
  {"name": "RadSDB", "device": 5, "index": 6, "addr": "0x2C06"},
  {"name": "Salon.A", "device": 5, "index": 0, "addr": "0x2C00"},
  {"name": "Ampli", "device": 5, "index": 1, "addr": "0x2C01"},
  {"name": "Arrosage auto", "device": 5, "index": 109, "addr": "0x0549"},
  {"name": "Arrosage Zone 1", "device": 5, "index": 2, "addr": "0x2C02"},
  {"name": "Arrosage Zone 2", "device": 5, "index": 3, "addr": "0x2C03"},
  {"name": "Prise charge Scooter", "device": 5, "index": 107, "addr": "0x0547"},
  {"name": "Borne charge VE", "device": 5, "index": 108, "addr": "0x0548"}
]
```

## Dépannage

### La lumière n'apparaît pas

1. Vérifiez que le serveur Modbus est accessible
2. Vérifiez l'adresse IP et le port dans les logs
3. Redémarrez Home Assistant

### La lumière n'éteint pas

Vérifiez que:
- L'adresse `addr` correspond à celle de votre serveur
- Le numéro de `device` est correct (1-5)
- L'`index` est bon pour le type de sortie

### Voir les logs

Allez à Paramètres > Système > Journaux et cherchez "ismart_modbus"

## Support du protocole

L'intégration utilise le protocole HTTP de votre serveur Modbus:

- **Lecture**: `GET /getState` - Récupère l'état de tous les appareils
- **Écriture**: `GET /writeCoil[device,addr,value]` - Contrôle un appareil

Les adresses hexadécimales (0x2C00) sont automatiquement converties en la forme requise.
