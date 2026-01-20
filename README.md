# iSMART Modbus - Extension Home Assistant

Extension Home Assistant (HACS) pour contrôler directement les automates iSMART via Modbus RS485.

## 🎯 Caractéristiques

- **Communication directe RS485** : Plus besoin de serveur Python intermédiaire
- **Protocole Modbus RTU natif** : Implémentation complète avec CRC16
- **Configuration simple** : Interface graphique pour configurer le port série
- **Solution tout-en-un** : Toute la logique centralisée dans l'extension

## 📦 Installation

### Via HACS (recommandé)

1. Ouvrir HACS dans Home Assistant
2. Cliquer sur "Integrations"
3. Cliquer sur le menu ⋮ en haut à droite
4. Sélectionner "Custom repositories"
5. Ajouter `https://github.com/artemis-fowl-fowl/hacs-modbus`
6. Catégorie : "Integration"
7. Cliquer sur "Add"
8. Chercher "iSMART Modbus" et installer

### Installation manuelle

1. Copier le dossier `custom_components/ismart_modbus` dans `config/custom_components/`
2. Redémarrer Home Assistant

## ⚙️ Configuration

1. Aller dans **Configuration** → **Intégrations**
2. Cliquer sur **+ Ajouter une intégration**
3. Chercher **iSMART Modbus**
4. Configurer :
   - **Port série** : `/dev/ttyUSB0` (ou votre port RS485)
   - **Vitesse** : `38400` bauds
   - **Timeout** : `0.03` secondes

## 🏠 Entités créées

L'extension crée automatiquement ces entités :

- `switch.gabriel_lumiere` - Lumière chambre Gabriel
- `switch.gabriel_lit` - Lumière lit Gabriel
- `switch.gabriel_volet_up` - Volet Gabriel (montée)
- `switch.gabriel_volet_down` - Volet Gabriel (descente)

## 🔧 Architecture technique

### Fichiers principaux

```
custom_components/ismart_modbus/
├── __init__.py          # Initialisation de l'intégration
├── const.py             # Constantes et mapping des devices
├── config_flow.py       # Interface de configuration
├── manifest.json        # Métadonnées de l'intégration
├── strings.json         # Traductions françaises
├── modbus_interface.py  # Implémentation Modbus RTU
└── switch.py            # Entités switch
```

### Modbus RTU

L'extension implémente nativement le protocole Modbus RTU :

- **Fonction 03H** : Lecture de registres (`readreg`)
- **Fonction 05H** : Écriture de bobine (`writecoil`)
- **CRC16** : Calcul avec polynôme Modbus (0xA001)

### Communication série

- Port : `/dev/ttyUSB0` (configurable)
- Baudrate : `38400` bauds
- Timeout : `30ms` (0.03s)
- Protocole : RS-485 RTU

## 📋 Mapping devices

| Device | Slave | Coil | Description |
|--------|-------|------|-------------|
| 1 | 1 | 0x2C02 | Lumière Gabriel |
| 4 | 4 | 0x2C14 | Lit Gabriel |
| 3 | 3 | 0x2C03 | Volet up |
| 3 | 3 | 0x2C02 | Volet down |

## 🔍 Dépannage

### Entities unavailable

Vérifier :
1. Le port série est correct : `ls -l /dev/ttyUSB*`
2. Les permissions : `sudo usermod -a -G dialout homeassistant`
3. Les logs : **Configuration** → **Logs**

### Erreur de connexion

```bash
# Tester la connexion série
python3 -m serial.tools.miniterm /dev/ttyUSB0 38400
```

### Logs détaillés

Activer les logs debug dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.ismart_modbus: debug
```

## 🆚 Différences avec l'ancienne version

| Ancienne version | Version centralisée |
|-----------------|---------------------|
| Serveur Python externe (domotique_unified.py) | Tout dans l'extension |
| Communication HTTP (ports 2080/2081) | Communication RS485 directe |
| Dépendance : aiohttp | Dépendance : pyserial |
| Configuration : host/port/mode | Configuration : serial_port/baudrate |

## 🚀 Évolution future

- [ ] Ajout d'un coordinateur pour la lecture d'état périodique
- [ ] Support de toutes les pièces (pas seulement Gabriel)
- [ ] Entités cover pour les volets
- [ ] Entités binary_sensor pour le feedback d'état
- [ ] Support des capteurs de température DS1820

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

## 👤 Auteur

Gabriel - [@artemis-fowl-fowl](https://github.com/artemis-fowl-fowl)

