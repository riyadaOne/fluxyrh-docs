# W09.1 — Paie · Paramétrage (PAIE)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W08 · Suite : W09.2 (éléments par employé)

## 1. Objet

Donner au gestionnaire de paie un paramétrage **entièrement configurable et versionné** : rubriques (gains, cotisations, impôts, retenues, informations), modes de calcul (fixe, pourcentage, barème, formule), plafonds, arrondis, traductions, **versions datées** qui ne modifient jamais les bulletins passés, fréquences de paie utilisées. **Aucun paramétrage de pays n'est livré** (décision 0002) et aucun taux, montant ni devise n'est écrit dans le code (T-08). À la fin de W09.1, le gestionnaire de paie de chaque entreprise a construit et activé son paramétrage.

## 2. Ce que le gestionnaire de paie reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Devise de l'entreprise ; législation de son pays (hors système) | Versions du paramétrage (`brouillon` → `active`), fréquences utilisées, réglage d'ouverture automatique | **Éléments par employé** (W09.2) : codes de rubriques ; **moteur** (W09.4) : rubriques ordonnées ; **périodes** (W09.3) : fréquences |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-01 | Rubriques paramétrables, modes de calcul, plafonds, imposable, cotisable |
| F-PAY-02 | Aucun paramétrage de pays livré (décision 0002) ; jeu de démonstration pour les tests |
| F-PAY-03 | Versions avec date d'effet ; bulletins passés inchangés |
| F-PAY-05 (fréquences) | Fréquences de paie utilisées par l'entreprise |
| T-08, T-12 | Aucun taux en dur ; formules en évaluateur restreint ; calcul décimal |

À lire : PRD §7.9, annexe 14.3 ; TRD §14.1, §14.2, §20 (devise), §22 (formules) ; APPFLOW §5.2 (H), §5.10 (fin), §6.5 (S-50) ; BACKEND SCHEMA §5.1 (`payroll_frequency_settings`), §5.9, §7, §8 ; UX/UI §5.3.

## 4. Prérequis et décisions

W08 livré. Paquets installés par le développeur : `symfony/expression-language` ; `brick/math` si W00.10 ne l'a pas retenu.

| Sujet | Proposition |
|---|---|
| Version applicable | Plusieurs versions peuvent être `active` : la version applicable à une date est la dernière `active` dont `effective_from` est antérieure ou égale. `archivee` = version remplacée avant d'avoir été utilisée, ou retirée par le PAIE |
| Modifier le paramétrage | Une version `active` n'est jamais modifiée : on **duplique** la version en vigueur en brouillon, on la modifie, on l'active avec sa date d'effet |
| Rétroactivité | La date d'effet d'une nouvelle version est postérieure à la fin de la dernière période **clôturée** de chaque fréquence |
| Paramétrage initial | Aucun (décision 0002) : le PAIE crée sa première version, ses rubriques et barèmes, puis l'active ; la liste de démarrage le guide, et l'écran propose un ordre de saisie (gains, cotisations, impôts, retenues) |
| Jeu de démonstration | Seeder de démonstration et de test reprenant l'exemple tchadien de l'annexe 14.3 du PRD, **jamais chargé en production** ; utilisé par le jeu de démonstration et les bulletins dorés (W09.4) |
| Comptes comptables | Les colonnes `debit_account`, `credit_account` sont ajoutées avec le module Conformité (W11) |
| Variables des formules | Le catalogue complet (TRD §14.2) est déclaré ici avec ses libellés et son aide ; leurs valeurs sont fournies par le moteur (W09.4) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Version `payroll_parameter_versions.status` | `brouillon` → `active` ; `brouillon` ou `active` non utilisée → `archivee` | PAIE |

Une version utilisée par une période n'est plus modifiable ni archivable (BACKEND SCHEMA §8).

## 6. Étapes ordonnées

### W09.1.1 — Enums et permissions

- `ParameterVersionStatus`, `RubricNature`, `RubricPayer`, `RubricCalcMode`, `BracketBasis`, `RoundingRule` ; `PayFrequency` (W04.1) réutilisé ; permission `payroll_parameters`.

### W09.1.2 — Données

- Migrations `payroll_parameter_versions`, `payroll_rubrics` (sans comptes, §4), `payroll_rubric_translations`, `payroll_rubric_brackets`, `payroll_frequency_settings`.
- Models, factories (une version de test complète pour les tests de paie).

### W09.1.3 — Formules

- `App\Services\Payroll\FormulaEvaluator` : Symfony ExpressionLanguage en environnement restreint, fonctions `min`, `max`, `arrondi`, `si`, `annuel`, `mensuel`, variables en lecture seule, calcul décimal ; aucun accès aux fonctions PHP ni aux objets.
- `App\Services\Payroll\PayrollVariableCatalog` : variables (`SALAIRE_BASE`, `BRUT`, `BRUT_COTISABLE`, `IMPOSABLE`, `JOURS_OUVRES`, `JOURS_TRAVAILLES`, `HEURES_SUP_<taux>`, `ANCIENNETE_ANNEES`, `ENFANTS_A_CHARGE`, `TYPE_EMPLOYE`, `R_<CODE>`), libellés trilingues, aide.
- Tests d'évasion : appel de fonction PHP, accès à une propriété, constante, boucle, division par zéro.

### W09.1.4 — Paramétrage et versions

- `App\Services\Payroll\PayrollParameterService` : dupliquer la version en vigueur, éditer un brouillon (rubriques, tranches, traductions, ordre), valider (syntaxe, variables connues, **absence de dépendance circulaire** par tri topologique, cohérence des tranches, plafonds), activer (date d'effet, §4), archiver, `versionFor(date)` ; immuabilité d'une version utilisée.
- `CurrencyService` : devise verrouillée dès la première rubrique (BACKEND SCHEMA §8) ; l'onglet devise de la Configuration (W02.9) devient non modifiable.

**Critère de fin** : un cycle entre deux rubriques est refusé avec le chemin du cycle ; une version active ne peut pas être modifiée.

### W09.1.5 — Jeu de démonstration

- Seeder **de démonstration** (refusé en production) : une version complète inspirée de l'annexe 14.3 du PRD (cotisations avec plafond, assiette minimale, impôt par barème annuel, taxes patronales, salaire de base, heures sup, absences non payées, retenue d'avance), utilisée par le jeu de démonstration et les tests.
- Aucune fréquence imposée : le PAIE coche celles qu'il utilise.

### W09.1.6 — Écran S-50

- S-50 `/payroll-parameters` (navlist UX/UI §5.3) : versions (statut, date d'effet, utilisée ou non), rubriques par nature et ordre de calcul, éditeur de rubrique selon le mode (montant, taux × base, barème, formule avec aide des variables), traductions, **prévisualisation** d'une rubrique ou de la version sur des valeurs saisies, différences entre deux versions, valeurs « à confirmer » signalées ; onglet **Fréquences** (utilisées, ouverture automatique de la période suivante).
- Liste de démarrage du PAIE : choisir les fréquences utilisées, créer et activer la première version du paramétrage.

**Critère de fin** : APPFLOW §5.2 (branche H) recetté : le PAIE construit sa première version, l'active, puis modifie un taux dans une nouvelle version.

### W09.1.7 — API et documentation

- `/api/v1/payroll/parameters` (lecture des versions et rubriques).
- `02-reference/` : rubriques, formules, catalogue des variables, versions, jeu de démonstration.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.1 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Formules | Syntaxe, variables inconnues, évasion de l'évaluateur, décimal, arrondis |
| Dépendances | Cycle direct et indirect, ordre topologique |
| Versions | Duplication, activation, version applicable à une date, immuabilité, rétroactivité refusée, archivage |
| Barèmes | Tranches progressives et par paliers, base annualisée, trous et chevauchements refusés |
| Devise | Verrouillage à la première rubrique |
| Provisionnement | Aucune rubrique dans une entreprise neuve ; jeu de démonstration complet en développement, refusé en production |
| Droits | `payroll_parameters` ; délégation ; autre entreprise ; l'ADM n'y a pas accès par défaut |

## 8. Critères de sortie

- Tests ciblés W09.1 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.2 (branche H).
- Documentation et livraison de W09.1.7 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Rubriques fixes par employé | W09.2 |
| Périodes, checklist | W09.3 |
| Moteur et bulletins dorés | W09.4 |
| Comptes comptables des rubriques | W11 |
