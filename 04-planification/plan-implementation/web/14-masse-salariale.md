# W14 — Module Masse salariale

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W13 · Module payant `masse_salariale`

## 1. Objet

Donner à la direction et au gestionnaire de paie la maîtrise de la masse salariale : **analyses** par structure, site, type d'employé et période ; **simulations** (hausse globale ou ciblée, rubrique ajoutée, retirée ou modifiée, variation d'effectif) calculées par le moteur de paie **sans rien écrire** dans la paie réelle, enregistrées et **comparées** côte à côte ; **modèles de rémunération** (assemblages de rubriques) appliqués à des populations. À la fin de W14, une décision salariale se chiffre avant d'être prise.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-MSA-01 | Analyses par structure, site, type, période |
| F-MSA-02 | Simulations : hausses, rubriques, variation d'effectif |
| F-MSA-03 | Simulations enregistrées et comparées |
| F-MSA-04 | Modèles de rémunération affectés à des populations |

À lire : PRD §7.10 ; TRD §9.2 (agrégats), §9.4, §14 ; APPFLOW §5.17, §6.6 (S-82, S-83) ; BACKEND SCHEMA §5.9, §5.10, §7 (`SimulationHypothesisKind`).

## 3. Prérequis et décisions

W13 livré ; le moteur de W09.4 calcule un employé sans écrire (fonction de calcul séparée de l'enregistrement, à vérifier au démarrage).

| Sujet | Proposition |
|---|---|
| Base d'une simulation | Une période **clôturée** de référence : ses contrats, rubriques fixes et variables ; le paramétrage utilisé est, au choix, celui de la période ou la version active actuelle |
| Hypothèses | Hausse globale ou ciblée (structure, site, type) en % ou en montant sur le salaire de base ; rubrique ajoutée, retirée ou modifiée (dans une copie en mémoire du paramétrage) ; variation d'effectif par catégorie avec un salaire de référence (employés fictifs) ; hypothèses cumulées dans l'ordre |
| Résultats | Par périmètre (total, structure, site, type) : effectif, brut, coût employeur, écart avec la référence ; chiffrés en base |
| Accès | DIR et PAIE (`remuneration_paie`) ; consultation d'une simulation nominative journalisée (TRD §9.4) |
| Application d'un modèle | Action explicite du PAIE : aperçu des employés de la population et des changements, date d'effet, puis création ou clôture des rubriques fixes (W09.2) ; un nouvel employé de la population est **signalé** au PAIE (notification et mention dans S-51) avec la proposition d'appliquer le modèle ; rien n'est appliqué automatiquement |
| Analyses | Calculées depuis les bulletins **publiés** ; agrégats en PHP (colonnes chiffrées) |

## 4. Étapes ordonnées

### W14.1 — Enums, permissions, module

- `SimulationHypothesisKind` ; permissions `simulations`, `compensation_models` liées au module `masse_salariale`.

### W14.2 — Analyses

- `App\Services\Payroll\PayrollAnalysisService` : masse brute, cotisations, coût employeur, effectif payé, salaire moyen et médian, par structure, site, type et période ; évolution sur 12 périodes.
- S-82 `/simulations`, onglet Analyses : tableaux et graphiques (ApexCharts), exports.

### W14.3 — Simulations

- Migrations `payroll_simulations`, `payroll_simulation_hypotheses`, `payroll_simulation_results`.
- `App\Services\Payroll\PayrollSimulationService` : contexte de la période de référence, application des hypothèses, calcul par le moteur **en mémoire** (aucune écriture dans `payslips`), résultats par périmètre ; job si l'effectif le demande ; recalcul.
- S-82 : création (nom), hypothèses, calcul, résultats, enregistrement ; liste des simulations par nom et date de création, réouverture ; **comparaison** de plusieurs simulations côte à côte. Une simulation reste à l'état de simulation : rien n'est écrit dans la vraie paie.

**Critère de fin** : une simulation sans hypothèse redonne exactement les totaux de la période de référence ; aucune table de paie réelle n'est modifiée.

### W14.4 — Modèles de rémunération

- Migrations `compensation_models`, `compensation_model_items`, `compensation_model_assignments`.
- `App\Services\Payroll\CompensationModelService` : modèle (rubriques individualisables, montants ou taux chiffrés), populations (poste, type), aperçu et application (§3), proposition aux nouveaux employés.
- S-83 `/compensation-models` ; mention « modèle applicable » dans S-51 (W09.2).

### W14.5 — Documentation et livraison

- `02-reference/` : analyses, simulations, modèles ; article d'aide.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W14 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Analyses | Totaux égaux aux états de paie (W09.8), regroupements, évolution |
| Simulations | Simulation neutre = référence ; chaque type d'hypothèse ; hypothèses cumulées ; employés fictifs ; aucune écriture réelle ; version de référence ou actuelle |
| Comparaison | Écarts entre simulations |
| Modèles | Population, aperçu, application datée, proposition à un nouvel employé |
| Non-fuite | RH, ADM, MGR : aucun accès, même délégué ; journal des consultations |
| Module | Fermé sans le module |
| Droits | `simulations`, `compensation_models` ; autre entreprise |

## 6. Critères de sortie

- Tests ciblés W14 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.17.
- Documentation et livraison de W14.5 faites.

## 7. Reporté

| Élément | Module |
|---|---|
| Simulations dans l'app | Non prévu (écrans web) |
