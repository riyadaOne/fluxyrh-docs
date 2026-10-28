# W09.3 — Paie · Période et variables (PAIE ouvre, RH valide)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.2 · Suite : W09.4 (calcul et contrôle)

## 1. Objet

Ouvrir une **période de paie** par fréquence, avec sa **checklist** à étapes bloquantes, puis laisser le RH rassembler et valider les **variables** de la période : jours travaillés, absences, congés non payés, heures sup validées, saisies manuelles. La validation fait passer la période `Variables validées` et gèle les données de temps de la période. À la fin de W09.3, la période est prête à être calculée (W09.4).

## 2. Ce que le PAIE et le RH reçoivent, produisent, transmettent

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **PAIE** | Fréquences utilisées (W09.1) | Période `Ouverte` (la première de chaque fréquence ; les suivantes en W09.6) | RH |
| **RH** | Journées (W06), heures sup validées (W06.4), congés validés (W07), rémunérations et anomalies (W09.2) | Variables de la période ; checklist RH complète ; `Variables validées` | **PAIE** (W09.4) : période calculable |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-05 (début) | Période par fréquence ; `Ouverte` → `Variables validées` (RH : présences, congés, heures sup, événements) |
| F-PAY-06 | Checklist intégrée, étapes bloquantes |
| F-TPS-06 (fin) | Heures sup validées intégrées aux variables de paie |
| F-ABS-01 (impact) | Congés non payés en variables |

À lire : PRD §7.9 ; TRD §14.3 ; APPFLOW §5.10, §6.5 (S-52, S-53, S-55), §7 ; BACKEND SCHEMA §5.6 (`payroll_period_id`), §5.9, §7 (`PayrollChecklistStep`, `PayrollVariableSource`), §8 ; UX/UI §6.6.

## 4. Prérequis et décisions

W09.2 livré.

| Sujet | Proposition |
|---|---|
| Bornes d'une période | `mensuelle` : mois civil ; `quinzaine` : 1–15 et 16–fin ; `hebdomadaire` : lundi–dimanche ; `journaliere` : un jour. Une période par fréquence **utilisée**, jamais deux ouvertes à la fois pour une même fréquence |
| Employés d'une période | Employés de cette fréquence dont une période d'emploi chevauche la période, et dont le type entre dans la paie |
| Gel des données de temps | Après `Variables validées`, les corrections de journées, heures sup et congés touchant la période sont refusées (motif « variables validées ») ; pour les rouvrir, le RH ramène la période à `Ouverte` |
| Retour à `Ouverte` | Non prévu par les spécifications. Proposition : le RH (ou le PAIE qui détecte une erreur) peut ramener la période à `Ouverte` tant qu'elle n'est pas `controlee` ; les bulletins calculés sont alors supprimés. BACKEND SCHEMA §6 mis à jour |
| Variables d'avances | Source `avance` ajoutée par W09.7 ; **pas de variable issue des événements RH** en v1 (décision de W12.1) ; la source `saisie` permet dès W09.3 une variable manuelle motivée |
| Montants dans les variables | Les variables sont des **quantités** (jours, minutes, nombre) ; le RH voit les montants de la paie, mais la saisie d'un montant reste réservée au PAIE (W09.4), pour séparer celui qui valide les présences de celui qui saisit la rémunération (décision 0003) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Période `payroll_periods.status` | (création) `ouverte` → `variables_validees` ; retour à `ouverte` (§4) | PAIE ouvre ; RH valide |
| Élément de checklist | `a_faire` → `fait` / `ignore` (motif, seulement pour un élément non bloquant) ; recalculé automatiquement pour les contrôles | SYS ; RH, PAIE |

## 6. Étapes ordonnées

### W09.3.1 — Enums, permissions, spécification

- `PayrollPeriodStatus`, `PayrollChecklistStep` (liste fermée complète, dernière étape `ouverture_periode_suivante`), `ChecklistItemStatus`, `PayrollVariableSource` ; permissions `payroll_variables`, `payroll_checklist`, `payroll_compute` (ouverture).
- BACKEND SCHEMA §6 (retour à `ouverte`) mis à jour.

### W09.3.2 — Périodes

- Migrations `payroll_periods`, `payroll_checklist_items`, `payroll_period_variables` ; ajout de `payroll_period_id` à `attendance_days` et `overtime_entries`.
- `App\Services\Payroll\PayrollPeriodService` : `open(frequency, startsOn)` (bornes, unicité, période précédente de la fréquence clôturée sauf pour la première), `employeesOf(period)`, transitions avec vérification de l'état de départ, journal.

### W09.3.3 — Checklist

- `App\Services\Payroll\PayrollChecklistService` : éléments créés à l'ouverture, dans l'ordre de l'enum ; contrôles automatiques des étapes RH : embauches (employés entrés avec contrat actif), sorties (sortants traités), contrats actifs (W09.2), heures sup (aucune `declaree` non décidée sur la période), congés (aucune demande en cours sur la période), variables (collecte faite), anomalies de rémunération (W09.2) ; les étapes de calcul, contrôle, approbation, publication, virements et ouverture de la suivante sont tenues par W09.4 à W09.6.
- Une transition est refusée tant qu'un élément bloquant de son étape n'est pas `fait`.

### W09.3.4 — Variables

- `App\Services\Payroll\PayrollVariableService::collect(period)` : par employé, jours ouvrés, jours travaillés, absences non justifiées, jours de congé non payé, minutes d'heures sup **validées** par règle (`HEURES_SUP_<taux>`), avec leur source (`pointage`, `conge`, `heures_sup`) ; relançable tant que la période est `ouverte`.
- Saisie manuelle motivée d'une variable de quantité (`saisie`).
- `validate(period)` : checklist RH complète, rattachement des journées et heures sup à la période, gel (§4), `variables_validees`, notification au PAIE.
- `reopen(period, reason)` (§4).

**Critère de fin** : les variables d'un mois du jeu de démonstration correspondent aux feuilles de temps (W06.4) et aux congés non payés ; une correction de journée sur une période validée est refusée.

### W09.3.5 — Écrans

- S-53 `/payroll-periods/{id}` : page de la période (UX/UI §6.6) : frise des statuts, checklist à gauche, contenu de l'étape à droite, un seul bouton principal désactivé avec sa raison ; liste des périodes par fréquence ; ouverture de la première période (PAIE).
- S-52 `/payroll-periods/{id}/variables` (RH) : variables par employé et par source, écarts avec la période précédente, saisie manuelle, collecte, validation.
- S-55 `/payroll-periods/{id}/checklist` (RH, PAIE) : éléments avec leur lien de résolution.
- Barre latérale : groupe « Paie » (Périodes).

### W09.3.6 — API et documentation

- `/api/v1/hr/payroll-periods/{id}/variables` (lecture, validation), `/payroll/payroll-periods` (liste, ouverture).
- `02-reference/` : périodes, checklist, variables, gel des données.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.3 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Périodes | Bornes par fréquence, unicité, une seule ouverte par fréquence, employés concernés (entrée, sortie en cours de période) |
| Checklist | Chaque contrôle bloquant, élément ignoré avec motif, transition refusée tant qu'un bloquant reste |
| Variables | Collecte exacte, heures sup validées seulement, congés non payés, saisie manuelle motivée |
| Gel | Correction de journée, d'heures sup, annulation de congé refusées après validation ; retour à `ouverte` |
| Transitions | Interdites (ex. `ouverte` → `calculee`) |
| Non-fuite | Un manager ou un ADM délégué ne voit aucun montant dans S-52, S-53, S-55 ; le RH voit sans saisir |
| Droits | `payroll_variables`, `payroll_checklist`, `payroll_compute` ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W09.3 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.10 jusqu'à `Variables validées`.
- Documentation et livraison de W09.3.6 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Calcul, contrôle, montants manuels | W09.4 |
| Ouverture automatique de la période suivante, clôture et verrouillage définitif | W09.6 |
| Variables d'avances | W09.7 |
