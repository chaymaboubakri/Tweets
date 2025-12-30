
# Pipeline Data – Détection de Cyberharcèlement

**Projet réalisé par : Chayma Boubakri**

---

## 1. Objectif du projet

Ce projet a pour objectif de créer un **pipeline de données complet** pour analyser des tweets liés au cyberharcèlement :

1. **Ingestion** du dataset CSV
2. **Nettoyage** des tweets
3. **Stockage** dans MongoDB local
4. **Exposition** via une API REST FastAPI
5. **Orchestration** avec Airflow
6. **Vérification des données avec ** `check_data.py`

---

## 2. Architecture du projet

```
cyberbullying_pipeline/
│
├── venv/                  # Environnement virtuel Python
├── data/                  # Dossier contenant le dataset
│   └── cyberbullying_tweets.csv
├── data_processing.py     # Script de nettoyage et insertion MongoDB
├── main.py                # API FastAPI
├── check_data.py          # Vérification des données dans MongoDB
├── dag.py                 # DAG Airflow (optionnel)
├── requirements.txt       # Dépendances Python
└── README.md
```

---

## 3. Pré-requis et installation

### 3.1 Installer Python 3.9+

```bash
python --version
```

### 3.2 Créer et activer l'environnement virtuel

```bash
python -m venv venv
```

Activation :

- **Windows** : `venv\Scripts\activate`
- **Linux / macOS** : `source venv/bin/activate`

### 3.3 Installer MongoDB local

- Suivre la documentation officielle : [https://www.mongodb.com/docs/manual/installation/](https://www.mongodb.com/docs/manual/installation/)  
- Démarrer le serveur MongoDB : `mongod`

### 3.4 Installer les dépendances

Créer `requirements.txt` :

```txt
pandas
pymongo
fastapi
uvicorn
apache-airflow
```

Installation :

```bash
pip install -r requirements.txt
```

---

## 4. Fichiers créés et rôle

| Fichier | Description |
|---------|------------|
| `data_processing.py` | Lecture CSV, nettoyage des tweets, ajout `tweet_id` et `tweet_length`, insertion MongoDB |
| `main.py` | API REST FastAPI pour exposer les tweets et statistiques |
| `check_data.py` | Vérification rapide des données insérées dans MongoDB |
| `dag.py` | DAG Airflow pour automatiser le pipeline |
| `requirements.txt` | Liste des dépendances Python |
| `data/` | Contient le fichier `cyberbullying_tweets.csv` |
| `README.md` | Documentation complète du projet |

---

## 5. Traitement des données – `data_processing.py`

### 5.1 Exécuter le script

```bash
python data_processing.py
```

### 5.2 Résultat attendu

- Message terminal : `Données nettoyées et insérées avec succès.`
- MongoDB local contient la base `harassment_db` et la collection `tweets`
- Chaque document possède :

```json
{
  "tweet_id": "uuid...",
  "cleaned_tweet_text": "tweet nettoyé",
  "cyberbullying_type": "gender",
  "tweet_length": 42,
  "ingestion_date": "2025-..."
}
```

---

## 6. Vérification des données – `check_data.py`

### 6.1 Exécuter

```bash
python check_data.py
```

### 6.2 Ce que ça vérifie

- Nombre total de tweets insérés
- Affiche les 5 premiers tweets pour inspection
- Vérifie l’absence de mentions `@` ou URLs

---

## 7. API REST – `main.py`

### 7.1 Lancer l’API

```bash
uvicorn main:app --reload
```

### 7.2 Endpoints disponibles

| Endpoint | Description | Exemple |
|----------|------------|--------|
| `/` | Message d’accueil | `Bienvenue dans l'API de détection de harcèlement !` |
| `/tweets?skip=0&limit=10` | Tweets paginés | Liste de tweets nettoyés |
| `/stats` | Statistiques globales | Nombre total, répartition par type, longueur moyenne |

### 7.3 Test via Swagger

- URL : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Interface interactive pour tester tous les endpoints
- Vérification visuelle et fonctionnelle simple

---

## 8. Airflow – Orchestration (`dag.py`)

### 8.1 Initialiser Airflow

```bash
airflow db init
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@test.com
```

### 8.2 Lancer Airflow

```bash
airflow webserver
airflow scheduler
```

- Accéder à : [http://localhost:8080](http://localhost:8080)
- Activer le DAG `simple_harassment_pipeline`
- Cliquer sur **Trigger DAG**
- Vérifier que la tâche `clean_and_load` est **SUCCESS**

---

## 9. Test complet du projet

1. Exécuter le script de nettoyage :

```bash
python data_processing.py
```

2. Vérifier les données via `check_data.py` :

```bash
python check_data.py
```

3. Lancer l’API FastAPI :

```bash
uvicorn main:app --reload
```

4. Tester les endpoints et Swagger :

- `/tweets`
- `/stats`

5. Déclencher le DAG Airflow et vérifier succès

---

## 10. Résultat attendu

- Tweets nettoyés et insérés dans MongoDB
- API fonctionnelle avec pagination et statistiques
- Swagger montre tous les endpoints
- DAG Airflow orchestre le pipeline avec succès

---

## 11. Commandes résumé

| Étape | Commande |
|-------|---------|
| Activer venv | `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (Linux/macOS)` |
| Installer dépendances | `pip install -r requirements.txt` |
| Lancer script nettoyage | `python data_processing.py` |
| Vérifier données | `python check_data.py` |
| Lancer API | `uvicorn main:app --reload` |
| Accéder Swagger | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| Lancer Airflow | `airflow webserver` + `airflow scheduler` |
| Déclencher DAG | UI Airflow → Trigger DAG |

---

**Rédigé par : Chayma Boubakri**
