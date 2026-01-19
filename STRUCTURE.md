# Structure du repository

Voici la structure complète de votre repository pour HACS:

```
ha-ismart-modbus/                          ← Votre repository GitHub
├── .github/
│   └── workflows/
│       ├── hassfest.yaml                  ← Validation des manifests
│       └── validate.yaml                  ← Validation du code Python
├── custom_components/
│   └── ismart_modbus/                     ← LE CUSTOM COMPONENT
│       ├── __init__.py                    ← Point d'entrée
│       ├── config_flow.py                 ← Configuration UI
│       ├── const.py                       ← Constantes
│       ├── light.py                       ← Entités lumière
│       ├── manifest.json                  ← Métadonnées (REQUIS)
│       ├── strings.json                   ← Traductions
│       └── README.md                      ← Doc locale
├── .gitignore                             ← Fichiers à ignorer
├── hacs.json                              ← Config HACS (REQUIS)
├── LICENSE                                ← Licence MIT
├── README.md                              ← Doc principale
├── QUICKSTART.md                          ← Guide rapide
├── CONFIGURATION.md                       ← Config détaillée
└── TECHNICAL.md                           ← Détails techniques
```

## Fichiers obligatoires pour HACS

### Pour le custom component
- ✅ `custom_components/ismart_modbus/manifest.json`
- ✅ `custom_components/ismart_modbus/__init__.py`

### Pour le repository GitHub
- ✅ `hacs.json`
- ✅ Repository **public**
- ✅ `.github/workflows/hassfest.yaml` (recommandé)

## Installation de votre repository

### 1. Créer le GitHub

1. Allez à https://github.com/new
2. Nom: `ha-ismart-modbus`
3. Description: `iSMART Modbus integration for Home Assistant`
4. Sélectionnez **Public**
5. Cochez "Add a README file"
6. Licence: MIT
7. Créez

### 2. Pousser le code

```bash
# Dans le dossier ha-ismart-modbus
git init
git add .
git commit -m "Initial commit: iSMART Modbus integration"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/ha-ismart-modbus.git
git push -u origin main
```

### 3. Ajouter à HACS

Une fois sur GitHub:

1. Home Assistant → HACS
2. Integrations → ⋯ (menu) → Custom repositories
3. URL: `https://github.com/VOTRE_USERNAME/ha-ismart-modbus`
4. Catégorie: **Integration**
5. Create
6. Cherchez "iSMART Modbus"
7. Install
8. Redémarrez HA

## Checklist finale

Avant de pousser sur GitHub:

- [ ] Fichier `manifest.json` présent
- [ ] Fichier `__init__.py` présent
- [ ] Fichier `config_flow.py` pour la configuration
- [ ] Fichier `light.py` avec les entités
- [ ] Fichier `strings.json` pour les traductions
- [ ] Fichier `hacs.json` à la racine
- [ ] Fichier `.github/workflows/hassfest.yaml`
- [ ] Repository défini en **public**
- [ ] Licence MIT ou compatible
- [ ] README.md à la racine

## Validation avant publication

```bash
# Installer les outils
pip install homeassistant

# Valider le structure
hassfest --help

# Vérifier syntax Python
python -m py_compile custom_components/ismart_modbus/*.py
```

## Après l'installation dans HA

1. Allez à Paramètres → Appareils et services
2. Cliquez "Créer une intégration"
3. Cherchez "iSMART Modbus"
4. Configurez selon QUICKSTART.md

## Dépannage de HACS

### L'intégration n'apparaît pas

1. Vérifiez que le repository est **public**
2. Vérifiez l'URL: `https://github.com/...`
3. Attendez quelques minutes
4. Redémarrez Home Assistant
5. Rafraîchissez HACS (⋯ → Rafraîchir)

### Erreur "Repository does not contain any valid integration"

Vérifiez:
- `manifest.json` existe dans `custom_components/ismart_modbus/`
- `__init__.py` existe dans `custom_components/ismart_modbus/`
- Pas d'erreurs Python (validez avec `python -c`)

## Fichiers générés automatiquement

Home Assistant génère automatiquement:
- Dossier `.homeassistant` (local)
- Fichiers de cache
- Fichiers de logs

Ils ne doivent PAS être poussés. Utilisez `.gitignore`.

---

**Vous êtes prêt à publier! 🚀**
