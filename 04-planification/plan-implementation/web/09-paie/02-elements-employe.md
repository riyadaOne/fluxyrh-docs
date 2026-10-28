# W09.2 — Paie · Éléments par employé (PAIE)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.1 · Suite : W09.3 (variables)

## 1. Objet

Rassembler, pour chaque employé, ce que la paie sait de lui avant toute période : **salaire de base** lu dans le contrat actif (jamais ressaisi), **rubriques fixes individuelles** (primes, indemnités, retenues permanentes) saisies par le gestionnaire de paie avec leurs dates, **fréquence de paie**. Ces montants sont des données sensibles de catégorie `remuneration_paie` : le RH ne les voit pas. À la fin de W09.2, chaque employé payable a une rémunération complète et cohérente avec le paramétrage en vigueur.

## 2. Ce que le gestionnaire de paie reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Contrats actifs (W08.4), rubriques par code (W09.1), dossiers (W04) | Rubriques fixes datées par employé ; fréquence de paie confirmée | **Moteur** (W09.4) ; **checklist** (W09.3) : anomalies (sans contrat actif, rubrique absente de la version) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-04 | Salaire de base issu du contrat actif ; autres rubriques fixes saisies par le PAIE |
| F-PAY-05 (fréquence) | Fréquence fixée par employé, défaut issu du type |
| F-ADM-04, NF-02 | Catégorie `remuneration_paie` : PAIE, direction, employé concerné |

À lire : PRD §6 (P6), §7.4 (propriété des données), §7.9 ; TRD §9 ; APPFLOW §4.5, §6.5 (S-51) ; BACKEND SCHEMA §5.9 (`employee_rubric_assignments`), §8.

## 4. Prérequis et décisions

W09.1 livré.

| Sujet | Proposition |
|---|---|
| Rubriques individualisables | Seules les rubriques de nature `gain`, `retenue` ou `information`, en mode `fixe` ou `pourcentage`, peuvent être affectées à un employé ; la valeur individuelle remplace celle de la rubrique. Les cotisations et impôts ne s'affectent jamais individuellement |
| Rubrique absente d'une version | Une affectation dont le code n'existe pas dans la version applicable est ignorée au calcul et signalée comme anomalie bloquante de la checklist (W09.3) |
| Changement de fréquence | Par le PAIE, avec date d'effet au début d'une période non encore ouverte ; journalisé |
| Affectation groupée | Une même rubrique (ex. prime de transport) affectée à une sélection d'employés (structure, site, type), chaque ligne restant individuelle |
| Salaire de base | Affiché en lecture seule depuis le contrat actif ; une modification passe par un avenant (W08.4) |

## 5. Statuts traversés

Aucun cycle de vie : les affectations sont datées (`starts_on`, `ends_on`) ; une affectation passée n'est jamais modifiée, on la clôt et on en crée une nouvelle.

## 6. Étapes ordonnées

### W09.2.1 — Permissions et champs sensibles

- Permission `employee_compensation` ; `SensitiveField` : `employee_rubric_assignments.amount`, `rate` en `remuneration_paie`.

### W09.2.2 — Données et service

- Migration `employee_rubric_assignments` (colonnes `enc`).
- `App\Services\Payroll\CompensationService` : affecter (règles du §4), clore, remplacer, affectation groupée ; `fixedRubricsFor(employee, date)` ; `baseSalaryFor(employee, date)` (contrat actif, W08.4) ; changement de fréquence ; journal avec valeurs chiffrées.
- Anomalies exposées pour la checklist : employé payable sans contrat actif, affectation dont la rubrique est absente de la version applicable.

### W09.2.3 — Écran S-51

- S-51 `/employee-compensation` : liste des employés payables (types qui entrent dans la paie), fréquence, salaire de base, nombre de rubriques fixes, anomalies ; fiche de rémunération : rubriques en cours et historique, ajout, clôture, remplacement ; affectation groupée.
- Onglet **Rémunération** de la fiche S-21, visible selon `FieldAccess` (PAIE, DIR).

**Critère de fin** : un RH délégué sur l'écran `employee_compensation` voit la liste mais **aucun** montant (APPFLOW §6.5) ; l'ADM n'y a aucun accès.

### W09.2.4 — Confidentialité

- Tests de non-fuite sur S-51, la fiche, le journal d'audit, l'API et les exports : aucune valeur pour ADM, RH, MGR.
- Consultation d'une fiche de rémunération par un tiers journalisée (`sensitive_data_views`).

### W09.2.5 — API et documentation

- `/api/v1/payroll/compensation` (liste, fiche, affectations).
- `02-reference/` : rémunération par employé, règles d'affectation.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.2 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Affectations | Rubrique individualisable ou non, dates, clôture, remplacement, groupée |
| Lecture | Salaire de base du contrat actif à une date ; rubriques fixes à une date |
| Anomalies | Sans contrat actif ; rubrique absente de la version |
| Non-fuite | ADM, RH (même délégué), MGR : aucun montant |
| Droits | `employee_compensation` ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W09.2 verts, dont la non-fuite ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Rémunérations complètes pour le jeu de démonstration.
- Documentation et livraison de W09.2.5 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Anomalies dans la checklist | W09.3 |
| Calcul | W09.4 |
| Modèles de rémunération appliqués à des populations | W14 |
