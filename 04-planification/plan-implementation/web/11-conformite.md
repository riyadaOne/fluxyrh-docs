# W11 — Module Conformité

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W10 · Module payant `conformite`

## 1. Objet

Préparer, à partir de la paie clôturée, ce que l'entreprise doit transmettre aux organismes et à sa comptabilité : **déclaration CNPS**, **déclaration fiscale** (IRPP et taxes), **bilan social** annuel, et **export comptable** des écritures de paie (format générique et format Sage) avec un plan comptable et une correspondance rubrique → compte paramétrables. FluxyRH **prépare** ; le dépôt reste manuel (PRD §10). À la fin de W11, le PAIE produit ses déclarations et ses écritures sans ressaisie.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-CNF-01 | Déclaration CNPS par période, depuis la paie clôturée |
| F-CNF-02 | Déclaration fiscale (IRPP, taxes) |
| F-CNF-03 | Bilan social annuel |
| F-CNF-04 | Export comptable Sage et générique ; plan comptable (SYSCOHADA ou autre) ; correspondance rubrique → compte |

À lire : PRD §7.13, §8.2, §10 ; TRD §8 (module), §16.2 ; APPFLOW §5.16, §6.7 (S-78, S-79) ; BACKEND SCHEMA §5.9 (`payroll_rubrics` : comptes), §5.13, §7.

## 3. Prérequis et décisions

W10 livré.

| Sujet | Proposition |
|---|---|
| Produit Sage | **Retenu : Sage 100 Comptabilité** (format d'import d'écritures) ; l'export est un **adaptateur** : un autre produit Sage ou un autre logiciel s'ajoutera sans toucher à la génération des écritures ; TRD §27 mis à jour |
| Contenu des déclarations | **Aucun formulaire de pays codé** (décision 0002) : le PAIE décrit ses **modèles de déclaration** (organisme social, administration fiscale…) : colonnes reliées à une rubrique, un agrégat de paie ou une donnée du dossier, et colonnes à saisir. Tables `declaration_templates` et `declaration_template_columns` ajoutées au BACKEND SCHEMA ; le jeu de démonstration contient un modèle CNPS et un modèle fiscal tchadiens pour les tests |
| Comptes des rubriques | Colonnes `debit_account`, `credit_account` ajoutées à `payroll_rubrics` (reporté de W09.1). Les comptes n'influencent pas le calcul : ils restent **modifiables sur une version active** (exception à l'immuabilité, journalisée), pour ne pas créer une version de paie à chaque correction comptable |
| Plan comptable | **Aucun plan livré** (décision 0002) : le PAIE saisit ou importe (CSV) les comptes de paie de son référentiel (SYSCOHADA ou autre) ; le jeu de démonstration contient des comptes SYSCOHADA pour les tests |
| Bilan social | Chaque entreprise **compose son bilan social** en choisissant ses indicateurs dans un **catalogue** (effectifs de fin d'année et moyen, par sexe, type, structure, tranche d'âge ; entrées et sorties par type ; ancienneté ; absentéisme ; heures sup ; masse salariale ; salaires moyens…), comme ses modèles de déclaration ; tables `social_report_templates` et `social_report_template_indicators` ajoutées au BACKEND SCHEMA |
| Accès | PAIE et DIR (catégorie `remuneration_paie`) ; module non souscrit → 404 « module non souscrit », données conservées si le module est retiré |

## 4. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Déclaration `declarations.status` | `brouillon` → `preparee` (fichier exporté) → `deposee` (référence de dépôt) ; `preparee` → `brouillon` tant qu'elle n'est pas déposée | PAIE |

## 5. Étapes ordonnées

### W11.1 — Enums, permissions, module

- `DeclarationType`, `DeclarationStatus`, `DeclarationLineSource`, `DeclarationColumnSource`, `AccountingExportFormat`, `AccountingGrouping` ; permissions `declarations`, `accounting` liées au module `conformite` (`requiredModule()`).

### W11.2 — Plan comptable et correspondances

- Migrations `chart_of_accounts` ; ajout des comptes à `payroll_rubrics`.
- Import CSV du plan comptable ; liste de démarrage du PAIE à l'activation du module : plan comptable et correspondances.
- S-79 `/accounting`, onglets Plan comptable et Correspondances (rubrique → compte de débit et de crédit, journal de paie) ; contrôle « toute rubrique au bulletin a ses comptes ».

### W11.3 — Écritures et export comptable

- `App\Services\Compliance\AccountingEntryService` : écritures d'une période **clôturée** (débit / crédit par rubrique, nets à payer, regroupement par compte ou par employé), équilibre vérifié.
- Adaptateurs `GenericCsvExporter`, `GenericXlsxExporter`, `SageExporter` (§3) derrière une interface commune.
- Migration `accounting_exports` ; export journalisé avec empreinte, rejouable à l'identique.
- S-79, onglet Exports : période, format, regroupement, historique, téléchargement.

**Critère de fin** : les écritures d'une période du jeu de démonstration sont équilibrées et le fichier Sage s'importe dans une base Sage de test (recette avec l'expert-comptable).

### W11.4 — Déclarations

- Migrations `declaration_templates`, `declaration_template_columns`, `declarations`, `declaration_payroll_periods`, `declaration_lines` (montants chiffrés).
- S-78, onglet Modèles : modèles de déclaration et leurs colonnes (source : rubrique, agrégat, donnée du dossier, saisie).
- `App\Services\Compliance\DeclarationService` : créer sur une ou plusieurs périodes clôturées, lignes **calculées** depuis les bulletins selon le modèle choisi (par employé ou totalisées), informations complémentaires **saisies** (« on ne saisit que ce qui manque »), préparer (fichier XLSX et PDF par `DocumentRenderer`), revenir en brouillon, déposer (référence, date).
- Bilan social : catalogue d'indicateurs (`SocialIndicator`), modèles composés par l'entreprise (S-78, onglet Bilan social), déclaration annuelle de type `bilan_social` calculée selon le modèle.
- S-78 `/declarations` : liste par type et statut, création, lignes (calcul et saisie distingués), export, dépôt.

### W11.5 — API et documentation

- `/api/v1/payroll/declarations`, `/payroll/accounting` (lecture, exports).
- `02-reference/` : déclarations, bilan social, écritures, adaptateurs d'export (mode d'emploi pour ajouter un format).
- Article d'aide du module (W10.5).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W11 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Module | Écrans et API fermés sans le module ; données conservées au retrait |
| Comptes | Correspondances manquantes signalées ; modification sur version active journalisée |
| Écritures | Équilibre, regroupements, période non clôturée refusée, export rejouable identique |
| Formats | CSV, XLSX, Sage conformes à leurs spécifications |
| Déclarations | Lignes calculées exactes (rapprochement avec les états W09.8), saisie, transitions, dépôt |
| Bilan social | Chaque indicateur du catalogue exact sur le jeu de démonstration ; modèle composé |
| Non-fuite | RH, ADM, MGR : aucun accès aux montants |
| Droits | `declarations`, `accounting` ; autre entreprise ; API |

## 7. Critères de sortie

- Tests ciblés W11 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.16 ; import Sage vérifié ; formulaires relus par l'expert-comptable.
- Documentation et livraison de W11.5 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Transmission électronique aux organismes | Hors périmètre (PRD §10) |
| Rapports de pilotage | W13 |
