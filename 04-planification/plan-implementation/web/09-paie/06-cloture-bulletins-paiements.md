# W09.6 — Paie · Clôture, bulletins, paiements (PAIE, SYS, EMP)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.5 · Suite : W09.7 (avances), W09.8 (journaux)

## 1. Objet

Clore la période et en tirer ce qui sort de la paie : **PDF des bulletins** figés, **publication** dans l'espace de l'employé, **accusé de réception** dans le système, **verrouillage définitif** des données de la période, **cumuls annuels**, **suivi des paiements** et **ouverture de la période suivante** (proposée ou automatique). Les **paiements se font hors de FluxyRH** (virements, espèces, mobile money) : le gestionnaire de paie y **enregistre seulement** le résultat (payé ou en échec, moyen, date, référence). À la fin de W09.6, le cycle complet d'une période de paie fonctionne de l'ouverture à la suivante.

## 2. Ce que chacun reçoit, produit, transmet

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **PAIE** | Période `Approuvée` (W09.5) | Clôture ; enregistrement des paiements faits hors système ; ouverture de la suivante | Employés ; Conformité (W11) |
| **SYS** | Clôture | PDF figés, bulletins `publie`, verrouillage, notifications ; ouverture automatique si activée | Employés |
| **EMP** | Bulletin publié | Accusé de réception | — |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-05 (fin) | `Approuvée` → `Clôturée` : bulletins publiés, période verrouillée |
| F-PAY-06 (fin) | Dernière étape de la checklist : ouverture de la période suivante, proposée ou automatique |
| F-PAY-07 | Bulletin PDF, publication, accusé de réception, réimpression |
| F-PAY-08 | Statut de paiement par bulletin, enregistré par le PAIE ; paiements faits hors système |
| F-EMP-08 | Cumuls annuels |
| T-13 | PDF figés avec empreinte |

À lire : PRD §7.9 ; TRD §14.3 ; APPFLOW §5.10, §6.5 (S-57), §6.8 (S-65, S-68), §7, §8 (ouverture des périodes) ; BACKEND SCHEMA §5.9 (`payslips`), §8 ; UX/UI §13.1, §13.2.

## 4. Prérequis et décisions

W09.5 livré.

| Sujet | Proposition |
|---|---|
| Paiements hors système | FluxyRH **ne produit aucun fichier de virement** : les tables `bank_transfer_formats`, `bank_transfer_format_columns`, `bank_transfer_exports` et l'écran S-58 « formats » sont retirés (BACKEND SCHEMA, APPFLOW, TRD §16.3 et PRD F-PAY-08 mis à jour). Le PAIE paie par ses moyens habituels, puis enregistre le résultat dans S-57 |
| Informations utiles au paiement | S-57 montre au PAIE, pour chaque bulletin, le net à payer et le compte principal **vérifié** de l'employé (ou l'absence de compte vérifié), pour qu'il puisse payer hors système ; aucune action de paiement n'est faite par FluxyRH |
| Dossier incomplet | Ne bloque plus de virement (il n'y en a plus dans FluxyRH) : S-57 signale seulement « dossier incomplet » et « compte non vérifié » à côté du bulletin. F-EMP-09 mis à jour : le dossier incomplet bloque les congés et les formulaires types |
| Correction après clôture | Impossible sur la période : un bulletin publié n'est jamais régénéré. La correction passe par la période suivante (montant ponctuel de rappel ou de retenue, W09.4) |
| Réimpression | Toujours le **même** PDF figé (même empreinte), jamais un nouveau rendu |
| Paiement en échec | `echec` → `paye` permis (nouvelle tentative) avec motif ; `paye` est définitif |
| Accusé de réception | Dans le système, avec ou sans carte (décision de W05 sur la signature d'actions) |
| Verrouillage | À la clôture : pointages reçus pour la période refusés (« période clôturée », reporté de W06.2), corrections de journées et d'heures sup, annulations de congés (reportées de W06.3, W07) refusées |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Période | `approuvee` → `cloturee` | PAIE |
| Bulletin | `calcule` → `publie` | SYS à la clôture |
| Paiement `payment_status` | `a_payer` → `paye` / `echec` ; `echec` → `paye` | PAIE (enregistrement d'un paiement fait hors système) |
| Checklist | `publication`, `paiements`, `ouverture_periode_suivante` → `fait` | SYS ; PAIE |

## 6. Étapes ordonnées

### W09.6.1 — Enums, permissions, spécification

- `PayslipStatus`, `PaymentStatus`, `PaymentChannel` (W04.2) ; permission `payments` ; l'étape de checklist `virements` devient `paiements`.
- BACKEND SCHEMA (§5.9 sans les tables de virement ; colonnes `paid_at`, `payment_channel`, `payment_reference` sur `payslips`), APPFLOW §5.10 et §6.5, TRD §16.3, PRD F-PAY-08 et F-EMP-09 mis à jour.

### W09.6.2 — Clôture et publication

- `PayrollPeriodService::close(period)` : période `approuvee`, job de génération des PDF par lots (`DocumentRenderer`, gabarit UX/UI §13.2 : rubriques, totaux, **net en lettres** par `Money`, cumuls annuels, mode de paiement), écriture non écrasable, `pdf_hash`, bulletins `publie`, période `cloturee`, `closed_by`, journal, notification aux employés (sans montant).
- Verrouillage (§4) : contrôle « période clôturée » ajouté à `ClockingService`, `AttendanceCorrectionService`, `OvertimeService`, `LeaveService`.

**Critère de fin** : un pointage, une correction, une annulation de congé sur une période clôturée sont refusés ; un PDF ne peut être ni écrasé ni régénéré.

### W09.6.3 — Bulletins de l'employé et cumuls

- `App\Services\Payroll\PayslipService` : cumuls annuels calculés depuis les bulletins publiés (brut, net, cotisations, impôt), jamais stockés (BACKEND SCHEMA §5.9).
- S-65 `/me/payslips` : bulletins par année, téléchargement, cumuls annuels ; élément « bulletin à accuser » dans S-68.
- Accusé de réception : `ActionSignatureService` (action `bulletin`, empreinte du PDF), `acknowledged_signature_id` ; mention sur l'écran (le PDF reste celui de la clôture).
- Fiche S-21, onglet Rémunération (PAIE, DIR) : bulletins de l'employé ; consultation journalisée (`sensitive_data_views`).

### W09.6.4 — Ouverture de la période suivante

- Dernière étape de la checklist : à la clôture, si `auto_open_next_period` est actif pour la fréquence, le système ouvre la période suivante (étape cochée « Système ») ; sinon l'action est proposée au PAIE.

### W09.6.5 — Enregistrement des paiements

- `App\Services\Payroll\PaymentRecordService` : marquer `paye` (moyen, date, référence facultative) ou `echec` (motif), un par un ou par sélection ; journal.
- S-57 `/payments` : bulletins d'une période par statut de paiement ; net, compte principal vérifié, signalements « dossier incomplet » et « compte non vérifié » ; enregistrement individuel et groupé ; export de la liste (XLSX, CSV) pour le suivi interne, réservé aux rôles autorisés sur `bancaire` (PAIE, DIR) et journalisé.

**Critère de fin** : tous les bulletins d'une période peuvent être marqués payés en une action ; un paiement `paye` ne peut plus changer.

### W09.6.6 — API

- `/api/v1/employee/payslips` (liste, PDF, cumuls, accusé), `/payroll/payroll-periods/{id}/close`, `/payroll/payments` (liste, enregistrement).
- Contrat Scramble à jour.

### W09.6.7 — Documentation et livraison

- `02-reference/` : clôture, verrouillage, bulletins, cumuls, enregistrement des paiements.
- `05-recette/` : scénario complet d'une période (ouverture → variables → calcul → contrôle → approbation → clôture → paiements enregistrés → suivante).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.6 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Clôture | Préalable `approuvee`, PDF figés et empreintes, publication, notification sans montant |
| Verrouillage | Pointage, correction, heures sup, congé sur période clôturée refusés |
| Bulletins | PDF fr et ar, net en lettres, réimpression identique, accusé de réception |
| Cumuls | Exactitude sur une année, employé entré en cours d'année |
| Suivante | Ouverture automatique et proposée |
| Paiements | Enregistrement individuel et groupé, transitions, `echec` → `paye`, `paye` définitif, signalements |
| Non-fuite | RH, ADM, MGR : aucun bulletin, aucune coordonnée bancaire, aucun export de paiements |
| Droits | `payments` ; employé limité à ses bulletins ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W09.6 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.10 de bout en bout.
- Documentation et livraison de W09.6.7 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Échéances d'avance prélevées | W09.7 |
| Journal de paie, états de cotisations | W09.8 |
| Déclarations, export comptable | W11 |
| Charte graphique du bulletin | W16 |
| Bulletins et accusé dans l'app | E07 |
