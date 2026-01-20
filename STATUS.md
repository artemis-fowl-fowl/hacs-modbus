# ✅ Extension iSMART Modbus - Complète et Fonctionnelle

## 🎉 Tout est prêt !

L'extension Home Assistant pour automates iSMART est **100% fonctionnelle** avec :

### ✅ Communication Modbus directe
- RS485 via `/dev/ttyUSB0` (38400 bauds)
- Protocole Modbus RTU natif (CRC16)
- Fonction 03H (lecture) + 05H (écriture)

### ✅ Retour d'état en temps réel
- **Coordinateur** avec polling toutes les 5 secondes
- Lecture automatique de l'état réel des automates
- Détection des changements manuels (interrupteurs physiques)
- Synchronisation parfaite HA ↔ Automates

### ✅ Gestion de disponibilité
- Détection automatique des automates hors ligne
- Entités marquées "unavailable" si automate défaillant
- Logs d'erreur détaillés

### ✅ Interface utilisateur
- Configuration via GUI (Configuration → Intégrations)
- 4 entités pour Gabriel (lumière, lit, volet up/down)
- Icônes adaptées (lightbulb, bed, window-shutter)
- État immédiat après commande

## 📁 Fichiers de l'extension (8 fichiers)

```
custom_components/ismart_modbus/
├── __init__.py              ✅ Init + coordinateur
├── config_flow.py           ✅ Wizard configuration
├── const.py                 ✅ Config série + devices
├── coordinator.py           ✅ Polling périodique (NOUVEAU)
├── manifest.json            ✅ Métadonnées
├── modbus_interface.py      ✅ Logique Modbus RTU
├── strings.json             ✅ Traductions FR
└── switch.py                ✅ Switches avec état (AMÉLIORÉ)
```

## 🚀 Installation

### 1. Copier l'extension
```bash
cp -r custom_components/ismart_modbus /config/custom_components/
```

### 2. Permissions série
```bash
sudo usermod -a -G dialout homeassistant
sudo systemctl restart home-assistant
```

### 3. Configuration dans HA
- Configuration → Intégrations → + Ajouter
- Chercher "iSMART Modbus"
- Port : `/dev/ttyUSB0`
- Vitesse : `38400`
- Timeout : `0.03`

### 4. Vérification
Les 4 entités apparaissent :
- ✅ `switch.gabriel_lumiere`
- ✅ `switch.gabriel_lit`
- ✅ `switch.gabriel_volet_up`
- ✅ `switch.gabriel_volet_down`

## 🔄 Fonctionnement du retour d'état

### Cycle de mise à jour (toutes les 5s)

```
Coordinateur → readstate() → 5 automates
     ↓
outvalid, outstate, memstate
     ↓
get_coil_state(device, coil) → bit extraction
     ↓
Switch.is_on → État affiché dans HA
```

### Après une commande

```
User clique switch → writecoil(1, 0x2C02, 1)
     ↓
Automate exécute
     ↓
async_request_refresh() → Lecture immédiate
     ↓
État mis à jour instantanément
```

## 📊 État actuel des fonctionnalités

| Fonctionnalité | État | Notes |
|----------------|------|-------|
| Communication RS485 | ✅ | Modbus RTU natif |
| Écriture bobines | ✅ | writecoil (05H) |
| Lecture registres | ✅ | readreg (03H) |
| **Retour d'état** | ✅ | **Polling 5s** |
| **Disponibilité** | ✅ | **Détection offline** |
| Configuration GUI | ✅ | Port/baudrate/timeout |
| Switches Gabriel | ✅ | 4 entités |
| Icônes adaptées | ✅ | lightbulb/bed/shutter |
| Logs debug | ✅ | Complets |
| Documentation | ✅ | README + guides |

## 🎯 Exemple d'utilisation

### Allumer la lumière Gabriel

**Dans Home Assistant** :
1. Cliquer sur `switch.gabriel_lumiere`
2. Extension envoie → `writecoil(slave=1, coil=0x2C02, value=1)`
3. Automate allume la lumière
4. Coordinateur rafraîchit → `readstate()`
5. État ON affiché **immédiatement**

**Avec interrupteur physique** :
1. Appui sur interrupteur mural
2. Automate change l'état
3. Coordinateur détecte le changement (dans les 5s)
4. État mis à jour automatiquement dans HA

## 📝 Comparaison avant/après

| Aspect | Avant (v1.0) | Maintenant (v1.1) |
|--------|-------------|-------------------|
| Communication | ✅ RS485 directe | ✅ RS485 directe |
| Commandes | ✅ writecoil | ✅ writecoil |
| Lecture d'état | ❌ Aucune | ✅ **Polling 5s** |
| État affiché | ❌ Optimiste | ✅ **État réel** |
| Changements manuels | ❌ Non détectés | ✅ **Détectés** |
| Disponibilité | ❌ Toujours "available" | ✅ **Détection offline** |
| Rafraîchissement | ❌ Manuel | ✅ **Automatique** |

## 🔧 Configuration avancée

### Modifier l'intervalle de polling

Éditer `coordinator.py` ligne 10 :
```python
SCAN_INTERVAL = timedelta(seconds=5)  # Changer ici
```

Recommandations :
- **5s** (défaut) : Bon compromis
- **2s** : Plus réactif, charge moyenne
- **10s** : Économie, moins réactif

### Activer logs détaillés

`configuration.yaml` :
```yaml
logger:
  logs:
    custom_components.ismart_modbus: debug
    custom_components.ismart_modbus.coordinator: debug
```

## 🐛 Dépannage

### Entités "unavailable"

**Cause** : Automate ne répond pas
**Solution** :
1. Vérifier câblage RS485
2. Tester avec `test_extension.py`
3. Consulter logs : `Echec lecture automate X`

### État ne se met pas à jour

**Cause** : Coordinateur ne tourne pas
**Solution** :
1. Vérifier logs : `Modbus state updated`
2. Redémarrer HA
3. Vérifier `/dev/ttyUSB0` libre

### Erreurs CRC

**Cause** : Problèmes communication
**Solution** :
1. Vérifier baudrate (38400)
2. Vérifier câble RS485
3. Réduire timeout si nécessaire

## 📚 Documentation

- [README.md](README.md) - Documentation principale
- [INSTALLATION.md](INSTALLATION.md) - Guide installation
- [MIGRATION.md](MIGRATION.md) - Migration réseau → série
- [RETOUR_ETAT.md](RETOUR_ETAT.md) - Détails retour d'état
- [STRUCTURE_FINALE.md](STRUCTURE_FINALE.md) - Structure projet

## ✨ Résumé final

### ✅ Ce qui fonctionne (TOUT !)

1. ✅ **Communication Modbus directe** via RS485
2. ✅ **Commandes** : Allumer/éteindre lumières et volets
3. ✅ **Retour d'état automatique** : Polling 5s
4. ✅ **Synchronisation parfaite** : HA ↔ Automates
5. ✅ **Détection changements manuels** : Interrupteurs physiques
6. ✅ **Gestion disponibilité** : Automates offline détectés
7. ✅ **Rafraîchissement immédiat** : Après chaque commande
8. ✅ **Interface GUI** : Configuration facile
9. ✅ **Logs complets** : Debug et info
10. ✅ **Documentation** : Complète et détaillée

### 🎯 Prêt pour production !

L'extension est **100% fonctionnelle** et prête à être utilisée en production. Tous les objectifs sont atteints :

- ✅ Communication directe sans serveur intermédiaire
- ✅ Retour d'état en temps réel
- ✅ Fiabilité et détection d'erreurs
- ✅ Documentation complète
- ✅ Code propre et maintenable

---

**Auteur** : Gabriel  
**Version** : 1.1.0 (avec retour d'état)  
**Date** : 20 janvier 2026  
**Statut** : ✅ **PRODUCTION READY**
