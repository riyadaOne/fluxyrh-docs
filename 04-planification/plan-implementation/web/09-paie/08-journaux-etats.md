# W09.8 — Paie · Journaux et états (PAIE, DIR, RH en lecture)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.6 · Clôt le module W09

## 1. Objet

Produire les états réglementaires et de gestion de chaque période : **journal de paie** (livre de paie : une ligne par employé, une colonne par rubrique) et **états de cotisations** (base, part salariale, part patronale par rubrique de cotisation et d'impôt), consultables à l'écran et exportables. Ces états servent au contrôle interne, à l'expert-comptable et, plus tard, au module Conformité (W11). À la fin de W09.8, le module Paie du socle est complet.

## 2. Ce que le gestionnaire de paie et la direction reçoivent, produisent, transmettent

| Reçoit | Produit | Transmet à |
|---|---|---|
| Bulletins et lignes d'une période (W09.4, W09.6) | Journal de paie, états de cotisations, exports | Expert-comptable, organismes (hors système) ; **Conformité** (W11) : mêmes agrégats |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-09 | Journal de paie et états de cotisations par période, export |

À lire : PRD §7.9 ; TRD §9.2 (agrégats sensibles), §9.3 ; APPFLOW §6.5 ; BACKEND SCHEMA §5.9 (`payslip_lines`), §9 (point 2) ; UX/UI §6.1, §13.1.

## 4. Prérequis et décisions

W09.6 livré (W09.7 n'est pas un prérequis).

| Sujet | Proposition |
|---|---|
| Périodes concernées | États **définitifs** pour une période `cloturee` ; états **provisoires** (mention « Provisoire » sur l'écran et les exports) dès `calculee`, pour le contrôle |
| Regroupement des cotisations | Par rubrique (nature `cotisation` ou `impot`, part salariale et patronale) : le paramétrage ne connaît pas d'« organisme » ; le PAIE nomme ses rubriques avec l'organisme concerné, ce qui suffit au regroupement visuel |
| Formats | Journal : XLSX et CSV ; états de cotisations : PDF (`DocumentRenderer`) et XLSX |
| Calcul | Agrégats faits en PHP sur les lignes déchiffrées (colonnes chiffrées, TRD §9.3) |

## 5. Étapes ordonnées

### W09.8.1 — Service

- `App\Services\Payroll\PayrollReportService` : `ledger(period)` (employés × rubriques, totaux par colonne, contrôle « somme des nets = total des nets »), `contributions(period)` (par rubrique : base, taux, part salariale, part patronale, totaux), mention provisoire selon le statut.

### W09.8.2 — Écrans et exports

- Onglet **États** de la page de période S-53 : journal de paie et états de cotisations ; filtres structure, site, type d'employé.
- Exports (§4), journalisés avec leur empreinte ; réservés aux rôles autorisés sur `remuneration_paie` (PAIE, DIR, RH en lecture).

### W09.8.3 — API et documentation

- `/api/v1/payroll/payroll-periods/{id}/ledger`, `/contributions` (lecture, export).
- `02-reference/` : journal et états.
- `05-recette/` : rapprochement des états avec les bulletins dorés.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.8 (et W09) dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Exactitude | Totaux du journal égaux à la somme des bulletins ; états de cotisations égaux aux lignes ; rapprochement avec les bulletins dorés |
| Statut | Provisoire dès `calculee`, définitif après `cloturee` |
| Exports | XLSX, CSV, PDF ; empreinte ; journal |
| Non-fuite | ADM, MGR : aucun accès, même par délégation d'écran |
| Droits | Autre entreprise ; API |

## 7. Critères de sortie

- Tests ciblés W09.8 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Rapprochement consigné dans `05-recette/`.
- Documentation et livraison de W09.8.3 faites ; W09 complet dans la ROADMAP.

## 8. Reporté

| Élément | Module |
|---|---|
| Déclarations CNPS et fiscales, bilan social, export comptable | W11 |
| Rapports de masse salariale | W13, W14 |
