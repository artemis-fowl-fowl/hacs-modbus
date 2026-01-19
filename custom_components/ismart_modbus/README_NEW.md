# iSMART Modbus pour Home Assistant

Extension HACS simplifiée pour contrôler les automates iSMART Modbus via Home Assistant.

## Installation

1. Ajoute ce repo à HACS :
   - Menu → HACS → Intégrations → ⋯ → Dépôts personnalisés
   - URL: `https://github.com/artemis-fowl-fowl/hacs-modbus`
   - Catégorie: `Intégration`

2. Redémarre Home Assistant.

3. Ajoute l'intégration :
   - Paramètres → Appareils et services → Créer une automatisation
   - Cherche "iSMART Modbus"
   - Configure ton port série (`/dev/ttyUSB0`), baudrate (38400), méthode (rtu)

## Configuration

### Exemple minimal (Gabriel)

Après l'installation, tu obtiens automatiquement :
- `switch.gabriel_lumiere` (Lumière Gabriel)
- `switch.gabriel_lit` (Lit Gabriel)
- `switch.gabriel_volet_up` (Volet montée)
- `switch.gabriel_volet_down` (Volet descente)

### Cover template (volets)

Pour combiner les deux switches en cover, ajoute dans `configuration.yaml` :

```yaml
template:
  - cover:
      - unique_id: tpl_vr_gabriel
        name: VR Gabriel
        default_entity_id: cover.vr_gabriel
        open_cover:
          - action: switch.turn_on
            target:
              entity_id: switch_gabriel_volet_up
        close_cover:
          - action: switch.turn_on
            target:
              entity_id: switch_gabriel_volet_down
        stop_cover:
          - action: switch.turn_off
            target:
              entity_id: switch_gabriel_volet_up
```

Puis redémarre HA.

## Étendre pour d'autres salles

Édite `custom_components/ismart_modbus/const.py` et ajoute une nouvelle salle :

```python
PARENTS_DEVICES = {
    "lumiere": {
        "name": "Lumière Parents",
        "device": 1,  # Numéro du device dans le script JS
        "coil": 0x2C00,
        "type": "switch",
    },
}

ALL_ROOMS = {
    "gabriel": GABRIEL_DEVICES,
    "parents": PARENTS_DEVICES,  # <- Ajoute ici
}
```

Redémarre l'intégration pour voir les nouveaux switches.

## Dépannage

### Les switches restent indisponibles ?
- Vérifie le port `/dev/ttyUSB0` (change si nécessaire).
- Regarde les logs Modbus : Paramètres → Système → Journaux → Filtre "modbus".
- Si "Illegal data address", le slave ID ou la coil sont incorrects ; ajuste dans const.py.

### Erreur de connexion ?
- Assure-toi que la passerelle Modbus (ou le dongle RS-485) est bien connectée.
- Teste avec le service `modbus.write_coil` (Outils Développeur → Services).

## Licence

MIT
