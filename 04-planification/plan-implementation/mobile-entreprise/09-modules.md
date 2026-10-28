# E09 — FluxyRH Entreprise · Modules

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E08

## 1. Objet

Porter sur le téléphone ce qui sert au quotidien dans les modules payants, et seulement si le module est souscrit : **Processus RH** (événements proposés par le manager, formulaires demandés par l'employé, courriers à accuser ou à signer, tâches de workflow), **Talents** (évaluations à remplir, rapports), **Pilotage** (accueil à indicateurs de la direction). Le paramétrage, la conformité et les simulations restent au web (UX/UI §7.5).

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-MOB-06 | Fonctions des modules non souscrits masquées |
| F-PRO-01, 02, 03, 04 (mobile) | Événements, tâches, courriers, formulaires |
| F-TAL-01 (mobile) | Évaluations |
| F-PIL-01 (mobile) | Indicateurs de l'accueil |

À lire : APPFLOW §5.12 à §5.14 ; `02-reference/` (W12, W13, W15).

## 3. Prérequis et décisions

E08 livré.

| Sujet | Proposition |
|---|---|
| Périmètre | Ce qu'on fait en mobilité : proposer, demander, répondre, accuser, signer, consulter. Tout ce qui se configure reste au web |
| Indicateurs | L'accueil de la direction reprend les widgets choisis au web, en lecture |

## 4. Étapes ordonnées

### E09.1 — Processus RH

- Manager : proposer un événement pour un membre de l'équipe, suivre ses propositions.
- Employé : demander un formulaire (dossier complet exigé selon le type), télécharger quand il est prêt ; courriers reçus et accusé de réception.
- Direction : courriers et formulaires à signer dans **Approbations**.
- Chacun : ses tâches de workflow (prendre, faire, ignorer avec note) ; RH : propositions de lancement de workflow (lancer, écarter avec motif).

### E09.2 — Talents

- Évaluations à remplir (une seule réponse par évaluateur), mes rapports d'évaluation selon l'anonymat de la campagne.

### E09.3 — Pilotage

- Accueil à indicateurs de la direction (et des rôles qui ont des widgets), en lecture.

### E09.4 — Documentation et livraison

- `02-reference/` : écrans des modules.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E09 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Modules | Chaque écran absent sans le module |
| Processus RH | Proposition, formulaire bloqué sur dossier incomplet, accusé, signature, tâches, propositions de workflow |
| Talents | Réponse unique, rapport anonyme ou nominatif |
| Pilotage | Widgets en lecture, aucune donnée sensible hors droits |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §5.12 à §5.14 sur téléphone pour une entreprise avec tous les modules et une sans.
- Documentation et livraison d'E09.4 faites.
