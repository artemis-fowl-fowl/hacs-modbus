# Guide d'installation rapide - iSMART Modbus HA

## 🚀 Installation via HACS (5 minutes)

### 1️⃣ Créer le repository GitHub

Avant tout, créez un repository GitHub avec la structure de ce dossier:
- Nom recommandé: `ha-ismart-modbus`
- Visibilité: **Public** (obligatoire pour HACS)
- Contenu: Copiez tous les fichiers de ce dossier

### 2️⃣ Ajouter à HACS

Dans Home Assistant:

1. Allez à **HACS** (en bas à gauche)
2. Cliquez sur **Integrations**
3. Cliquez sur **⋯** (3 points) en haut à droite
4. Sélectionnez **Custom repositories**
5. Collez votre URL GitHub (ex: `https://github.com/VOTRE_USER/ha-ismart-modbus`)
6. Sélectionnez **Integration** comme catégorie
7. Cliquez **Create**
8. Trouvez **iSMART Modbus** et cliquez **Install**
9. **Redémarrez** Home Assistant

### 3️⃣ Configurer dans Home Assistant

Une fois redémarré:

1. Allez à **Paramètres** → **Appareils et services**
2. Cliquez **Créer une intégration** (en bas à droite)
3. Cherchez **iSMART Modbus**
4. Entrez:
   - **Adresse**: `192.168.1.11` (votre serveur)
   - **Port**: `2080`
5. Cliquez **Suivant**
6. Entrez vos lampes en JSON (voir ci-dessous)
7. Cliquez **Créer**

## 📝 Configuration des lampes (JSON)

### Format simple

Chaque lampe nécessite:
- `name`: Nom dans Home Assistant
- `device`: Numéro du device (1-5)
- `index`: Index de la sortie
- `addr`: Adresse hexadécimale

### Exemple minimal

```json
[
  {"name": "Salon", "device": 2, "index": 0, "addr": "0x2C00"},
  {"name": "Cuisine", "device": 2, "index": 2, "addr": "0x2C02"}
]
```

### Exemple complet (vos lampes)

Voici tous vos points lumineux depuis `scripts.js`:

```json
[
  {"name": "Parents", "device": 1, "index": 0, "addr": "0x2C00"},
  {"name": "Dressing", "device": 1, "index": 1, "addr": "0x2C01"},
  {"name": "Gabriel", "device": 1, "index": 2, "addr": "0x2C02"},
  {"name": "Paul", "device": 1, "index": 3, "addr": "0x2C03"},
  {"name": "Sophie", "device": 1, "index": 4, "addr": "0x2C04"},
  {"name": "SDB", "device": 1, "index": 5, "addr": "0x2C05"},
  {"name": "Miroir SDB", "device": 1, "index": 6, "addr": "0x2C06"},
  {"name": "Douche", "device": 1, "index": 7, "addr": "0x2C07"},
  {"name": "Grenier", "device": 1, "index": 8, "addr": "0x2C10"},
  {"name": "Couloir", "device": 1, "index": 9, "addr": "0x2C11"},
  {"name": "Mezzanine", "device": 1, "index": 10, "addr": "0x2C12"},
  {"name": "Sejour", "device": 1, "index": 11, "addr": "0x2C13"},
  {"name": "Passerelle", "device": 1, "index": 12, "addr": "0x2C14"},
  {"name": "Cabanon", "device": 1, "index": 13, "addr": "0x2C15"},
  {"name": "SDJ", "device": 1, "index": 14, "addr": "0x2C16"},
  {"name": "WC Etage", "device": 1, "index": 15, "addr": "0x2C17"},
  {"name": "Salon 1", "device": 2, "index": 0, "addr": "0x2C00"},
  {"name": "Salon 2", "device": 2, "index": 1, "addr": "0x2C01"},
  {"name": "Cuisine", "device": 2, "index": 2, "addr": "0x2C02"},
  {"name": "Ilot", "device": 2, "index": 3, "addr": "0x2C03"},
  {"name": "Evier", "device": 2, "index": 4, "addr": "0x2C04"},
  {"name": "Terrasse", "device": 2, "index": 5, "addr": "0x2C05"},
  {"name": "Buanderie", "device": 2, "index": 6, "addr": "0x2C06"},
  {"name": "Miroir RDC", "device": 2, "index": 7, "addr": "0x2C07"},
  {"name": "WC RDC", "device": 2, "index": 8, "addr": "0x2C10"},
  {"name": "Hall", "device": 2, "index": 9, "addr": "0x2C11"},
  {"name": "Cellier", "device": 2, "index": 10, "addr": "0x2C12"},
  {"name": "Atelier", "device": 2, "index": 11, "addr": "0x2C13"},
  {"name": "Preau", "device": 2, "index": 12, "addr": "0x2C14"},
  {"name": "Garage", "device": 2, "index": 13, "addr": "0x2C15"},
  {"name": "Cave", "device": 2, "index": 14, "addr": "0x2C16"},
  {"name": "Cour", "device": 2, "index": 15, "addr": "0x2C17"},
  {"name": "Lit Aurel", "device": 3, "index": 14, "addr": "0x2C16"},
  {"name": "Lit Aline", "device": 3, "index": 15, "addr": "0x2C17"},
  {"name": "Sejour.A", "device": 4, "index": 10, "addr": "0x2C12"},
  {"name": "Sejour.B", "device": 4, "index": 11, "addr": "0x2C13"},
  {"name": "Lit Gabriel", "device": 4, "index": 12, "addr": "0x2C14"},
  {"name": "Lit Paul", "device": 4, "index": 13, "addr": "0x2C15"},
  {"name": "Lit Sophie", "device": 4, "index": 14, "addr": "0x2C16"},
  {"name": "RadSDB", "device": 5, "index": 6, "addr": "0x2C06"},
  {"name": "Salon.A", "device": 5, "index": 0, "addr": "0x2C00"},
  {"name": "Ampli", "device": 5, "index": 1, "addr": "0x2C01"},
  {"name": "Arrosage Zone 1", "device": 5, "index": 2, "addr": "0x2C02"},
  {"name": "Arrosage Zone 2", "device": 5, "index": 3, "addr": "0x2C03"},
  {"name": "Prise charge Scooter", "device": 5, "index": 107, "addr": "0x0547"},
  {"name": "Borne charge VE", "device": 5, "index": 108, "addr": "0x0548"},
  {"name": "Arrosage auto", "device": 5, "index": 109, "addr": "0x0549"}
]
```

## ✅ Vérification

Une fois configuré:

1. Allez à **Tableau de bord** → **Ajuster le tableau**
2. Cliquez **Créer une nouvelle carte**
3. Cherchez "Entités"
4. Sélectionnez vos lumières iSMART
5. Elles devraient apparaître!

## 🐛 Dépannage

### L'intégration n'apparaît pas dans l'UI

1. Allez à **Paramètres** → **Système** → **Journaux**
2. Cherchez "ismart" et "modbus"
3. Vérifiez les erreurs

### Les lampes n'allument pas

1. Testez votre serveur: `http://192.168.1.11:2080/getState`
2. Vérifiez dans les logs de Home Assistant
3. Assurez-vous que le serveur répond

### Configuration invalide

Le JSON doit être parfait. Utilisez: https://jsonlint.com pour valider

## 📚 Documentation complète

- Voir [CONFIGURATION.md](CONFIGURATION.md) pour la configuration avancée
- Voir [README.md](README.md) pour les détails techniques

## 🤝 Support

- Les logs: **Paramètres** → **Système** → **Journaux**
- Cherchez "ismart_modbus" dans les logs

---

**C'est tout! Vos lampes devraient maintenant être contrôlables depuis Home Assistant! 🎉**
