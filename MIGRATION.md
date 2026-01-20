# 🎉 Migration complète vers extension centralisée

## ✅ Ce qui a été fait

### 1. Centralisation de toute la logique Modbus

Tous les composants nécessaires ont été intégrés directement dans l'extension :

- ✅ **modbus_interface.py** : Implémentation complète du protocole Modbus RTU
  - Fonction `crc16()` : Calcul CRC16 avec polynôme Modbus
  - Fonction `readreg()` : Lecture de registres (0x03)
  - Fonction `writecoil()` : Écriture de bobines (0x05)
  - Classe `ModbusInterface` : Gestion de la connexion série RS485

- ✅ **const.py** : Configuration série au lieu de réseau
  - `CONF_SERIAL_PORT` = "/dev/ttyUSB0"
  - `CONF_BAUDRATE` = 38400
  - `CONF_TIMEOUT` = 0.03
  - `GABRIEL_DEVICES` : Mapping simplifié (sans rest_name)

- ✅ **config_flow.py** : Interface pour configuration série
  - Demande port série, baudrate, timeout
  - Supprimé host/port/mode réseau

- ✅ **__init__.py** : Initialisation ModbusInterface
  - Création de l'instance ModbusInterface au démarrage
  - Connexion au port série
  - Déconnexion propre au unload

- ✅ **switch.py** : Appels Modbus directs
  - Supprimé aiohttp et appels HTTP
  - Utilise `modbus_interface.writecoil_device()`
  - Exécution via `async_add_executor_job()`

- ✅ **manifest.json** : Dépendance pyserial
  - Changé `aiohttp>=3.8.0` → `pyserial>=3.5`

- ✅ **strings.json** : Textes adaptés pour série
  - "Port série", "Vitesse (bauds)", "Timeout"

### 2. Documentation complète

- ✅ **README.md** : Documentation utilisateur
- ✅ **INSTALLATION.md** : Guide d'installation détaillé

### 3. Fichiers nettoyés

Supprimés :
- ❌ cover_template.py (non utilisé)
- ❌ light.py (non utilisé)
- ❌ README_NEW.md (doublon)

## 📁 Structure finale

```
hacsextnesin/
├── custom_components/
│   └── ismart_modbus/
│       ├── __init__.py          ✅ Initialisation + ModbusInterface
│       ├── const.py             ✅ Config série + GABRIEL_DEVICES
│       ├── config_flow.py       ✅ Wizard config série
│       ├── manifest.json        ✅ pyserial>=3.5
│       ├── modbus_interface.py  ✅ Logique Modbus RTU complète
│       ├── strings.json         ✅ Textes français
│       └── switch.py            ✅ Switches avec appels Modbus
├── python/
│   └── domotique_unified.py    ℹ️ Serveur Python (optionnel, plus nécessaire)
├── README.md                    ✅ Documentation
├── INSTALLATION.md              ✅ Guide installation
└── doc.md                       ℹ️ Documentation originale

```

## 🔄 Changements majeurs

### Avant (version réseau)

```
┌─────────────┐      HTTP      ┌──────────────────┐    Modbus    ┌──────────┐
│ Home        │ ──────────────→ │ Serveur Python   │ ───────────→ │ Automates│
│ Assistant   │ ← ─ ─ ─ ─ ─ ─ ─ │ (domotique_     │ ← ─ ─ ─ ─ ─ │ iSMART   │
└─────────────┘   JSON/REST     │  _unified.py)    │   RS485 RTU  └──────────┘
                                 └──────────────────┘
```

### Maintenant (version centralisée)

```
┌─────────────┐     Modbus RTU      ┌──────────┐
│ Home        │ ──────────────────→ │ Automates│
│ Assistant   │ ← ─ ─ ─ ─ ─ ─ ─ ─ ─ │ iSMART   │
└─────────────┘   RS485 /dev/ttyUSB0 └──────────┘
     ↓
modbus_interface.py
```

## 🚀 Prochaines étapes

### Installation

1. **Copier l'extension** dans Home Assistant :
   ```bash
   cp -r custom_components/ismart_modbus /config/custom_components/
   ```

2. **Ajouter permissions série** :
   ```bash
   sudo usermod -a -G dialout homeassistant
   ```

3. **Redémarrer Home Assistant**

4. **Configurer l'intégration** :
   - Configuration → Intégrations → + Ajouter
   - Chercher "iSMART Modbus"
   - Port série : `/dev/ttyUSB0`
   - Vitesse : `38400`
   - Timeout : `0.03`

### Vérification

Les 4 entités doivent apparaître :
- ✅ switch.gabriel_lumiere
- ✅ switch.gabriel_lit
- ✅ switch.gabriel_volet_up
- ✅ switch.gabriel_volet_down

## 💡 Avantages de la centralisation

| Avantage | Détails |
|----------|---------|
| **Simplicité** | Un seul composant au lieu de deux |
| **Performance** | Pas de latence HTTP intermédiaire |
| **Autonomie** | Plus besoin de serveur Python externe |
| **Maintenance** | Un seul code à maintenir |
| **Fiabilité** | Moins de points de défaillance |

## 🆚 Compatibilité

### Serveur Python (domotique_unified.py)

Le serveur Python n'est **plus nécessaire** pour l'extension, mais reste utilisable :

- **Interface web** (port 2081) : Toujours fonctionnelle
- **API REST** : Toujours accessible
- **TCP Legacy** (port 2080) : Toujours opérationnel

Vous pouvez :
- ✅ Garder le serveur pour l'interface web
- ✅ Utiliser l'extension ET le serveur en parallèle
- ⚠️ Attention : Un seul peut utiliser `/dev/ttyUSB0` à la fois

## 📝 Notes importantes

1. **Port série exclusif** : Soit l'extension, soit le serveur Python utilise `/dev/ttyUSB0`

2. **Choix d'architecture** :
   - Extension seule → Communication directe Modbus
   - Serveur + extension → Passer l'extension en mode réseau (ancien code)

3. **Évolution future** :
   - Coordinateur pour polling d'état
   - Support toutes les pièces
   - Entités cover/binary_sensor

## ✨ Résultat

🎯 **Extension 100% autonome et centralisée**

Toute la logique de communication Modbus est maintenant intégrée directement dans l'extension Home Assistant. Plus besoin de dépendances externes !

---

**Auteur** : Gabriel  
**Date** : 20 janvier 2026  
**Version** : 1.0.0 (centralisée)
