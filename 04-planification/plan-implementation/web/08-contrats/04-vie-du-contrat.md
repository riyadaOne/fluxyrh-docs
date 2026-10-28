# W08.4 — Contrats · Vie du contrat (SYS, RH)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W08.3 · Clôt le module W08

## 1. Objet

Faire vivre le contrat signé : **activation** automatique à sa date de début (le précédent se termine), **un seul contrat actif** par employé, **avenants**, **alertes d'échéance** (CDD, période d'essai, stage), **terminaison** à l'échéance et **résiliation** motivée par le RH, en lien avec la sortie de l'employé. À la fin de W08.4, chaque employé a au plus un contrat actif, que la paie (W09.2) lit pour le salaire de base.

## 2. Ce que le système et le RH reçoivent, produisent, transmettent

| Acteur | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **SYS** | Contrats `Signé` (W08.3) | Contrat `Actif` ; précédent `Terminé` ; contrat échu `Terminé` ; alertes | **Paie** (W09.2) : contrat actif ; **RH**, **manager** : échéances |
| **RH** | Contrats actifs, alertes | Avenants (même circuit W08.2 → W08.3), résiliations | Employé, direction ; **sortie** de l'employé (W04.1.7, W12.2) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-CTR-02 (fin) | `Signé` → `Actif` → `Terminé` / `Résilié` (motif, date, type) |
| F-CTR-03 | Un seul contrat actif, avenants, alerte d'échéance |

À lire : PRD §7.8 ; TRD §11.2 ; APPFLOW §5.9, §5.10 (contrôle de la paie) ; BACKEND SCHEMA §5.1 (`reminder_settings`), §5.8, §6, §8 ; UX/UI §6.1.

## 4. Prérequis et décisions

W08.3 livré.

| Sujet | Proposition |
|---|---|
| Activation tardive | Un contrat signé après sa date de début est activé immédiatement, avec sa date de début d'origine |
| Avenant | Un avenant est un **nouveau contrat complet**, lié au contrat modifié (`amends_contract_id`), créé en copiant ses blocs et conditions, rédigé et signé par le même circuit. À son activation, le contrat modifié passe `termine` la veille de la date d'effet de l'avenant |
| Contrat échu | À `ends_on`, le contrat passe `termine` ; l'employé n'est **pas** sorti automatiquement : le RH est alerté (nouveau contrat, avenant de prolongation ou déclaration de sortie). Un employé sans contrat actif est signalé par la checklist de paie (W09.3) |
| Résiliation | Le RH saisit le type (`TerminationType`), le motif, la date d'effet et, s'il y a lieu, le document (lettre) ; le contrat reste `actif` jusqu'à la date d'effet, puis passe `resilie` par le système. En saisissant la résiliation, le RH répond à la question « **Déclarer la sortie de l'employé à cette date ?** » ; s'il répond oui, la sortie (W04.1.7) est déclarée avec la même date et le même type ; avec le module Processus RH, le lancement du workflow de sortie est proposé au RH (W12.2) |
| Sortie d'un employé au contrat actif | **Pas de sortie sans résiliation** : déclarer la sortie (W04.1.7) d'un employé dont le contrat est actif propose d'abord la résiliation (date, type, motif) ; la sortie n'est enregistrée qu'avec elle |
| Alertes | `contract_end_notice_days` (30 jours) pour la fin de CDD, de stage et de période d'essai ; au RH et au manager |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Contrat | `signe` → `actif` (à `starts_on`) ; `actif` → `termine` (à `ends_on`, ou remplacé par un contrat ou un avenant) ; `actif` → `resilie` (à la date d'effet de la résiliation) | SYS ; RH saisit la résiliation |

`termine` et `resilie` sont définitifs.

## 6. Étapes ordonnées

### W08.4.1 — Enums et spécification

- `TerminationType` (créé en W04.1) réutilisé ; APPFLOW §5.9 et BACKEND SCHEMA §6 précisés (avenant, contrat échu, résiliation datée).

### W08.4.2 — Données

- Migration : ajout à `contracts` de `amends_contract_id`, `ended_at`, `termination_type`, `termination_reason`, `termination_document_id`, `termination_effective_on` (date d'effet, BACKEND SCHEMA mis à jour).
- Migration : `contract_end_notice_days` ajouté à `reminder_settings` ; onglet Relances de la Configuration complété.

### W08.4.3 — Activation et fin

- `ContractService::activate(contract)` : un seul `actif` par employé (le précédent passe `termine`), en transaction, journal `logAsSystem`, notification au RH et à l'employé.
- Tâche planifiée quotidienne (fuseau de l'entreprise) : activations du jour, terminaisons à l'échéance, résiliations arrivées à leur date d'effet.
- `ContractService::activeFor(employee, date)` : contrat actif à une date (lu par la paie).

**Critère de fin** : avec horloge simulée, activation, remplacement et échéance se produisent au bon jour ; deux contrats actifs sont impossibles, même en cas de tâche relancée.

### W08.4.4 — Avenants

- `ContractService::draftAmendment(contract)` : copie des blocs et conditions dans un nouveau brouillon lié ; même rédaction (W08.2) et même signature (W08.3).
- S-40 : historique des contrats et avenants d'un employé, différences entre un contrat et son avenant.

### W08.4.5 — Échéances et alertes

- Tâche planifiée : alertes avant la fin d'un CDD, d'un stage, d'une période d'essai ; alerte au jour de l'échéance si aucun contrat suivant n'est signé.
- S-40 : filtre « échéances à venir » ; widget sur le tableau de bord du RH.

### W08.4.6 — Résiliation

- `ContractService::terminate(contract, type, reason, effectiveOn, ?document)` : RH, motif obligatoire ; document déposé comme pièce RH du dossier ; journal ; notification à l'employé et à la direction ; question « déclarer la sortie à cette date ? » (§4).
- Branchement sur `EmployeeService::declareExit()` (W04.1.7) : si un contrat est actif, la résiliation est demandée d'abord (§4).

### W08.4.7 — API

- `/api/v1/hr/contracts` complété (avenant, résiliation, échéances), `/employee/contracts` (contrat actif et historique).
- Contrat Scramble à jour.

### W08.4.8 — Documentation et livraison

- `02-reference/` : activation, avenants, échéances, résiliation, lien avec la sortie.
- `05-recette/` : scénario complet du contrat (modèle → rédaction → signatures simulées → activation → avenant → résiliation).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W08.4 (et W08) dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Activation | Date de début future, passée (activation tardive), remplacement du précédent, unicité de l'actif, idempotence de la tâche |
| Fin | Échéance, résiliation datée, transitions interdites depuis `termine` et `resilie` |
| Avenant | Copie, circuit complet, terminaison du contrat modifié la veille |
| Alertes | Fin de CDD, de stage, de période d'essai ; une alerte par échéance |
| Sortie | Résiliation avec sortie déclarée à la même date ; sortie d'un employé au contrat actif impossible sans résiliation |
| Non-fuite | Salaire masqué dans les alertes, notifications, historique pour ADM et MGR |
| Droits | `contracts` ; délégation ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W08.4 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.9 de bout en bout (signatures simulées).
- Documentation et livraison de W08.4.8 faites ; W08 complet dans la ROADMAP.

## 9. Reporté

| Élément | Module |
|---|---|
| Salaire de base lu par la paie, contrôle « sans contrat actif » | W09.2, W09.3 |
| Workflow de sortie | W12.2 |
| Contrat dans l'app | E06 |
