# iSMART Modbus for Home Assistant

Cette intégration Home Assistant permet de contrôler votre installation domotique iSMART Modbus directement depuis Home Assistant.

## Fonctionnalités

- Contrôle des lampes (allumer/éteindre)
- Configuration directe dans Home Assistant
- Installation via HACS
- Support de plusieurs appareils Modbus
- Gestion des états en temps réel

## Installation

### Via HACS

1. Ouvrez HACS dans Home Assistant
2. Allez à "Integrations"
3. Cliquez sur les trois points et sélectionnez "Custom repositories"
4. Ajoutez l'URL de ce repository
5. Cherchez "iSMART Modbus" et installez-la
6. Redémarrez Home Assistant

### Manuel

1. Clonez ce repository
2. Copiez le dossier `ismart_modbus` dans `config/custom_components/`
3. Redémarrez Home Assistant

## Configuration

### Via l'interface Home Assistant

1. Allez à Paramètres > Appareils et services > Intégrations
2. Cliquez sur "Créer une intégration"
3. Cherchez "iSMART Modbus"
4. Entrez l'adresse IP et le port de votre serveur Modbus
5. Configurez vos lampes au format JSON:

```json
[
  {
    "name": "Parents",
    "device": 1,
    "index": 0,
    "addr": "0x2C00"
  },
  {
    "name": "Dressing",
    "device": 1,
    "index": 1,
    "addr": "0x2C01"
  }
]
```

## Configuration des lampes

Chaque lampe doit avoir les paramètres suivants (basés sur scripts.js):

- `name`: Nom de la lampe
- `device`: Numéro du device Modbus (1-5)
- `index`: Index de la sortie (0-15 pour outState, 100+ pour memState)
- `addr`: Adresse de commutation en hexadécimal (ex: 0x2C00)

## Exemples

Voici des exemples basés sur votre configuration scripts.js:

```json
[
  {"name": "Parents", "device": 1, "index": 0, "addr": "0x2C00"},
  {"name": "Salon 1", "device": 2, "index": 0, "addr": "0x2C00"},
  {"name": "Cuisine", "device": 2, "index": 2, "addr": "0x2C02"},
  {"name": "Arrosage auto", "device": 5, "index": 109, "addr": "0x0549"},
  {"name": "Borne charge VE", "device": 5, "index": 108, "addr": "0x0548"}
]
```

## Support

Pour les problèmes, consultez vos logs Home Assistant.

## License

MIT
