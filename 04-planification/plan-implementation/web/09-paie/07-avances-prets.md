# W09.7 — Paie · Avances et prêts (EMP → PAIE → DIR → SYS)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.6 · Suite : W09.8 (journaux et états)

## 1. Objet

Permettre, si l'entreprise l'active, les **avances et prêts sur salaire** : demande de l'employé contrôlée par la politique de l'entreprise, acceptation par le gestionnaire de paie, approbation par la direction, échéancier, **prélèvement automatique** à chaque paie jusqu'au solde. À la fin de W09.7, une avance approuvée apparaît en retenue sur les bulletins suivants et se solde d'elle-même.

## 2. Ce que chacun reçoit, produit, transmet

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **EMP** | Politique de l'entreprise | Demande (montant, échéances, motif) | PAIE |
| **PAIE** | Demande | `Acceptée` / `Refusée` ; report d'une échéance | Direction |
| **DIR** | Demande acceptée (S-81) | `Approuvée` / `Refusée` | SYS : échéancier |
| **SYS** | Échéancier ; clôtures de paie | Retenues sur les bulletins ; `En remboursement` → `Soldée` | Employé, PAIE |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-10 | Politique de l'entreprise ; `Demandé` → `Accepté` → `Approuvé` / `Refusé` → `En remboursement` → `Soldé` ; retenues sur les paies suivantes |

À lire : PRD §7.9 ; TRD §14.3 ; APPFLOW §5.11, §6.5 (S-59), §6.6 (S-81), §6.8 (S-67) ; BACKEND SCHEMA §5.1 (`advance_policies`), §5.9 (avances), §6, §7.

## 4. Prérequis et décisions

W09.6 livré.

| Sujet | Proposition |
|---|---|
| Réglage de la politique | Onglet **Avances** de S-50 (PAIE) : activation, plafond en % du dernier net publié, nombre maximal d'échéances, ancienneté minimale, nombre maximal en cours |
| Versement | Le versement de l'avance à l'employé se fait **hors paie** (caisse, virement manuel), comme tous les paiements (FluxyRH ne paie pas) ; le PAIE saisit la date de versement à l'approbation, ce qui déclenche l'échéancier |
| Échéancier | Montant divisé par le nombre d'échéances, l'arrondi porté sur la dernière ; première échéance sur la première période de la fréquence de l'employé dont les variables ne sont pas encore validées |
| Montants dans la paie | Les échéances restent chiffrées (`advance_loan_installments.amount`) : le moteur les lit directement ; la variable de période (`source` = `avance`) ne porte que la référence de l'échéance, jamais son montant |
| Net insuffisant | Le PAIE peut **reporter** une échéance à la fin de l'échéancier (motif, journal) |
| Sortie de l'employé | À la déclaration de sortie, les échéances restantes sont regroupées sur la dernière période et le PAIE est alerté |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Avance `advances_loans.status` | `demande` → `acceptee` → `approuvee` → `en_remboursement` → `soldee` ; `refusee` (motif) depuis `demande` ou `acceptee` | EMP ; PAIE ; DIR ; SYS (première retenue publiée, dernière retenue publiée) |
| Échéance | `a_prelever` → `preleve` (à la clôture de la période) | SYS |

## 6. Étapes ordonnées

### W09.7.1 — Enums et permissions

- `AdvanceKind`, `AdvanceStatus`, `InstallmentStatus` ; permission `advances` ; `SensitiveField` : montants des avances et des échéances en `remuneration_paie`.

### W09.7.2 — Données et politique

- Migrations `advance_policies`, `advances_loans`, `advance_loan_installments`.
- Onglet Avances de S-50 (§4).

### W09.7.3 — Service

- `App\Services\Payroll\AdvanceLoanService` : `request()` (politique : activée, plafond, ancienneté, nombre en cours ; refus immédiat motivé), `accept()`, `refuse(reason)`, `approve(disbursedOn)` (échéancier), `postpone(installment, reason)`, `onPeriodClosed(period)` (échéances `preleve`, passage `en_remboursement` puis `soldee`), regroupement à la sortie ; journal ; notifications.
- Branchement sur le moteur (W09.4) : contexte « échéance due » par employé, rubrique de retenue désignée par le PAIE dans l'onglet Avances ; variable de période de référence (§4).
- Bulletin doré « avance en remboursement » ajouté (W09.4.4).

### W09.7.4 — Écrans

- S-67 `/me/requests` (onglet Avances) : demande avec les règles affichées, suivi, échéancier.
- S-59 `/advances` (PAIE) : demandes, accepter, refuser, échéanciers, reports.
- Élément « avance à approuver » dans S-81 (DIR).

### W09.7.5 — API et documentation

- `/api/v1/employee/advances` (politique, demande, suivi), `/payroll/advances`, `/direction/approvals` (avances).
- `02-reference/` : politique, circuit, échéancier, prélèvement.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.7 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Politique | Désactivée, plafond, ancienneté, nombre en cours ; refus immédiat motivé |
| Circuit | Chaque transition, transitions interdites, refus à chaque étape |
| Échéancier | Division et arrondi, première période, report, regroupement à la sortie |
| Paie | Bulletin doré « avance » ; retenue prélevée à la clôture ; `soldee` après la dernière |
| Non-fuite | RH, ADM, MGR : aucun montant ; variable de période sans montant |
| Droits | `advances` ; employé limité à ses demandes ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W09.7 verts, dont le bulletin doré « avance » ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.11 jusqu'au solde sur trois périodes du jeu de démonstration.
- Documentation et livraison de W09.7.5 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Demandes d'avance dans l'app | E07 |
| Formulaires types (autre onglet de S-67) | W12.3 |
