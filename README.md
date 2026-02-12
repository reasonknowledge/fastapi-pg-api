# FastAPI PostgreSQL API - Gestion École

API RESTful avec FastAPI, SQLModel et PostgreSQL pour la gestion des administrateurs et étudiants. Authentification JWT.

## Prérequis

Avant de commencer, assure-toi d'avoir installé :

- **Python 3.10+** - Le langage de programmation ([télécharger ici](https://www.python.org/downloads/))
- **Git** - Pour cloner le repository ([télécharger ici](https://git-scm.com/downloads))
- **PostgreSQL 13+** OU **Docker Desktop** - La base de données
  - Option A : [Télécharger PostgreSQL](https://www.postgresql.org/download/)
  - Option B : [Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop/) (plus simple pour débutants)
- **Node.js** (optionnel, si tu veux tester avec un frontend) ([télécharger ici](https://nodejs.org/))
- **Un navigateur web** (Chrome, Firefox, Edge, etc.)
- **pip** - Généralement installé avec Python (gestionnaire de paquets Python)

## Installation

### 1. Cloner le repository avec Git

Ouvre un terminal (Invite de commandes sur Windows, Terminal sur Mac/Linux) et tape :

```bash
git clone fastapi-
cd fastapi-pg-api
```

**Pour un débutant :** 
- Le terminal se trouve dans : Menu Démarrer > Tape "cmd" > Invite de commandes
- La commande `git clone` télécharge le projet sur ton ordinateur
- La commande `cd` te place dans le dossier du projet

### 2. Créer un environnement virtuel Python

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate

# Sur Linux/Mac :
source venv/bin/activate
```

**Pour un débutant :** L'environnement virtuel isole les dépendances de ce projet pour éviter les conflits avec d'autres projets Python.

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Pour un débutant :** Cette commande installe automatiquement toutes les bibliothèques nécessaires (FastAPI, SQLModel, PostgreSQL async, JWT, etc.).

### 4. Configurer la base de données PostgreSQL

Tu as **deux options** pour la base de données :

#### Option A : Avec Docker (Recommandé pour débutants)

Si tu as installé Docker Desktop :

```bash
# Démarrer PostgreSQL dans un conteneur Docker
docker-compose up -d
```

**Pour un débutant :** 
- Cette commande télécharge et démarre automatiquement PostgreSQL
- La base de données sera accessible sur `localhost:5432`
- Utilisateur : `postgres` | Mot de passe : `postgres` | Database : `school_db`

Pour arrêter la base de données plus tard :
```bash
docker-compose down
```

#### Option B : PostgreSQL local installé

1. Ouvre pgAdmin (fourni avec PostgreSQL) ou utilise la ligne de commande
2. Crée une base de données nommée `fastapisqlmodelpostgres`
3. Crée un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql+asyncpg://postgres:ton_mot_de_passe@localhost:5432/fastapisqlmodelpostgres
JWT_SECRET_KEY=ta_cle_secrete_jwt_super_longue_et_aleatoire
FRONTEND_URL=http://localhost:5173
PORT=8000
```

**Pour un débutant :** 
- Remplace `ton_mot_de_passe` par ton vrai mot de passe PostgreSQL
- Par défaut sur Windows, c'est souvent vide ou celui que tu as défini lors de l'installation
- Si tu utilises Docker, le mot de passe est `postgres`
- `JWT_SECRET_KEY` doit être une longue chaîne aléatoire pour sécuriser les tokens

### 5. Créer les tables dans PostgreSQL

Si tu n'utilises pas Docker (SQLModel crée auto les tables sinon) :

```bash
# Se connecter à PostgreSQL et exécuter le fichier SQL
psql -U postgres -d fastapisqlmodelpostgres -f tables.sql
```

Ou via pgAdmin : Importe le fichier `tables.sql`.

## Lancement de l'application

```bash
python -m uvicorn main:app --reload --port 8000
```

Tu verras quelque chose comme :
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Pour un débutant :** L'API est maintenant accessible à l'adresse indiquée.

## Comment tester l'API (guide débutant)

### Qu'est-ce qu'une API ?

Une API (Application Programming Interface) est un service qui répond à des requêtes. Contrairement à un site web classique, tu ne vois pas de pages HTML, mais des données en format JSON.

### Méthodes de test

Tu peux tester l'API de plusieurs façons :

1. **Navigateur** (uniquement pour les requêtes GET)
2. **cURL** (ligne de commande)
3. **Postman** ou **Insomnia** (applications dédiées)
4. **Swagger UI** (interface web intégrée à FastAPI - **RECOMMANDÉ**)

### Swagger UI - La méthode la plus simple pour débutants

FastAPI fournit une interface web automatique pour tester l'API.

**URL à taper dans le navigateur :** `http://localhost:8000/docs`

Cette page montre tous les endpoints disponibles et te permet de les tester directement !

Alternative : `http://localhost:8000/redoc` pour une documentation différente.

---

## API Endpoints - Guide complet pour débutants

Les "endpoints" sont les adresses auxquelles tu envoies des requêtes pour interagir avec l'API.

### Authentification Admin (Connexion/Inscription)

| Endpoint | Méthode | Description | URL complète |
|----------|---------|-------------|--------------|
| `/api/admins/signup` | POST | Créer un compte admin et recevoir un token JWT | `http://localhost:8000/api/admins/signup` |
| `/api/admins/signin` | POST | Se connecter et recevoir un token JWT | `http://localhost:8000/api/admins/signin` |
| `/api/admins/me` | GET | Voir les infos de l'admin connecté (nécessite token) | `http://localhost:8000/api/admins/me` |
| `/api/admins/me` | PATCH | Modifier son propre compte (nécessite token) | `http://localhost:8000/api/admins/me` |
| `/api/admins/me` | DELETE | Supprimer son propre compte (nécessite token) | `http://localhost:8000/api/admins/me` |

### Gestion des Administrateurs

| Endpoint | Méthode | Description | URL complète |
|----------|---------|-------------|--------------|
| `/api/admins/` | GET | Liste tous les admins (nécessite token) | `http://localhost:8000/api/admins/` |
| `/api/admins/{admin_id}` | PATCH | Modifier un admin par ID (nécessite token) | Ex: `http://localhost:8000/api/admins/550e8400-e29b-41d4-a716-446655440000` |
| `/api/admins/{admin_id}` | DELETE | Supprimer un admin par ID (nécessite token) | Ex: `http://localhost:8000/api/admins/550e8400-e29b-41d4-a716-446655440000` |

### Gestion des Étudiants

| Endpoint | Méthode | Description | URL complète |
|----------|---------|-------------|--------------|
| `/api/students/` | GET | Liste tous les étudiants (nécessite token) | `http://localhost:8000/api/students/` |
| `/api/students/` | POST | Créer un nouvel étudiant (nécessite token) | `http://localhost:8000/api/students/` |
| `/api/students/{student_id}` | GET | Voir un étudiant par ID (nécessite token) | Ex: `http://localhost:8000/api/students/550e8400-e29b-41d4-a716-446655440000` |
| `/api/students/{student_id}` | PATCH | Modifier un étudiant par ID (nécessite token) | Ex: `http://localhost:8000/api/students/550e8400-e29b-41d4-a716-446655440000` |
| `/api/students/{student_id}` | DELETE | Supprimer un étudiant par ID (nécessite token) | Ex: `http://localhost:8000/api/students/550e8400-e29b-41d4-a716-446655440000` |

**Note pour les débutants :** Les IDs sont des UUID (longues chaînes de caractères). Remplace `{admin_id}` ou `{student_id}` par un vrai ID obtenu lors de la création.

---

## Instructions de test détaillées (pour débutants)

### Test 1 : Vérifier que Docker PostgreSQL fonctionne (si utilisé)

**Objectif :** S'assurer que la base de données est prête.

**Étapes :**
1. Si tu utilises Docker, vérifie que le conteneur tourne :
```bash
docker ps
```
2. Tu dois voir un conteneur `postgres` en cours d'exécution
3. **Résultat attendu :** Le conteneur est "Up" et expose le port 5432

### Test 2 : Vérifier que l'API fonctionne

**Objectif :** S'assurer que le serveur tourne.

**Étapes :**
1. Lance le serveur : `python -m uvicorn main:app --reload --port 8000`
2. Ouvre ton navigateur
3. Tape : `http://localhost:8000/`
4. **Résultat attendu :** Tu vois un message JSON :
```json
{"message": "Bienvenue sur l'API FastAPI + PostgreSQL !"}
```

### Test 3 : Explorer la documentation Swagger

**Objectif :** Découvrir l'interface de test intégrée.

**Étapes :**
1. Dans le navigateur, tape : `http://localhost:8000/docs`
2. Tu vois une page avec tous les endpoints listés
3. Clique sur n'importe quel endpoint pour le déplier
4. **Résultat attendu :** Tu vois les paramètres attendus et un bouton "Try it out"

### Test 4 : Créer un compte admin (Signup)

**Objectif :** Créer le premier administrateur.

**Étapes avec Swagger :**
1. Va sur : `http://localhost:8000/docs`
2. Trouve `POST /api/admins/signup`
3. Clique sur "Try it out"
4. Dans le corps (Request body), entre :
```json
{
  "nom": "Admin Principal",
  "email": "admin@test.com",
  "password": "password123"
}
```
5. Clique sur "Execute"
6. **Résultat attendu :** Code 200 avec une réponse contenant `access_token` :
```json
{
  "status": "success",
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Important :** Copie ce token ! Tu en auras besoin pour les prochaines requêtes.

### Test 5 : Se connecter (Signin)

**Objectif :** Obtenir un token JWT en se connectant.

**Étapes :**
1. Dans Swagger, trouve `POST /api/admins/signin`
2. Clique "Try it out"
3. Entre les identifiants :
```json
{
  "nom": "Admin Principal",
  "email": "admin@test.com",
  "password": "password123"
}
```
4. Clique "Execute"
5. **Résultat attendu :** Un nouveau token JWT

### Test 6 : Voir son profil (Get Me)

**Objectif :** Récupérer les informations de l'admin connecté.

**Étapes :**
1. Dans Swagger, trouve `GET /api/admins/me`
2. Clique "Try it out"
3. Dans le champ **Authorize** (en haut de la page Swagger), colle ton token :
   - Clique sur le cadenas 🔒 en haut à droite
   - Dans le champ, écris : `Bearer eyJhbGciOiJIUzI1NiIs...` (remplace par ton token)
   - Clique "Authorize" puis "Close"
4. Clique "Execute" sur `GET /api/admins/me`
5. **Résultat attendu :** 
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "nom": "Admin Principal",
  "email": "admin@test.com",
  "role": "admin",
  "created_at": "2024-01-15T10:30:00"
}
```

### Test 7 : Créer un étudiant

**Objectif :** Ajouter un étudiant dans la base.

**Étapes :**
1. Assure-toi d'être authentifié (token dans Authorize)
2. Trouve `POST /api/students/`
3. Clique "Try it out"
4. Entre les données :
```json
{
  "nom": "Dupont",
  "prenom": "Marie",
  "filiere": "Informatique",
  "email": "marie.dupont@example.com",
  "annee": "2024-09-01"
}
```
5. Clique "Execute"
6. **Résultat attendu :** 
```json
{
  "status": "success",
  "student": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "nom": "Dupont",
    "prenom": "Marie",
    "filiere": "Informatique",
    "email": "marie.dupont@example.com",
    "annee": "2024-09-01",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  }
}
```

### Test 8 : Lister tous les étudiants

**Objectif :** Voir tous les étudiants enregistrés.

**Étapes :**
1. Authentifié avec le token
2. Trouve `GET /api/students/`
3. Clique "Execute"
4. **Résultat attendu :** Liste contenant l'étudiant créé au Test 7

### Test 9 : Modifier un étudiant

**Objectif :** Changer les informations d'un étudiant.

**Étapes :**
1. Récupère l'ID de l'étudiant créé (Test 7)
2. Trouve `PATCH /api/students/{student_id}`
3. Clique "Try it out"
4. Dans `student_id`, colle l'ID de l'étudiant
5. Dans le corps, entre les nouvelles données :
```json
{
  "nom": "Dupont",
  "prenom": "Marie",
  "filiere": "Mathematics",
  "email": "marie.dupont@example.com",
  "annee": "2024-09-01"
}
```
6. Clique "Execute"
7. **Résultat attendu :** L'étudiant avec la filière mise à jour

### Test 10 : Voir un étudiant spécifique

**Objectif :** Récupérer les détails d'un seul étudiant.

**Étapes :**
1. Trouve `GET /api/students/{student_id}`
2. Entre l'ID de l'étudiant
3. Clique "Execute"
4. **Résultat attendu :** Les détails complets de l'étudiant

### Test 11 : Supprimer un étudiant

**Objectif :** Retirer un étudiant.

**Étapes :**
1. Trouve `DELETE /api/students/{student_id}`
2. Entre l'ID de l'étudiant
3. Clique "Execute"
4. **Résultat attendu :** Code 204 (No Content) - suppression réussie

### Test 12 : Tester sans authentification (Erreur attendue)

**Objectif :** Vérifier que les routes protégées nécessitent un token.

**Étapes :**
1. Clique sur "Logout" en haut de Swagger (ou supprime le token d'Authorize)
2. Essaie `GET /api/students/`
3. **Résultat attendu :** Code 401 avec message "Not authenticated"

### Test 13 : Tester un email déjà utilisé

**Objectif :** Vérifier la validation des données.

**Étapes :**
1. Authentifié, essaie de créer un étudiant avec l'email `marie.dupont@example.com` (déjà créé au Test 7)
2. **Résultat attendu :** Code 400 avec message "Email déjà utilisé"

### Test 14 : Lister les admins

**Objectif :** Voir tous les administrateurs.

**Étapes :**
1. Authentifié, trouve `GET /api/admins/`
2. Clique "Execute"
3. **Résultat attendu :** Liste des admins avec leur ID, nom, email

### Test 15 : Modifier son propre compte

**Objectif :** Mettre à jour ses informations.

**Étapes :**
1. Authentifié, trouve `PATCH /api/admins/me`
2. Entre de nouvelles données :
```json
{
  "nom": "Admin Modifié",
  "email": "admin@test.com",
  "password": "nouveaumotdepasse"
}
```
3. Clique "Execute"
4. **Résultat attendu :** Confirmation de la mise à jour

---

## Tester avec cURL (ligne de commande)

Si tu préfères utiliser le terminal :

### 1. Créer un admin
```bash
curl -X POST "http://localhost:8000/api/admins/signup" \
  -H "Content-Type: application/json" \
  -d '{"nom": "Admin Test", "email": "admin@test.com", "password": "password123"}'
```

### 2. Se connecter et récupérer le token
```bash
curl -X POST "http://localhost:8000/api/admins/signin" \
  -H "Content-Type: application/json" \
  -d '{"nom": "Admin Test", "email": "admin@test.com", "password": "password123"}'
```

### 3. Créer un étudiant (avec token)
```bash
curl -X POST "http://localhost:8000/api/students/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TON_TOKEN_ICI" \
  -d '{"nom": "Dupont", "prenom": "Marie", "filiere": "Informatique", "email": "marie@example.com", "annee": "2024-09-01"}'
```

### 4. Lister les étudiants
```bash
curl -X GET "http://localhost:8000/api/students/" \
  -H "Authorization: Bearer TON_TOKEN_ICI"
```

---

## Structure du projet

```
.
├── main.py                      # Point d'entrée de l'application
├── docker-compose.yml           # Configuration Docker pour PostgreSQL
├── config/
│   ├── database.py             # Configuration de la base de données PostgreSQL
│   └── ...
├── controllers/
│   ├── admin_controller.py     # Routes API pour les admins
│   └── student_controller.py   # Routes API pour les étudiants
├── models/
│   ├── admin.py                # Modèle SQLModel Admin
│   └── student.py              # Modèle SQLModel Student
├── schemas/
│   ├── admin.py                # Schémas Pydantic pour Admin
│   └── student.py              # Schémas Pydantic pour Student
├── auth/
│   └── jwt.py                  # Authentification JWT
├── requirements.txt            # Dépendances Python
├── tables.sql                  # Structure de la base de données PostgreSQL
└── .env                        # Variables d'environnement (non versionnée)
```

## Technologies utilisées

- **FastAPI** - Framework web moderne et rapide pour Python
- **SQLModel** - ORM basé sur SQLAlchemy et Pydantic
- **AsyncPG** - Connecteur PostgreSQL asynchrone
- **Uvicorn** - Serveur ASGI performant
- **Pydantic** - Validation des données
- **python-jose** - Gestion des tokens JWT
- **passlib** - Hachage sécurisé des mots de passe
- **PostgreSQL** - Base de données relationnelle avancée
- **Docker** - Conteneurisation (optionnel)
- **Git** - Gestion de version

## Notes de sécurité

- **JWT (JSON Web Tokens)** : Les tokens d'authentification expirent après un certain temps
- **Mots de passe** : Hachés avec bcrypt avant stockage
- **CORS** : Configuré pour n'accepter que les requêtes du frontend autorisé (`FRONTEND_URL`)
- **SQLModel** : Protège contre les injections SQL via des requêtes paramétrées
- **PostgreSQL** : Base de données robuste avec support des transactions ACID
- **Le fichier `setup.py` n'est pas inclus dans le repository**
- **Le fichier `.env` contenant les secrets n'est pas versionné**

## Dépannage pour débutants

### Problème : "ModuleNotFoundError: No module named 'fastapi'"
**Solution :** Tu as oublié d'activer l'environnement virtuel :
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Problème : "Cannot connect to PostgreSQL" ou "Connection refused"
**Solution :** 
- Si tu utilises Docker : Vérifie que le conteneur tourne avec `docker ps`
- Si PostgreSQL local : Vérifie que le service PostgreSQL est démarré (Services Windows ou `sudo service postgresql start` sur Linux)
- Vérifie tes identifiants dans le fichier `.env`

### Problème : Docker ne démarre pas (port 5432 déjà utilisé)
**Solution :** Un autre PostgreSQL tourne déjà sur ce port. Soit :
- Arrête l'autre PostgreSQL : `sudo service postgresql stop`
- Ou modifie le port dans `docker-compose.yml` : change `"5432:5432"` en `"5433:5432"` et mets à jour `.env`

### Problème : "Authentication failed" ou 401 Unauthorized
**Solution :** 
- Vérifie que tu as bien mis le token dans l'en-tête `Authorization: Bearer ...`
- Vérifie que le token n'a pas expiré (récupère-en un nouveau avec signin)
- Assure-toi qu'il n'y a pas d'espace en trop dans le token

### Problème : "Email déjà utilisé" alors que la base est vide
**Solution :** 
- SQLModel a peut-être déjà créé les tables avec des données
- Connecte-toi à PostgreSQL : `docker exec -it <nom_conteneur> psql -U postgres -d school_db`
- Vide la table : `TRUNCATE TABLE admin CASCADE;`
- Ou recrée le conteneur Docker : `docker-compose down -v && docker-compose up -d`

### Problème : "Validation error" ou 422 Unprocessable Entity
**Solution :** 
- Vérifie le format de tes données JSON
- L'email doit être valide (format email@domain.com)
- La date doit être au format ISO : `YYYY-MM-DD`
- Le mot de passe ne doit pas être vide

### Problème : Impossible d'accéder à l'API depuis le frontend
**Solution :** 
- Vérifie que `FRONTEND_URL` dans `.env` correspond bien à l'URL de ton frontend
- Pour le développement local, tu peux temporairement mettre `FRONTEND_URL=*`
