# W09.4 — Paie · Calcul et contrôle (PAIE)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.3 · Suite : W09.5 (approbation)

## 1. Objet

Construire le **moteur de paie** et le travail du gestionnaire de paie sur une période : calcul de tous les bulletins en job par lots avec progression, bulletins **reproductibles** (lignes figées, version du paramétrage référencée), contrôle des écarts et anomalies, recalcul, montants ponctuels, puis passage `Contrôlée`. Les **bulletins dorés** deviennent la référence obligatoire de toute évolution du moteur (TRD §14.4). À la fin de W09.4, une période se calcule exactement, en moins d'une minute pour 200 employés.

## 2. Ce que le gestionnaire de paie reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Période `Variables validées` (W09.3) ; paramétrage (W09.1) ; rémunérations (W09.2) ; contrats actifs (W08.4) ; dossiers vérifiés (W04.3) | Bulletins `calcule` avec leurs lignes ; période `Calculée` puis `Contrôlée` | **Direction** (W09.5) : période à approuver |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-05 (suite) | `Variables validées` → `Calculée` → `Contrôlée` ; recalcul avant approbation |
| F-PAY-04 | Salaire de base du contrat actif ; rubriques fixes |
| NF-11 | 200 employés en moins d'une minute |
| T-12 | Calcul décimal, bulletins reproductibles, bulletins dorés |

À lire : PRD §7.9, annexe 14.3 ; TRD §14 (en entier), §9.3 (colonnes chiffrées) ; APPFLOW §5.10, §6.5 (S-53, S-54) ; BACKEND SCHEMA §5.9 (`payslips`, `payslip_lines`), §8, §9 (point 2) ; UX/UI §6.6.

## 4. Prérequis et décisions

W09.3 livré.

| Sujet | Proposition |
|---|---|
| Montants ponctuels | `payroll_period_variables.value` n'est pas chiffré : y saisir un montant exposerait une rémunération. Un montant ponctuel (prime exceptionnelle, rappel, retenue) est une **affectation de rubrique bornée à la période** (`employee_rubric_assignments`, chiffrée, W09.2), saisie par le PAIE depuis S-54 |
| Version du paramétrage | Celle applicable à la **date de fin** de la période, fixée sur la période au premier calcul et reprise sur chaque bulletin |
| Prorata | Entrée ou sortie en cours de période : `JOURS_TRAVAILLES` / `JOURS_OUVRES` appliqué par les formules du paramétrage de l'entreprise, pas par le moteur (le moteur ne connaît aucune règle métier codée) |
| Net négatif | Anomalie **bloquante** : la période ne peut pas passer `Contrôlée` ; le PAIE corrige (montant ponctuel, échéance d'avance reportée) |
| Seuil d'écart | Variation du net de plus de 20 % par rapport à la période précédente signalée (non bloquante) ; seuil en configuration |
| Bulletins dorés | Jeux de cas chiffrés de la TRD §14.4, calculés **à la main** sur un **paramétrage de test** (seeder de démonstration inspiré de l'annexe 14.3, décision 0002) et relus par le PAIE de RIYADA ONE |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Période | `variables_validees` → `calculee` → `controlee` ; `calculee` → `calculee` (recalcul) ; `controlee` → `calculee` (retour pour correction) | PAIE |
| Bulletin `payslips.status` | (création) `calcule` ; remplacé à chaque recalcul tant que la période n'est pas `approuvee` | SYS |

## 6. Étapes ordonnées

### W09.4.1 — Permissions

- Permissions `payroll_compute`, `payroll_control` ; `SensitiveField` : montants des bulletins et de leurs lignes en `remuneration_paie`.

### W09.4.2 — Données

- Migrations `payslips`, `payslip_lines` (colonnes `enc`) ; `payroll_parameter_version_id` renseigné sur la période au premier calcul.

### W09.4.3 — Moteur

- `App\Services\Payroll\PayrollEngine::computeEmployee(period, employee)` :
  1. contexte : contrat actif (salaire de base), rubriques fixes et ponctuelles, variables de la période, données vérifiées (ancienneté, enfants à charge), type d'employé ;
  2. rubriques de la version dans l'**ordre topologique** ;
  3. chaque rubrique selon son mode (fixe, pourcentage avec plancher et plafond, barème progressif ou par paliers, base annualisée, formule) ; arithmétique **décimale**, arrondi de la rubrique ;
  4. agrégats : brut, imposable, cotisable, cotisations salariales et patronales, impôts, net, coût employeur ;
  5. écriture du bulletin et de **toutes ses lignes** (base, taux, quantité, montant, part), chiffrées.
- Aucune règle métier dans le moteur : tout vient du paramétrage.
- `PayrollEngine::compute(period)` : job par lots d'employés (`Bus::batch`), progression visible, reprise d'un lot en échec, identifiants scalaires seulement (T-03).

**Critère de fin** : un bulletin recalculé plus tard avec un paramétrage modifié **ne change pas** s'il n'est pas recalculé ; recalculé, il utilise toujours la version de sa période.

### W09.4.4 — Bulletins dorés

- `tests/Payroll/Golden/` : cas de référence (TRD §14.4) : salaire sous et au-dessus du plafond CNPS, chaque tranche d'IRPP, heures sup de chaque nature, absences non payées, congé non payé, avance en remboursement (ajouté en W09.7), entrée et sortie en cours de mois, temps partiel, rubrique en formule.
- Chaque cas : entrées, lignes attendues, net attendu ; échec du test au moindre franc d'écart.

**Critère de fin** : tous les bulletins dorés passent ; le document de calcul à la main est rangé dans `05-recette/`.

### W09.4.5 — Contrôle

- `App\Services\Payroll\PayrollControlService` : écarts par employé avec la période précédente (variation du net, rubriques nouvelles ou disparues), anomalies (net négatif, salaire de base nul, employé sans bulletin, seuil d'écart) ; `markControlled(period)` (aucune anomalie bloquante, checklist « calcul » et « contrôle » faites).
- Recalcul de la période ou d'un employé ; montant ponctuel (§4) puis recalcul de l'employé.

### W09.4.6 — Écrans

- S-53 : action « Calculer » avec barre de progression, résumé (effectif, masse brute et nette selon `FieldAccess`).
- S-54 `/payroll-periods/{id}/payslips` : liste des bulletins (net, variation, anomalies), tri par écart (en PHP, colonnes chiffrées, BACKEND SCHEMA §9 point 2), détail d'un bulletin (lignes), aperçu HTML du bulletin, recalcul, montants ponctuels, « Marquer contrôlée ».

### W09.4.7 — Performance

- Mesure sur MySQL avec 200 employés et le paramétrage de démonstration complet : **moins d'une minute** (NF-11) ; profil des requêtes (pas de N+1, déchiffrement groupé) ; résultat consigné dans `05-recette/` et réutilisé pour le dimensionnement du serveur (MEP).

### W09.4.8 — API et documentation

- `/api/v1/payroll/payroll-periods/{id}` (calcul, progression, bulletins, contrôle).
- `02-reference/` : moteur, ordre de calcul, contrôle, bulletins dorés (mode d'emploi pour ajouter un cas).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.4 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Moteur | Bulletins dorés ; chaque mode de calcul ; arrondis ; ordre topologique ; aucune valeur flottante |
| Reproductibilité | Bulletin inchangé après modification du paramétrage ; version de la période |
| Job | Lots, reprise après échec d'un lot, reconnexion à l'entreprise |
| Contrôle | Écarts, anomalies bloquantes et non bloquantes, retour à `calculee` |
| Montants ponctuels | Chiffrés, bornés à la période, recalcul de l'employé |
| Non-fuite | ADM, MGR : aucun montant (écran, API, journal) ; aucun montant dans une notification, quel que soit le destinataire |
| Performance | 200 employés < 1 min (MySQL) |
| Droits | `payroll_compute`, `payroll_control` ; autre entreprise |

## 8. Critères de sortie

- Tests ciblés W09.4 verts, **dont tous les bulletins dorés** ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Mesure de performance consignée.
- Recette APPFLOW §5.10 jusqu'à `Contrôlée`.
- Documentation et livraison de W09.4.8 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Approbation par la direction | W09.5 |
| PDF du bulletin, publication, clôture | W09.6 |
| Échéances d'avance dans le calcul | W09.7 |
