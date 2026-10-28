# FluxyRH — Feuille de route

Statuts : ⬜ à faire · 🟡 en cours · ✅ livré

Ordre, dépendances, contenu et couverture des exigences : [`plan-implementation/`](plan-implementation/README.md). Décision : [0001](../03-architecture/decisions/2026-10-27-0001-ordre-de-developpement.md).

## Application web (`FluxyRH-web/app/`)

| Code | Module | Dépend de | Statut |
|---|---|---|---|
| W00 | Amorçage technique | — | ⬜ |
| W01 | Plateforme | W00 | ⬜ |
| W02 | Administration et accès | W01 | ⬜ |
| W03 | Organisation, sites, bornes | W02 | ⬜ |
| W04.1 | Dossier — RH : invitation et affectation | W03 | ⬜ |
| W04.2 | Dossier — Employé : complétion | W04.1 | ⬜ |
| W04.3 | Dossier — Vérification | W04.2 | ⬜ |
| W05 | Cartes NFC | W04 | ⬜ |
| W06.1 | Temps — Paramétrage | W05 | ⬜ |
| W06.2 | Temps — Pointage | W06.1 | ⬜ |
| W06.3 | Temps — Manager | W06.2 | ⬜ |
| W06.4 | Temps — RH | W06.3 | ⬜ |
| W07 | Congés et absences | W06 | ⬜ |
| W08.1 | Contrats — Bibliothèque de blocs | W07 | ⬜ |
| W08.2 | Contrats — Rédaction | W08.1 | ⬜ |
| W08.3 | Contrats — Signature | W08.2 | ⬜ |
| W08.4 | Contrats — Vie du contrat | W08.3 | ⬜ |
| W09.1 | Paie — Paramétrage | W08 | ⬜ |
| W09.2 | Paie — Éléments par employé | W09.1 | ⬜ |
| W09.3 | Paie — Variables (RH) | W09.2 | ⬜ |
| W09.4 | Paie — Calcul et contrôle | W09.3 | ⬜ |
| W09.5 | Paie — Approbation (DIR) | W09.4 | ⬜ |
| W09.6 | Paie — Clôture, bulletins, paiements | W09.5 | ⬜ |
| W09.7 | Paie — Avances et prêts | W09.6 | ⬜ |
| W09.8 | Paie — Journaux et états | W09.6 | ⬜ |
| W10 | Communication et centre d'aide | W09 | ⬜ |
| W11 | Module Conformité | W10 | ⬜ |
| W12.1 | Processus RH — Événements | W11 | ⬜ |
| W12.2 | Processus RH — Workflows | W12.1 | ⬜ |
| W12.3 | Processus RH — Courriers et formulaires | W12.2 | ⬜ |
| W13 | Module Pilotage | W12 | ⬜ |
| W14 | Module Masse salariale | W13 | ⬜ |
| W15 | Module Talents | W14 | ⬜ |
| W16 | Module Identité | W15 | ⬜ |

## FluxyRH Entreprise (`FluxyRH-mobile/entreprise/`)

| Code | Module | Dépend de | Statut |
|---|---|---|---|
| E00 | Amorçage | W16 | ⬜ |
| E01 | Connexion, accès et administration | E00 | ⬜ |
| E02 | Dossier | E01 | ⬜ |
| E03 | Carte NFC | E02 | ⬜ |
| E04 | Pointage et temps | E03 | ⬜ |
| E05 | Congés | E04 | ⬜ |
| E06 | Contrats | E05 | ⬜ |
| E07 | Paie | E06 | ⬜ |
| E08 | Communication | E07 | ⬜ |
| E09 | Modules | E08 | ⬜ |
| E10 | Marque blanche et publication | E09 | ⬜ |

## FluxyRH Borne (`FluxyRH-mobile/borne/`)

| Code | Module | Dépend de | Statut |
|---|---|---|---|
| B00 | Amorçage | E10 | ⬜ |
| B01 | Appairage | B00 | ⬜ |
| B02 | Pointage | B01 | ⬜ |
| B03 | Activation de carte et secours | B02 | ⬜ |

## FluxyRH Console (`FluxyRH-mobile/console/`)

| Code | Module | Dépend de | Statut |
|---|---|---|---|
| C00 | Amorçage | B03 | ⬜ |
| C01 | Encodage des cartes | C00 | ⬜ |
| C02 | Suivi des entreprises | C01 | ⬜ |

## Mise en production

| Code | Module | Dépend de | Statut |
|---|---|---|---|
| MEP | Serveur, déploiement, sauvegardes, supervision, publication des apps | C02 | ⬜ |
