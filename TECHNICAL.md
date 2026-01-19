# Architecture technique - iSMART Modbus HA

## Fonctionnement général

L'intégration Home Assistant fonctionne selon ce flux:

```
Home Assistant
    │
    ├─ Utilisateur allume/éteint une lampe
    │
    ├─ Requête HTTP POST: GET /writeCoil[device,addr,1 ou 0]
    │     └─ Serveur Modbus exécute la commande
    │
    └─ Mise à jour périodique (toutes les 30s):
         └─ Requête HTTP: GET /getState
              └─ Analyse la réponse et met à jour l'état
```

## Fichiers et rôles

### `manifest.json`
Fichier de configuration du package Home Assistant:
- Déclare le domaine `ismart_modbus`
- Spécifie les dépendances (`aiohttp`)
- Défini la version minimale de Home Assistant

### `__init__.py`
Point d'entrée de l'intégration:
- Configure les plateformes (`light`)
- Gère le cycle de vie (setup, unload, reload)
- Stocke les données dans `hass.data`

### `config_flow.py`
Interface de configuration dans HA:
- **Étape 1** (`user`): Demande l'adresse et le port du serveur
- **Étape 2** (`lights`): Demande la liste des lampes en JSON
- Teste la connexion au serveur
- Validation du JSON

### `const.py`
Constantes de l'intégration:
- Noms de paramètres de configuration
- Valeurs par défaut
- Codes d'état des entités

### `light.py`
Implémentation de l'entité lumière:
- Classe `ISmartModbusLight` hérite de `LightEntity`
- Implémente les méthodes:
  - `async_turn_on()`: Envoyer writeCoil avec value=1
  - `async_turn_off()`: Envoyer writeCoil avec value=0
  - `async_update()`: Récupérer l'état avec getState

### `strings.json`
Textes et traductions pour l'interface:
- Descriptions des étapes de configuration
- Messages d'erreur
- Libellés des champs

## Protocol Modbus HTTP

### getState
```
GET http://192.168.1.11:2080/getState

Réponse exemple:
[1,1,1,1,1][0,0,0,0,0][2048,0,0,0,0]

Structure:
[validState0,validState1,...][outState0,outState1,...][memState0,memState1,...]
```

**Explication**:
- `validState[i]`: Indicateur que les données du device i sont valides
- `outState[i]`: État des sorties Q du device i (16 bits)
- `memState[i]`: État des variables mémoire Y/M du device i (16 bits)

### writeCoil
```
GET http://192.168.1.11:2080/writeCoil[device,addr,value]

Exemples:
- Allumer: /writeCoil[1,0x2C00,1]
- Éteindre: /writeCoil[1,0x2C00,0]
```

## Décodage de l'état

Pour un device/index donné:

1. **Vérifier la validité**
   ```python
   if validState[device-1] == 0:
       state = ERROR  # Données non valides
   ```

2. **Lire dans outState ou memState**
   ```python
   if index < 100:
       # Lire dans outState
       bit = (outState[device-1] >> index) & 0x1
   else:
       # Lire dans memState
       bit = (memState[device-1] >> (index-100)) & 0x1
   ```

3. **Interpréter le bit**
   ```python
   state = ON if bit == 1 else OFF
   ```

## Exemple complet

Pour la lampe "Arrosage auto":
```json
{"name": "Arrosage auto", "device": 5, "index": 109, "addr": "0x0549"}
```

Réponse getState:
```
[1,1,1,1,1][0,0,0,0,0][2048,0,0,0,0]
validState = [1,1,1,1,1]
outState = [0,0,0,0,0]
memState = [2048,0,0,0,0]
```

Décodage:
1. `validState[5-1]` = `validState[4]` = 1 ✓ Valide
2. `index` = 109 ≥ 100, donc lire dans memState
3. `memState[5-1]` = `memState[4]` = 2048 = 0x0800 = 0b100000000000
4. Bit à position 109-100=9: (2048 >> 9) & 0x1 = 1 ✓ Allumé

## Flux d'activation/désactivation

### Allumage (User clic on)
```
1. User clique sur la lampe dans Home Assistant
2. HA appelle async_turn_on()
3. Intégration envoie: GET /writeCoil[device,addr,1]
4. Serveur Modbus exécute la commande
5. Intégration met à jour l'état local
6. Interface HA se rafraîchit
7. À la mise à jour suivante, vérifie l'état via getState
```

### Mise à jour périodique
```
Chaque 30 secondes:
1. async_update() est appelé
2. Envoie GET /getState
3. Parse la réponse
4. Met à jour self._is_on pour chaque lampe
5. HA notifie les clients (interface, automations, etc.)
```

## Gestion des erreurs

L'intégration gère:

- **Erreur de connexion**: Définie `available = False`
- **Status HTTP != 200**: Log l'erreur, définie `available = False`
- **JSON invalide dans config**: Affiche erreur, demande nouvelle config
- **Données invalides de getState**: Définit état à ERROR

## Extendabilité

Pour ajouter de nouvelles fonctionnalités:

### Ajouter d'autres types d'appareils
1. Créer `switch.py` ou `climate.py`
2. Ajouter à `PLATFORMS` dans `__init__.py`
3. Implémenter les entités appropriées

### Ajouter la configuration des alarmes
1. Créer classe `AlarmEntity` dans `light.py`
2. Parser la configuration alarme
3. Implémenter les transitions d'état (Standby → Armée → Alarme)

### Ajouter les volets roulants
1. Créer `cover.py` pour les volets
2. Ajouter les états: Ouvert, Fermé, Ouverture, Fermeture
3. Implémenter les commandes up/down/stop

## Performance

- **Timeout HTTP**: 2 secondes par requête
- **Mise à jour**: Toutes les 30 secondes (configurable)
- **Session HTTP**: Réutilisée (efficace)
- **Parse JSON**: Optimisé pour peu de données

## Sécurité

⚠️ **Important**: Cette intégration utilise HTTP simple (pas de HTTPS).
Pour un usage en production:
1. Utilisez un reverse proxy avec HTTPS
2. Activez l'authentification
3. Restreignez l'accès réseau

## Debug

Pour voir les logs détaillés:

1. Allez à **Paramètres** → **Système** → **Journaux**
2. Entrez "ismart_modbus" dans le champ
3. Cliquez "Charger les journaux complets"
4. Attendez une action (allumer/éteindre)
5. Cliquez le bouton de rafraîchissement

Logs typiques:
```
2024-01-19 12:34:56 DEBUG (MainThread) [custom_components.ismart_modbus.light] Lumière Parents allumée
2024-01-19 12:34:56 DEBUG (MainThread) [custom_components.ismart_modbus.light] Lumière Parents: 1
```

---

Cette architecture rend facile:
- ✅ Configuration directe dans HA
- ✅ Installation via HACS
- ✅ Mise à jour automatique
- ✅ Évolution future (alarmes, volets, etc.)
