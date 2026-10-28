# E02 — FluxyRH Entreprise · Dossier

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E01

## 1. Objet

Porter le dossier authentique sur le téléphone : l'employé complète et tient à jour ses données (assistant de complétion, blocs, pièces prises en photo), même hors ligne ; le RH, le PAIE et la direction **vérifient** une demande à la fois avec le justificatif ; le RH cherche un employé ; le manager voit son équipe. À la fin d'E02, tout le cycle invitation → complétion → vérification se fait aussi dans l'app.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-EMP-03 | Complétion, nouvelle version à chaque modification |
| F-EMP-04, F-MOB-04 | Vérification par le RH, le PAIE, la direction, une par une |
| F-EMP-05, 06 | Pièces, complétude |
| F-MOB-03 | Saisies du dossier en file hors ligne |

À lire : APPFLOW §3.1 (fin), §4.4 à §4.7, §5.3, §5.4 ; UX/UI §6.3 à §6.5, §7.4 ; `02-reference/` (W04).

## 3. Prérequis et décisions

E01 livré.

| Sujet | Proposition |
|---|---|
| Photos des pièces | Prises avec l'appareil photo ou choisies dans la galerie, recadrées et compressées sous 10 Mo (limite du serveur), mises en file avec la saisie (TRD §18.2) |
| Données bancaires | Affichées masquées par défaut (`SensitiveValue`), révélées d'un appui par l'employé lui-même ; jamais dans le cache des autres rôles |
| Vérification | Une demande à la fois, valeur en vigueur, nouvelle valeur et justificatif en plein écran ; passage automatique à la suivante ; exige le réseau |
| Accès rapide par la carte | Construit en E03 |

## 4. Étapes ordonnées

### E02.1 — Mon dossier et assistant

- Composants `Stepper` et `VersionDiff`.
- Assistant de complétion (UX/UI §6.5) après la première connexion et depuis l'accueil tant qu'il n'est pas terminé ; « Enregistrer et continuer plus tard ».
- Mon dossier par blocs : valeur en vigueur, modification en attente, badge de statut, motif de rejet ; modifier un bloc (correction en place d'une version en attente, W04.2).
- Saisies et pièces en file hors ligne (E00.7).

### E02.2 — Pièces

- Mes pièces : attendues, déposées, expirées ; dépôt par photo ou fichier ; dates de délivrance et d'expiration ; documents déposés par le RH en lecture.

### E02.3 — Vérifications

- Onglet **Validations** du RH (données), du PAIE (banque) et élément de la direction dans **Approbations** (données des RH, banque des PAIE) : liste, écran de vérification (§3), vérifier, rejeter avec motif.

### E02.4 — Employés et équipe

- RH : onglet **Employés** (recherche, fiche en lecture selon les droits, complétude).
- Manager : onglet **Équipe**, liste de l'équipe directe et indirecte.

### E02.5 — Documentation et livraison

- `02-reference/` : écrans du dossier.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E02 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Complétion | Assistant interrompu et repris, bloc modifié, correction en place, rejet affiché |
| Hors ligne | Saisie et photo en file, envoi au retour du réseau, refus motivé |
| Pièces | Compression, limite de taille, expiration |
| Vérification | Une par une, justificatif, rejet motivé, ses propres données absentes |
| Confidentialité | Banque masquée, absente pour RH et ADM |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §5.3 et §5.4 sur téléphone, en ligne et hors ligne.
- Documentation et livraison d'E02.5 faites.

## 7. Reporté

| Élément | Fichier |
|---|---|
| Ouverture d'un dossier en scannant une carte | E03 |
