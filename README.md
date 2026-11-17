# TransConnect

Plateforme web B2B de mise en relation entre entreprises chargeuses et
transporteurs. TransConnect permet de publier des expéditions, de gérer une
flotte de véhicules, de recevoir des offres de transport et de suivre les
opérations depuis un espace sécurisé.

## Sommaire

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Rôles et droits](#rôles-et-droits)
- [Règles métier](#règles-métier)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [Parcours principaux](#parcours-principaux)
- [Structure du projet](#structure-du-projet)
- [URLs principales](#urls-principales)
- [Vérifications](#vérifications)
- [Sécurité et production](#sécurité-et-production)
- [Améliorations possibles](#améliorations-possibles)

## Présentation

TransConnect centralise les échanges liés au transport de marchandises :

1. Une entreprise **chargeur** décrit un besoin d'expédition.
2. Une entreprise **transporteur** consulte les expéditions disponibles.
3. Le transporteur propose un prix, un délai et un véhicule compatible.
4. Le chargeur consulte les offres et peut en accepter une.
5. L'expédition passe automatiquement à l'état attribué lorsque l'offre est
   acceptée.

L'interface est en français et possède une identité visuelle B2B responsive,
avec un mode clair/sombre, une navigation adaptée aux petits écrans et des
illustrations SVG intégrées aux templates.

## Fonctionnalités

### Authentification et comptes

- Connexion, déconnexion et inscription.
- Modèle utilisateur personnalisé `EntreprisesApp.Utilisateur`.
- Modification du profil.
- Changement du mot de passe.
- Redirection des utilisateurs non connectés vers la page de connexion.
- Tableau de bord personnalisé selon le rôle.
- Création d'une seule entreprise par utilisateur.

### Gestion des entreprises

- Création, consultation, modification et suppression d'une entreprise.
- Association d'une entreprise à son gérant.
- Vérification du matricule fiscal tunisien.
- Vérification du type d'entreprise :
  - `chargeur`
  - `transporteur`

### Gestion des expéditions

- Création automatique d'une référence annuelle au format
  `EXP-AA-00001`.
- Gestion des villes de départ et d'arrivée.
- Date souhaitée, poids et description.
- Statuts :
  - Publiée
  - Attribuée
  - En cours
  - Livrée
  - Annulée
- Isolation des données : un chargeur ne voit que les expéditions de son
  entreprise, sauf l'administrateur.

### Gestion des véhicules

- Immatriculation unique.
- Type de véhicule et capacité en kilogrammes.
- Disponibilité du véhicule.
- Vérification qu'un véhicule appartient à une entreprise transporteur.
- Vérification automatique de la capacité selon le type de véhicule.

### Gestion des offres

- Création d'une offre avec prix, délai, véhicule et expédition.
- Une offre ne peut être proposée que sur une expédition publiée.
- Le véhicule doit appartenir au transporteur qui propose l'offre.
- Un véhicule indisponible ne peut pas être utilisé pour une nouvelle offre.
- Une seule offre proposée active par transporteur et par expédition.
- Acceptation d'une offre :
  - l'expédition devient `attribuée` ;
  - les autres offres proposées deviennent `refusées`.

### Interface et expérience utilisateur

- Design corporate adapté à la logistique B2B.
- Logo TransConnect simplifié en monogramme `TC`.
- Navigation avec accès regroupés au profil et à la déconnexion.
- Mode clair/sombre mémorisé dans le navigateur.
- Menu responsive sur mobile.
- Cartes de services, indicateurs, raccourcis et parcours en trois étapes.
- Illustrations et icônes SVG sans dépendance externe.
- Formulaires avec affichage/masquage du mot de passe.
- Confirmation avant suppression.

## Rôles et droits

| Fonction | Chargeur | Transporteur | Administrateur |
| --- | :---: | :---: | :---: |
| Consulter son tableau de bord | Oui | Oui | Oui |
| Gérer son profil | Oui | Oui | Oui |
| Gérer son entreprise | Oui | Oui | Oui |
| Créer une expédition | Oui | Non | Oui |
| Modifier/supprimer ses expéditions | Oui | Non | Oui |
| Consulter les expéditions | Oui | Oui | Oui |
| Créer/modifier des véhicules | Non | Oui | Oui |
| Créer une offre | Non | Oui | Oui |
| Consulter les offres reçues | Oui | Oui | Oui |
| Voir toutes les données | Non | Non | Oui |

Les contrôles d'accès sont centralisés dans
[`config/access.py`](config/access.py). Les vues filtrent également les
querysets et les formulaires afin d'éviter l'accès à des objets d'une autre
entreprise.

## Règles métier

### Compatibilité des poids

Les limites sont centralisées dans
[`config/weights.py`](config/weights.py) :

| Type | Poids autorisé |
| --- | --- |
| Camionnette | `0.01` à `1500 kg` |
| Fourgon | `0.01` à `3500 kg` |
| Camion porteur | `3500.01` à `19000 kg` |
| Semi-remorque | `19000.01` à `26000 kg` |

La capacité déclarée d'un véhicule doit également rester dans la plage de
son type. Les valeurs sont comparées avec `Decimal` pour éviter les erreurs
de précision des nombres flottants.

### Validation des données

- Les poids et prix doivent être strictement supérieurs à `0`.
- Le délai d'une offre doit être au moins égal à un jour.
- Une adresse d'entreprise doit contenir au moins 20 caractères.
- Les adresses email doivent utiliser le domaine `gmail.com` selon le
  validateur actuel du projet.
- Le matricule fiscal doit respecter le format configuré dans
  `EntreprisesApp/models.py`.

## Technologies

- Python 3
- Django `5.2.17`
- SQLite
- HTML5, CSS3 et JavaScript natif
- Templates Django
- SVG inline pour le logo et les illustrations

Aucune bibliothèque frontend externe n'est nécessaire pour l'interface
actuelle.

## Installation

### Prérequis

- Python installé et disponible dans le terminal.
- Git, si le projet est récupéré depuis un dépôt.
- Windows PowerShell recommandé pour l'environnement actuel.

### Récupérer le projet

```powershell
git clone <url-du-depot>
cd transconnect
```

### Créer l'environnement virtuel

```powershell
py -m venv .venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l'activation, il est possible d'utiliser directement
l'interpréteur de l'environnement :

```powershell
.\.venv\Scripts\python.exe manage.py check
```

### Installer Django

Le projet utilise Django 5.2.17 :

```powershell
python -m pip install "Django==5.2.17"
```

Pour une installation reproductible, ajouter les dépendances du projet à un
futur fichier `requirements.txt`.

## Configuration

Les principaux réglages se trouvent dans
[`config/settings.py`](config/settings.py) :

- Base SQLite : `nour.sqlite3`
- Modèle utilisateur : `EntreprisesApp.Utilisateur`
- Templates : dossier `templates/`
- URL de connexion : `/connexion/`
- Redirection après connexion : `/dashboard/`
- Redirection après déconnexion : `/`
- Langue Django actuelle : `en-us`
- Fuseau horaire actuel : `UTC`

### Base de données

Appliquer les migrations :

```powershell
python manage.py migrate
```

Créer un compte administrateur Django pour `/admin/` :

```powershell
python manage.py createsuperuser
```

Le rôle applicatif `administrateur` est distinct du superutilisateur Django.
Pour l'administration fonctionnelle de la plateforme, utiliser un utilisateur
avec le rôle approprié.

## Lancement

Démarrer le serveur de développement :

```powershell
python manage.py runserver
```

Application disponible à l'adresse :

```text
http://127.0.0.1:8000/
```

Sous Windows, avec l'environnement du projet :

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

## Parcours principaux

### Créer un compte chargeur ou transporteur

1. Ouvrir `/inscription/`.
2. Saisir les informations du compte.
3. Choisir `Chargeur` ou `Transporteur`.
4. Se connecter depuis `/connexion/`.
5. Créer l'entreprise depuis le tableau de bord.

L'inscription publique ne propose pas le rôle administrateur.

### Parcours chargeur

1. Créer une entreprise de type chargeur.
2. Ouvrir `Expéditions`.
3. Ajouter une expédition avec son poids.
4. Consulter les offres reçues.
5. Accepter l'offre choisie.

### Parcours transporteur

1. Créer une entreprise de type transporteur.
2. Ajouter un véhicule.
3. Vérifier sa capacité et sa disponibilité.
4. Consulter les expéditions publiées.
5. Créer une offre avec un véhicule compatible.

## Structure du projet

```text
transconnect/
├── config/
│   ├── access.py              # Règles d'accès et rôles
│   ├── forms.py               # Formulaires d'authentification/profil
│   ├── settings.py            # Configuration Django
│   ├── urls.py                # Routes principales
│   ├── views.py               # Authentification et dashboard
│   └── weights.py             # Limites de poids partagées
├── EntreprisesApp/
│   ├── models.py              # Utilisateur et entreprise
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── VehiculesApp/
│   ├── models.py              # Véhicules et capacité
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── ExpeditionsApp/
│   ├── models.py              # Expéditions et statuts
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── OffersApp/
│   ├── models.py              # Offres et règles d'acceptation
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── templates/
│   ├── base.html              # Layout, navigation, thème et JS
│   ├── home.html              # Page d'accueil
│   ├── dashboard.html         # Tableau de bord
│   ├── registration/          # Authentification et profil
│   ├── expeditions/
│   ├── vehicules/
│   ├── offres/
│   └── entreprises/
├── manage.py
├── nour.sqlite3               # Base locale de développement
└── README.md
```

## URLs principales

| URL | Description |
| --- | --- |
| `/` | Accueil |
| `/connexion/` | Connexion |
| `/inscription/` | Inscription |
| `/deconnexion/` | Déconnexion |
| `/profil/` | Profil |
| `/mot-de-passe/` | Changement du mot de passe |
| `/dashboard/` | Tableau de bord |
| `/Expeditions/` | Gestion des expéditions |
| `/Vehicules/` | Gestion des véhicules |
| `/Offres/` | Gestion des offres |
| `/Entreprises/` | Gestion des entreprises |
| `/admin/` | Administration Django |

## Vérifications

Vérifier la configuration Django :

```powershell
python manage.py check
```

Vérifier les migrations :

```powershell
python manage.py makemigrations --check
python manage.py migrate --plan
```

Lancer la suite de tests :

```powershell
python manage.py test
```

Vérifier les espaces et erreurs de patch :

```powershell
git diff --check
```

Le JavaScript principal est intégré dans
[`templates/base.html`](templates/base.html). Avec Node.js installé, une
vérification syntaxique peut être exécutée après extraction du bloc script.

## Sécurité et production

La configuration actuelle est destinée au développement. Avant tout
déploiement, il faut obligatoirement :

1. Remplacer `SECRET_KEY` par une variable d'environnement secrète.
2. Passer `DEBUG = False`.
3. Configurer `ALLOWED_HOSTS`.
4. Configurer une base de données de production.
5. Configurer les fichiers statiques avec `collectstatic`.
6. Utiliser HTTPS et activer les cookies sécurisés.
7. Configurer un vrai backend email.
8. Ne pas versionner `nour.sqlite3`, les secrets ou les fichiers `.env`.
9. Vérifier les réglages de sécurité avec :

   ```powershell
   python manage.py check --deploy
   ```

Le fichier de configuration contient une section `MAILERS` orientée vers la
console. Pour un envoi réel, configurer explicitement `EMAIL_BACKEND` et les
paramètres SMTP adaptés à l'environnement de déploiement.

## Améliorations possibles

- Ajouter un fichier `requirements.txt` ou `pyproject.toml`.
- Ajouter des tests permanents pour les droits, les poids et l'acceptation des
  offres.
- Ajouter un historique des changements de statut.
- Ajouter des notifications pour les nouvelles offres.
- Ajouter une recherche et des filtres avancés par ville, poids et statut.
- Ajouter une pagination sur les listes importantes.
- Ajouter un suivi de livraison avec événements horodatés.
- Remplacer SQLite par PostgreSQL en production.
- Ajouter une gestion de pièces jointes pour les documents de transport.

## Licence

Aucune licence open source n'est déclarée actuellement dans le projet.
Ajouter un fichier `LICENSE` si le projet doit être distribué publiquement.