# Diagramme d'intégration iSMART Modbus

## Flux global

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOME ASSISTANT                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Interface utilisateur                                   │  │
│  │  - Tableau de bord avec lumières                         │  │
│  │  - Paramètres → Appareils et services                    │  │
│  │  - Automation et scripts                                 │  │
│  └─────────────────────────┬────────────────────────────────┘  │
│                            │                                    │
│  ┌─────────────────────────▼────────────────────────────────┐  │
│  │  iSMART Modbus Integration (custom_components)           │  │
│  │                                                           │  │
│  │  ┌───────────────────────────────────────────────────┐  │  │
│  │  │ __init__.py                                       │  │  │
│  │  │ - Initialisation de l'intégration                │  │  │
│  │  │ - Gestion du cycle de vie                        │  │  │
│  │  └───────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  ┌───────────────────────────────────────────────────┐  │  │
│  │  │ config_flow.py                                    │  │  │
│  │  │ - Étape 1: Configuration serveur (IP/port)       │  │  │
│  │  │ - Étape 2: Configuration lampes (JSON)           │  │  │
│  │  │ - Validation et test de connexion                │  │  │
│  │  └───────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  ┌───────────────────────────────────────────────────┐  │  │
│  │  │ light.py → ISmartModbusLight                      │  │  │
│  │  │                                                    │  │  │
│  │  │  Pour chaque lampe configurée:                   │  │  │
│  │  │  ├─ async_turn_on()  → /writeCoil[d,a,1]        │  │  │
│  │  │  ├─ async_turn_off() → /writeCoil[d,a,0]        │  │  │
│  │  │  └─ async_update()   → /getState                │  │  │
│  │  └───────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  └──────────────────────────────┬──────────────────────────┘  │
│                                 │                              │
└─────────────────────────────────┼──────────────────────────────┘
                                  │ HTTP (aiohttp)
                                  │
┌─────────────────────────────────▼──────────────────────────────┐
│                 SERVEUR MODBUS iSMART                          │
│              192.168.1.11:2080                                 │
│                                                                 │
│  Endpoints HTTP:                                              │
│  - GET /getState                                              │
│    Response: [validState][outState][memState]                 │
│                                                                 │
│  - GET /writeCoil[device,addr,value]                          │
│    Response: OK ou erreur                                     │
│                                                                 │
└─────────────────────────────────┬──────────────────────────────┘
                                  │
                        ┌─────────▼──────────┐
                        │ Automates Modbus   │
                        │ (Device 1-5)       │
                        │ Sorties Q/Y        │
                        │ Variables M        │
                        └────────────────────┘
```

## Architecture des données

```
Réponse getState:
┌────────────────────────────────────────────────────┐
│ [validState0,validState1,validState2,...]          │
│ [outState0,outState1,outState2,...]                │
│ [memState0,memState1,memState2,...]                │
└────────────────────────────────────────────────────┘
       │              │              │
       │              │              └─ Variables M (bits 0-15)
       │              └─ Sorties Q (bits 0-15)
       └─ Indicateurs de validité

Par device:
Device 1: bits 0-15 pour Q0-Q15
Device 2: bits 16-31 pour Q0-Q15
...
Device 5: bits 64-79 pour Q0-Q15
```

## Flux de commande - Allumer une lampe

```
1. Utilisateur clique sur la lampe
   │
   ▼
2. Home Assistant appelle async_turn_on()
   │
   ▼
3. ISmartModbusLight envoie:
   GET http://192.168.1.11:2080/writeCoil[device,addr,1]
   │
   ▼
4. Serveur reçoit et exécute
   │
   ▼
5. Intégration reçoit réponse HTTP 200
   │
   ▼
6. Mise à jour locale: self._is_on = True
   │
   ▼
7. Home Assistant notifie l'interface
   │
   ▼
8. Lampe s'affiche allumée dans HA
   │
   ▼
9. À la mise à jour périodique:
   - getState récupère l'état réel du serveur
   - Vérifie que la lampe est bien allumée
   - Synchronise avec l'interface
```

## Flux de mise à jour d'état

```
┌──────────────────────────┐
│ Toutes les 30 secondes   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ light.py: async_update()                     │
│ Pour chaque lampe configurée                 │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ GET /getState                                │
│ Response: [validState][outState][memState]   │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ _parse_state()                               │
│ 1. Extraire device-1 de validState           │
│ 2. Si invalide → ERROR                       │
│ 3. Si index < 100 → lire dans outState       │
│ 4. Si index >= 100 → lire dans memState      │
│ 5. Extraire le bit approprié                 │
│ 6. Convertir: 0→OFF, 1→ON                    │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ Mettre à jour self._is_on                    │
│ Home Assistant notifie les changements       │
└──────────────────────────────────────────────┘
```

## Structure des classes

```
LightEntity (Home Assistant)
    │
    ▼
ISmartModbusLight
├─ __init__(hass, host, port, name, device, index, addr)
│  ├─ self._host: str
│  ├─ self._port: int
│  ├─ self._device: int (1-5)
│  ├─ self._index: int (0-15 ou 100+)
│  ├─ self._addr: str (0x2C00)
│  ├─ self._is_on: bool
│  ├─ self._available: bool
│  └─ self._attr_unique_id: str
│
├─ async_turn_on(): None
│  └─ Envoyer /writeCoil[device,addr,1]
│
├─ async_turn_off(): None
│  └─ Envoyer /writeCoil[device,addr,0]
│
├─ async_update(): None
│  ├─ Envoyer /getState
│  └─ Appeler _parse_state(data)
│
├─ _parse_state(data: str): None
│  ├─ Parser la réponse
│  ├─ Extraire validState, outState, memState
│  ├─ Décoder le bit selon index
│  └─ Mettre à jour self._is_on
│
├─ @property is_on: bool
│  └─ Retourner self._is_on
│
└─ @property available: bool
   └─ Retourner self._available
```

## Gestion des états

```
                    ┌─────────────────┐
                    │   UNKNOWN       │
                    │ (initial)       │
                    └────────┬────────┘
                             │
                   ┌─────────┼─────────┐
                   │                   │
                   ▼                   ▼
            ┌──────────────┐   ┌──────────────┐
            │     OFF      │   │      ON      │
            │              │   │              │
            │ Lampe        │   │ Lampe        │
            │ éteinte      │   │ allumée      │
            └──────┬───────┘   └───────┬──────┘
                   │                   │
                   └─────────┬─────────┘
                             │
                            ▼
                    ┌─────────────────┐
                    │      ERROR      │
                    │ Serveur ne      │
                    │ répond pas      │
                    └─────────────────┘
```

## Flux de configuration

```
User clique "Créer intégration"
        │
        ▼
config_flow.py: async_step_user()
├─ Demande: Serveur (IP + Port)
├─ Test de connexion avec /getState
└─ Si OK → async_step_lights()
        │
        ▼
async_step_lights()
├─ Demande: Configuration lampes (JSON)
├─ Parse et valide le JSON
└─ async_create_entry() → Enregistre la config
        │
        ▼
__init__.py: async_setup_entry()
├─ Récupère les données de config
├─ Crée les entités LightEntity
└─ Ajoute au Home Assistant
        │
        ▼
Les lampes apparaissent dans HA! ✨
```

---

Cette architecture permet:
- ✅ Configuration facile et intuitive
- ✅ Mise à jour périodique automatique
- ✅ Gestion des erreurs robuste
- ✅ Extensibilité pour d'autres appareils
- ✅ Performance optimale
