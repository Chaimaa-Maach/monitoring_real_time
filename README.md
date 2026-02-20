#  Data Pipeline & Dashboard de Monitoring Système en Temps Réel

##  Présentation du projet

Ce projet consiste à concevoir un pipeline de données permettant de surveiller les performances d’un système en temps réel.

Les métriques système (CPU, RAM, Disque, Réseau) sont collectées automatiquement via Python, stockées dans Google Sheets, puis visualisées à travers un dashboard interactif développé avec Looker Studio.

Ce projet illustre le cycle complet de la donnée :

Collecte → Stockage → Transformation → Visualisation → Détection d’alertes

---

##  Objectifs

- Surveiller les performances système en temps réel
- Analyser les tendances historiques
- Détecter les surcharges potentielles
- Appliquer les bonnes pratiques de dashboarding
- Mettre en œuvre un pipeline de données de bout en bout

---

##  Architecture du projet

```
Métriques système (CPU, RAM, Disque, Réseau)
                ↓
Script Python (collecte automatique)
                ↓
Google Sheets (TimeSeries + LastOnly)
                ↓
Dashboard Looker Studio
```

---

##  Fonctionnement du pipeline

### 1️ Collecte des données

- Script Python utilisant la bibliothèque `psutil`
- Extraction automatique des métriques :
  - CPU (%)
  - RAM (%)
  - Disque (%)
  - Réseau (KB/s)
- Mise à jour toutes les 15 secondes

###  Stockage des données

Deux feuilles sont utilisées :

**TimeSeries**
- Contient l’historique complet des métriques
- Utilisée pour l’analyse des tendances

**LastOnly**
- Contient uniquement la dernière mesure
- Utilisée pour les indicateurs temps réel (KPIs)

---

##  Fonctionnalités du Dashboard

###  Indicateurs temps réel
- Scorecard CPU
- Scorecard RAM
- Jauge Disque
- Indicateur de surcharge CPU

###  Analyse historique
- Évolution du CPU dans le temps
- Évolution de la RAM
- Utilisation du disque
- Activité réseau

---

##  Logique d’alerte CPU

```
CASE
  WHEN CPU% > 80 THEN "HIGH"
  WHEN CPU% > 50 THEN "MEDIUM"
  ELSE "NORMAL"
END
```

Cette logique permet d’identifier le niveau de charge du système.

---

##  Technologies utilisées

- Python
- psutil
- Google Sheets API
- Google OAuth 2.0
- Looker Studio
- Git & GitHub

---




##  Sécurité

Les fichiers sensibles ne sont pas inclus dans le dépôt :

- credentials.json
- token.pickle


---

##  Compétences développées

- Conception d’un pipeline de données simple
- Intégration d’API Google
- Monitoring en temps réel
- Création de dashboards interactifs
- Implémentation d’indicateurs d’alerte
- Structuration et storytelling des données

---

##  Contexte

Projet réalisé dans le cadre d’une formation Data Analyst afin de mettre en pratique les concepts de collecte continue, visualisation et analyse de données en environnement quasi temps réel.

