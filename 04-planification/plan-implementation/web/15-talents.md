# W15 — Module Talents

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W14 · Module payant `talents`

## 1. Objet

Suivre et développer les personnes : **évaluations 360°** (campagnes, critères, poids par type d'évaluateur, une réponse par évaluateur, score pondéré, évaluation clôturée immuable), **référentiel de compétences** (compétences par employé et par poste, recherche), **parcours de carrière** (étapes de postes, historique) et **import des candidats retenus depuis Jobyflow**, qui deviennent des invitations pré-remplies. À la fin de W15, le RH conduit une campagne d'évaluation complète et recrute sans ressaisie depuis Jobyflow.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-TAL-01 | Évaluations 360° |
| F-TAL-02 | Compétences, compétences par employé, recherche |
| F-TAL-03 | Parcours de carrière, historique des postes |
| F-TAL-04 | Import Jobyflow, invitations pré-remplies |

À lire : PRD §7.12, §10 (recrutement hors périmètre) ; TRD §16.1, §27 ; APPFLOW §3.1, §5.3 (fin), §5.14, §5.15, §6.7 (S-75 à S-77) ; BACKEND SCHEMA §5.3 (`recruitment_import_id`), §5.12, §7, §8.

## 3. Prérequis et décisions

W14 livré. Le contrat d'interface Jobyflow (TRD §16.1) est **transmis à l'équipe Jobyflow** au démarrage de W15 (TRD §27).

| Sujet | Proposition |
|---|---|
| Désignation des évaluateurs | Le RH **choisit tous les évaluateurs à la main**, individuellement ou par groupe (structure, site, équipe d'un manager), et indique le type de chacun (auto, manager, pair, collaborateur) |
| Anonymat | **Paramétré par campagne** : pour chaque type d'évaluateur, réponses nominatives ou anonymes, et nombre minimum de réponses pour afficher une moyenne anonyme ; colonnes ajoutées à `evaluation_campaign_weights` |
| Réponses manquantes à la clôture | **Réglé à la création de chaque campagne** (décision 0004) : soit la clôture est bloquée tant que tous les évaluateurs n'ont pas répondu, soit elle est permise après la date de fin avec les poids recalculés sur les réponses reçues ; dans les deux cas, le RH relance ou retire un évaluateur défaillant avec un motif (journalisé). Colonne `evaluation_campaigns.closure_requires_all_responses` |
| Visibilité du rapport | Employé évalué, son manager, RH, direction |
| Évaluation des compétences | Par le RH et le manager (`assessed_by`) ; l'employé consulte les siennes ; écart avec le niveau requis par son poste |
| Parcours de carrière | Définis par le RH ; la position d'un employé est déduite de son historique d'affectation (W04.1, W12.1) ; prochaine étape « accessible » si la durée minimale est atteinte, à titre indicatif |
| Configuration Jobyflow | Onglet **Intégrations** de la Configuration (ADM) : URL et clé d'API chiffrée par la DEK, test de connexion |
| Données importées | Pré-remplies dans l'assistant de complétion comme **brouillon** que l'employé confirme : c'est lui qui soumet (P1, P2) ; les pièces sont proposées dans l'étape Pièces et passent `À vérifier` à sa confirmation |
| Fournisseur de test | Faux fournisseur `FakeRecruitmentSource` pour les tests et la recette, tant que Jobyflow n'expose pas son API |

## 4. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Campagne `evaluation_campaigns.status` | `brouillon` → `ouverte` → `cloturee` | RH |
| Évaluation `evaluations.status` | `en_cours` → `cloturee` (immuable) | SYS à la clôture de la campagne |
| Évaluateur | `a_faire` → soumis (une seule fois) | Évaluateur |
| Import `recruitment_imports.status` | `importe` → `invitation_envoyee` / `ignore` | RH |

## 5. Étapes ordonnées

### W15.1 — Enums, permissions, module

- `EvaluationCampaignStatus`, `EvaluationStatus`, `EvaluatorType`, `RecruitmentImportStatus` ; permissions `evaluations`, `skills`, `recruitment_imports` liées au module `talents`.

### W15.2 — Évaluations 360°

- Migrations `evaluation_campaigns`, `evaluation_campaign_weights`, `evaluation_criteria`, `evaluations`, `evaluation_evaluators`, `evaluation_answers`.
- `App\Services\Talent\EvaluationService` : campagne (critères, échelle, poids dont la somme = 100), employés, évaluateurs choisis par le RH (§3), ouverture (notifications), réponse unique par évaluateur, relances, retrait motivé d'un évaluateur, clôture selon le réglage de la campagne (score pondéré, immuabilité), rapport selon l'anonymat paramétré (§3).
- S-75 `/evaluations` (RH) : campagnes, avancement ; `/evaluations/to-fill` (évaluateurs) ; `/me/evaluations` (rapports de la personne) ; onglet de la fiche S-21.

### W15.3 — Compétences et carrières

- Migrations `skills`, `employee_skills`, `job_position_skills`, `career_paths`, `career_path_steps`.
- `App\Services\Talent\SkillService`, `CareerPathService` : référentiel, niveaux par employé et requis par poste, écarts, recherche par compétence et niveau ; parcours et position d'un employé (§3).
- S-76 `/skills` : référentiel, compétences par poste, recherche ; parcours de carrière ; onglets Compétences et Carrière de la fiche S-21 et de « Mon dossier ».

### W15.4 — Import Jobyflow

- Migrations `recruitment_sources`, `recruitment_imports`, `recruitment_import_documents` ; `recruitment_import_id` ajouté à `employee_invitations` (reporté de W04.1).
- Interface `RecruitmentSource`, `JobyflowClient` (HTTP, délai, nouvelles tentatives, contrat TRD §16.1), `FakeRecruitmentSource`.
- `App\Services\Talent\JobyflowImportService` : candidats retenus depuis le dernier import, sélection, complétion de l'affectation, **invitations en brouillon** pré-remplies, accusé d'import à Jobyflow, pièces récupérées sur le disque privé ; à l'acceptation, pré-remplissage de l'assistant (§3).
- S-77 `/recruitment-imports` : importer, sélectionner, compléter, ignorer, suivre ; onglet Intégrations de la Configuration.

**Critère de fin** : avec le faux fournisseur, un candidat importé reçoit son invitation, retrouve ses données dans l'assistant et les soumet lui-même.

### W15.5 — API et documentation

- `/api/v1/employee/evaluations` (à remplir, soumettre, rapports), `/manager/evaluations`, `/hr/skills`, `/hr/recruitment-imports`.
- `02-reference/` : évaluations, compétences, carrières, contrat Jobyflow (version transmise) ; article d'aide.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W15 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Évaluations | Poids = 100, réponse unique, soumission hors campagne ouverte refusée, clôture bloquée ou permise selon le réglage de la campagne, retrait motivé, immuabilité, score pondéré, anonymat paramétré |
| Compétences | Niveaux, écarts avec le poste, recherche |
| Carrières | Position déduite de l'historique, durée minimale |
| Jobyflow | Faux fournisseur : import, déduplication par identifiant externe, accusé, pièces, erreurs réseau et nouvelles tentatives, clé chiffrée |
| Pré-remplissage | Données en brouillon, soumises par l'employé seulement |
| Module | Fermé sans le module |
| Droits | `evaluations`, `skills`, `recruitment_imports` ; périmètre du manager ; autre entreprise ; API |

## 7. Critères de sortie

- Tests ciblés W15 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.14 et §5.15 (faux fournisseur) ; contrat Jobyflow transmis.
- Documentation et livraison de W15.5 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Recette avec la vraie API Jobyflow | Dès que Jobyflow l'expose (extension datée) |
| Évaluations dans l'app | E09 |
