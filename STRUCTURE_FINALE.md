# 📁 Structure finale du projet iSMART Modbus

## ✅ Structure nettoyée et organisée

```
hacsextnesin/
│
├── 📂 custom_components/           # Extension Home Assistant (PRINCIPALE)
│   └── ismart_modbus/
│       ├── __init__.py            # Initialisation + connexion Modbus
│       ├── config_flow.py         # Wizard de configuration
│       ├── const.py               # Constantes (port série, devices)
│       ├── manifest.json          # Métadonnées (pyserial>=3.5)
│       ├── modbus_interface.py    # ⭐ Logique Modbus RTU complète
│       ├── strings.json           # Traductions françaises
│       └── switch.py              # Entités switch
│
├── 📂 python/                      # Scripts Python (référence/optionnel)
│   ├── domotique_unified.py      # Serveur Python complet (ports 2080/2081)
│   ├── modbus2TCP_new.py         # Bridge Modbus → TCP
│   ├── doc.md                    # Documentation du serveur
│   └── [autres scripts...]       # Scripts originaux
│
├── 📂 .github/                     # Configuration GitHub
│
├── 📄 README.md                    # Documentation principale
├── 📄 INSTALLATION.md              # Guide d'installation
├── 📄 MIGRATION.md                 # Explication de la migration
├── 📄 test_extension.py            # Script de test
├── 📄 hacs.json                    # Configuration HACS
├── 📄 LICENSE                      # Licence MIT
└── 📄 .gitignore                   # Fichiers ignorés par Git
```

## 🎯 Fichiers principaux

### Extension (à installer dans HA)

**`custom_components/ismart_modbus/`** - Tous les fichiers nécessaires pour l'intégration

- **7 fichiers** au total
- **Autonome** : ne dépend d'aucun autre fichier du projet
- **Communication directe** : RS485 via pyserial

### Documentation

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation complète utilisateur |
| `INSTALLATION.md` | Guide pas à pas pour installer |
| `MIGRATION.md` | Explication de la centralisation |

### Scripts Python (optionnels)

Le dossier `python/` contient :
- Le serveur Python original (`domotique_unified.py`)
- Les scripts de référence
- **Non requis pour l'extension**

### Fichiers de test

- `test_extension.py` : Tester la communication Modbus avant installation

## 📦 Installation de l'extension

**Copier uniquement** :
```bash
cp -r custom_components/ismart_modbus /config/custom_components/
```

Tout le reste est **documentation ou référence**.

## 🗑️ Fichiers supprimés

Les fichiers suivants ont été supprimés car obsolètes :

- ❌ `ha_integration/` (doublon)
- ❌ `00_LISEZ_MOI_D_ABORD.md`
- ❌ `ARCHITECTURE.md`
- ❌ `CONFIGURATION.md`
- ❌ `EXEMPLE_VISUEL.md`
- ❌ `FINALRESUME.md`
- ❌ `LISEZMOI.txt`
- ❌ `QUICKSTART.md`
- ❌ `README_old.md`
- ❌ `RESUME.md`
- ❌ `STRUCTURE.md`
- ❌ `TECHNICAL.md`
- ❌ `scripts.js`
- ❌ `example_config.json`

## ✨ Structure optimale

**7 fichiers essentiels** dans `custom_components/ismart_modbus/`
**3 fichiers de documentation** à la racine
**1 script de test** pour valider avant installation

Total : **Structure propre et minimaliste** 🎉

---

**Date de nettoyage** : 20 janvier 2026
