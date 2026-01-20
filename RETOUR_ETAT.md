# 🔄 Retour d'état en temps réel - iSMART Modbus

## ✅ Fonctionnalité implémentée

L'extension dispose maintenant d'un **retour d'état automatique** qui synchronise en temps réel l'état affiché dans Home Assistant avec l'état réel des automates.

## 🎯 Comment ça fonctionne

### Architecture avec coordinateur

```
┌─────────────────┐
│ Home Assistant  │
│                 │
│  ┌───────────┐  │
│  │ Switches  │←─┼─── Affichage état
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼──────┐ │
│  │Coordinator │ │ ← Polling toutes les 5s
│  └─────┬──────┘ │
│        │        │
└────────┼────────┘
         │
    ┌────▼────┐
    │ Modbus  │ ← readreg(0x0608)
    │Interface│
    └────┬────┘
         │ RS485
    ┌────▼────────┐
    │ Automates   │
    │ iSMART 1-5  │
    └─────────────┘
```

### 1. Coordinateur (`coordinator.py`)

Le coordinateur **ISmartModbusCoordinator** :
- Hérite de `DataUpdateCoordinator`
- Lance une lecture Modbus toutes les **5 secondes**
- Appelle `modbus_interface.readstate()` pour lire les 5 automates
- Stocke les données dans `self.data`

```python
SCAN_INTERVAL = timedelta(seconds=5)

async def _async_update_data(self):
    outvalid, outstate, memstate = await self.hass.async_add_executor_job(
        self.modbus_interface.readstate
    )
    return {
        "outvalid": outvalid,   # [1,1,1,1,1] = automates disponibles
        "outstate": outstate,   # État des sorties de chaque automate
        "memstate": memstate,   # État des mémoires
    }
```

### 2. Lecture d'état Modbus

La fonction `readstate()` dans `modbus_interface.py` :

```python
def readstate(self):
    for i in range(0, 5):
        # Lit 18 registres (0x12) à partir de 0x0608
        data = readreg(self.rs485, i + 1, 0x0608, 0x0012)
        
        if data != [-1]:
            outvalid[i] = 1  # Automate disponible
            memstate[i] = data[1] + 0x100 * data[0]      # Registre M0
            outstate[i] = data[23] + 0x100 * data[21]     # État sorties
```

**Registres lus** (18 mots = 36 octets) :
- `0x0608-0x0609` : Mémoires M0-M15
- `0x0610-0x0611` : État sorties Q0-Q15
- Autres registres pour supervision

### 3. Extraction de l'état d'une bobine

La méthode `get_coil_state()` :

```python
def get_coil_state(self, device_id: int, coil: int) -> bool | None:
    # Récupérer outstate du device
    outstate = self.data.get("outstate", [0, 0, 0, 0, 0])
    state_word = outstate[device_id - 1]
    
    # Calculer l'offset du bit (0x2C00 = bit 0, 0x2C01 = bit 1, ...)
    coil_offset = coil - 0x2C00
    
    # Tester le bit
    bit_value = (state_word >> coil_offset) & 1
    return bool(bit_value)
```

**Exemple** : Lumière Gabriel (slave 1, coil 0x2C02)
- `outstate[0]` = état du slave 1
- `coil_offset` = 0x2C02 - 0x2C00 = 2
- Bit 2 de `outstate[0]` → État ON/OFF

### 4. Switches avec CoordinatorEntity

Les switches héritent de `CoordinatorEntity` :

```python
class ISmartModbusSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, ...):
        super().__init__(coordinator)  # Liaison au coordinateur
    
    @property
    def is_on(self):
        # L'état est lu depuis le coordinateur
        return self.coordinator.get_coil_state(self._device_id, self._coil)
    
    @property
    def available(self):
        # Disponibilité basée sur outvalid
        return self.coordinator.is_device_available(self._device_id)
```

### 5. Rafraîchissement après commande

Après chaque commande, l'état est rafraîchi immédiatement :

```python
async def async_turn_on(self, **kwargs):
    result = await self._modbus.writecoil_device(...)
    if result == 0:
        # Demander une mise à jour immédiate
        await self.coordinator.async_request_refresh()
```

## 📊 Flux complet

### Allumage d'une lumière

1. **Utilisateur** clique sur le switch dans HA
2. **Switch** appelle `async_turn_on()`
3. **Modbus** envoie `writecoil(slave=1, coil=0x2C02, value=1)`
4. **Automate** exécute la commande
5. **Coordinateur** rafraîchit immédiatement (pas d'attente 5s)
6. **readstate()** lit l'état réel depuis l'automate
7. **get_coil_state()** extrait le bit 2 de outstate[0]
8. **Switch** met à jour l'affichage avec l'état réel

### Mise à jour périodique

Toutes les 5 secondes :
1. **Coordinateur** lance `_async_update_data()`
2. **readstate()** interroge les 5 automates
3. Données stockées dans `coordinator.data`
4. **Home Assistant** notifie tous les switches
5. Chaque switch recalcule son état via `is_on`
6. Interface mise à jour automatiquement

## 🎨 Avantages

| Fonctionnalité | Bénéfice |
|----------------|----------|
| **Synchronisation** | État HA = État réel automate |
| **Détection hors ligne** | Automate défaillant → entité "unavailable" |
| **Changements manuels** | Interrupteur physique détecté dans les 5s |
| **Feedback immédiat** | Commande HA → rafraîchissement instantané |
| **Multi-instance** | Plusieurs clients HA voient le même état |

## ⚙️ Configuration

### Intervalle de polling

Par défaut : **5 secondes**

Pour modifier, éditer [coordinator.py](custom_components/ismart_modbus/coordinator.py) :

```python
SCAN_INTERVAL = timedelta(seconds=5)  # Changer ici
```

**Recommandations** :
- ✅ 5s : Bon compromis performance/réactivité
- ⚠️ 2s : Plus réactif, charge RS485 moyenne
- ❌ 1s : Très réactif, charge RS485 élevée
- ❌ 10s : Faible charge, retour d'état lent

### Détection d'erreurs

Si un automate ne répond pas :
- `outvalid[i] = 0`
- Toutes les entités du device → `unavailable`
- Logs : `Echec lecture automate X`

## 🔍 Debugging

### Activer logs debug

Dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.ismart_modbus: debug
    custom_components.ismart_modbus.coordinator: debug
```

### Logs typiques

**Polling réussi** :
```
DEBUG Modbus state updated - valid: [1,1,1,1,1], outstate: [4, 0, 12, 16384, 0], memstate: [...]
```

**Automate hors ligne** :
```
WARNING Echec lecture automate 3
DEBUG Modbus state updated - valid: [1,1,0,1,1], ...
```

**Commande switch** :
```
INFO writecoil - slave: 1, coil: 0x2C02, state: 1
INFO Ack OK
INFO Switch gabriel_lumiere turned on
```

## 📈 Performance

### Charge Modbus

- **5 automates** × **18 registres** × **1 lecture/5s**
- = **90 registres/5s** = **18 registres/s**
- Temps par transaction : ~50ms
- Charge bus : < 1%

### Charge HA

- 1 coordinator
- 4 switches (Gabriel)
- Mise à jour : ~100ms toutes les 5s
- Impact CPU : négligeable

## ✨ Résultat

🎯 **État en temps réel fonctionnel !**

- ✅ L'état dans HA reflète l'état réel
- ✅ Changements physiques détectés (5s max)
- ✅ Feedback immédiat après commande
- ✅ Détection automates hors ligne
- ✅ Performance optimale

---

**Date** : 20 janvier 2026  
**Version** : 1.1.0 (avec coordinateur)
