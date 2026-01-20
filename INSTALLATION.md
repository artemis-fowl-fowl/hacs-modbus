# Installation et Configuration de l'extension iSMART Modbus

## 🚀 Étapes d'installation

### 1. Copier l'extension dans Home Assistant

```bash
# Se connecter à Home Assistant (SSH ou terminal)
cd /config

# Créer le dossier custom_components si besoin
mkdir -p custom_components

# Copier l'extension
cp -r /chemin/vers/hacsextnesin/custom_components/ismart_modbus custom_components/
```

### 2. Vérifier les permissions du port série

```bash
# Lister les ports USB
ls -l /dev/ttyUSB*

# Ajouter l'utilisateur homeassistant au groupe dialout
sudo usermod -a -G dialout homeassistant

# Redémarrer Home Assistant
sudo systemctl restart home-assistant
```

### 3. Configurer l'intégration

1. Aller dans **Configuration** → **Intégrations**
2. Cliquer sur **+ Ajouter une intégration**
3. Chercher **iSMART Modbus**
4. Remplir :
   - **Nom** : `iSMART Modbus`
   - **Port série** : `/dev/ttyUSB0`
   - **Vitesse** : `38400`
   - **Timeout** : `0.03`
5. Cliquer sur **Soumettre**

### 4. Vérifier les entités

Les 4 entités doivent apparaître :
- `switch.gabriel_lumiere`
- `switch.gabriel_lit`
- `switch.gabriel_volet_up`
- `switch.gabriel_volet_down`

## 🔧 Structure de l'extension

```
custom_components/ismart_modbus/
├── __init__.py              # Point d'entrée, initialise ModbusInterface
├── const.py                 # Configuration série + mapping GABRIEL_DEVICES
├── config_flow.py           # Wizard de configuration
├── manifest.json            # Dépendance: pyserial>=3.5
├── strings.json             # Textes en français
├── modbus_interface.py      # Logique Modbus (crc16, readreg, writecoil)
└── switch.py                # Entités switch qui appellent ModbusInterface
```

## ✅ Fonctionnement

### Communication Modbus directe

L'extension n'utilise **plus** le serveur Python externe (`domotique_unified.py`).

Elle communique **directement** avec les automates via RS485 :

```python
# Avant (avec serveur HTTP)
POST http://192.168.1.11:2081/api/toggle/gabriel

# Maintenant (Modbus direct)
ModbusInterface.writecoil_device(slave=1, coil=0x2C02, value=1)
```

### Flux de commande

1. Utilisateur clique sur le switch dans Home Assistant
2. `switch.py` appelle `async_turn_on()`
3. `async_add_executor_job()` exécute `ModbusInterface.writecoil_device()`
4. `modbus_interface.py` envoie la trame Modbus RTU via `/dev/ttyUSB0`
5. L'automate iSMART reçoit et exécute la commande
6. Le switch est marqué comme activé

## 📝 Fichiers importants

### `modbus_interface.py`

Contient toute la logique Modbus copiée de `domotique_unified.py` :

- `crc16()` : Calcul CRC16 avec polynôme 0xA001
- `readreg()` : Fonction 03H Modbus
- `writecoil()` : Fonction 05H Modbus
- `ModbusInterface` : Classe de gestion de la connexion série

### `const.py`

Configuration centralisée :

```python
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 38400
DEFAULT_TIMEOUT = 0.03

GABRIEL_DEVICES = [
    {"name": "gabriel_lumiere", "device_id": 1, "coil": 0x2C02, ...},
    {"name": "gabriel_lit", "device_id": 4, "coil": 0x2C14, ...},
    ...
]
```

## 🆚 Comparaison

| Aspect | Ancienne version | Version centralisée |
|--------|------------------|---------------------|
| **Architecture** | Extension HA → HTTP → Serveur Python → Modbus | Extension HA → Modbus |
| **Dépendances** | Serveur externe requis | Autonome |
| **Configuration** | host, port, mode | serial_port, baudrate |
| **Complexité** | 2 composants | 1 composant |
| **Latence** | HTTP + Modbus | Modbus uniquement |

## ⚠️ Notes importantes

1. **Le serveur Python n'est plus nécessaire** : Vous pouvez arrêter `domotique_unified.py`

2. **Une seule connexion série** : L'extension ouvre `/dev/ttyUSB0` au démarrage

3. **Pas de lecture d'état** : Pour l'instant, pas de polling périodique (à venir)

## 🐛 Problèmes courants

### Port série occupé

```
Erreur: Device or resource busy
```

→ Arrêter le serveur Python qui utilise le même port

### Permission denied

```
Erreur: Permission denied: '/dev/ttyUSB0'
```

→ Exécuter `sudo usermod -a -G dialout homeassistant` et redémarrer

### Entities unavailable

→ Vérifier les logs : **Configuration** → **Logs** → Rechercher "ismart_modbus"

## 📚 Ressources

- [Documentation Home Assistant](https://www.home-assistant.io/)
- [Protocole Modbus RTU](https://en.wikipedia.org/wiki/Modbus)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
