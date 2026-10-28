# W08.1 — Contrats · Bibliothèque de blocs (RH)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W07 · Suite : W08.2 (rédaction)

## 1. Objet

Donner au RH sa bibliothèque juridique : des **blocs** (clauses) créés lors de la configuration, rédigés dans la **langue officielle** de l'entreprise, versionnés, avec leurs **règles de proposition** (pour quelle nature de contrat, quel type d'employé, inséré d'office ou seulement proposé). À la rédaction d'un contrat (W08.2), les blocs pertinents sont **proposés**, et le RH peut toujours en ajouter. W08.1 pose aussi l'éditeur de texte riche assaini et les **champs de fusion**, réutilisés par les courriers (W12.3). À la fin de W08.1, l'entreprise a sa bibliothèque de blocs ; aucune clause n'est livrée par défaut (décision 0002).

## 2. Ce que le RH reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Types d'employé, postes (W03, W04) ; dossier vérifié (W04.3) comme source des champs | Blocs publiés et leurs règles de proposition | **Rédaction** (W08.2) : blocs proposés ; **courriers** (W12.3) : éditeur et champs de fusion |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-CTR-01 | Contrats rédigés dans l'application, éditeur avec champs de fusion |
| T-09 (fusion) | Un champ sensible n'est inséré que par un auteur qui y a droit, jamais résolu pour un lecteur non autorisé |

À lire : PRD §7.8 ; TRD §9.2, §15, §22 (contenu riche) ; APPFLOW §5.2 (I), §5.9, §6.4 (S-41) ; BACKEND SCHEMA §5.8, §7 (`ClauseCategory`, `ContractKind`) ; UX/UI §6.7, §13.4.

## 4. Prérequis et décisions

W07 livré. Paquets installés par le développeur : `symfony/html-sanitizer` ; Tiptap (npm).

| Sujet | Proposition |
|---|---|
| Blocs à la place des modèles | La rédaction se fait **par blocs proposés** : les tables `contract_templates` et `contract_template_items` sont remplacées par **`contract_clause_rules`** (`contract_clause_id`, `contract_kind` ?, `employee_type_id` ?, `is_preselected` bool) : un bloc est proposé pour une nature de contrat et / ou un type d'employé, inséré d'office s'il est présélectionné. BACKEND SCHEMA §5.8 mis à jour |
| Langue | Les documents sont rédigés dans la **langue officielle** de l'entreprise : un bloc a un seul texte, dans cette langue ; la table `contract_clause_texts` (texte par langue) est remplacée par `title` et `body` sur la version. Si l'entreprise change de langue officielle, les blocs existants restent tels quels et le RH les réécrit |
| Bibliothèque par défaut | **Aucune** (décision 0002) : le RH crée ses blocs ; le jeu de démonstration en contient pour les tests |
| Ajout pendant la rédaction | Le RH peut, depuis l'éditeur d'un contrat, écrire un bloc libre et l'**enregistrer dans la bibliothèque** pour les contrats suivants (W08.2) |
| Versions d'un bloc | Une version en brouillon est modifiable ; une version **publiée** est figée ; modifier un bloc publié crée une nouvelle version. Un contrat copie le texte (TRD §15) : publier une nouvelle version ne change aucun contrat existant |
| Éditeur de texte riche | Pas de licence Flux Pro : **Tiptap** (gratuit, npm) intégré dans un composant Livewire maison `rich-editor`, réutilisé par les contrats, les courriers et les annonces. Fonctions limitées au TRD §15 : gras, italique, listes, titres, tableaux simples, pastilles de champs |
| Champs de fusion | Liste fermée déclarée dans `MergeFieldRegistry` : `entreprise.*`, `employe.*` (valeurs vérifiées), `affectation.*` (poste, structure, site, manager), `contrat.*` (nature, dates, période d'essai, horaires, salaire de base — résolus en W08.2) ; chaque champ porte son libellé et, s'il y a lieu, sa catégorie `SensitiveField` |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Version de bloc | brouillon → publiée (`published_at`) ; publiée immuable | RH |
| Bloc | actif ; corbeille | RH |

## 6. Étapes ordonnées

### W08.1.1 — Enums, permissions, spécification

- `ClauseCategory`, `ContractKind` ; permission `contract_library`.
- BACKEND SCHEMA §5.8 mis à jour (`contract_clause_rules`, texte sur la version, retrait des modèles et des textes par langue) ; APPFLOW §5.9 (rédaction par blocs proposés) et §6.4 (S-41 « Bibliothèque de blocs ») mis à jour.

### W08.1.2 — Contenu riche

- `App\Support\RichText` : assainissement par liste blanche (balises du TRD §15, attributs limités, pastilles de champs) appliqué à **l'enregistrement** et au rendu ; test des injections (script, style, liens `javascript:`, images distantes).
- Composant d'édition (§4) avec insertion des pastilles depuis un menu.

### W08.1.3 — Champs de fusion

- `App\Services\Documents\MergeFieldRegistry` : liste fermée (§4), libellés, catégories sensibles.
- `MergeFieldResolver::resolve(text, context, reader)` : remplace les champs par leurs valeurs **vérifiées**, applique `FieldAccess` au lecteur (valeur masquée « •••• » s'il n'y a pas droit) ; champ inconnu refusé à l'enregistrement d'un texte ; champ sensible refusé à l'enregistrement si l'auteur n'y a pas droit.
- Les résolveurs `contrat.*` sont branchés en W08.2.

**Critère de fin** : un texte avec un champ inconnu est refusé ; un champ sensible est masqué pour un lecteur non autorisé ; seules les valeurs vérifiées sont utilisées.

### W08.1.4 — Blocs et règles de proposition

- Migrations `contract_clauses`, `contract_clause_versions` (avec `title`, `body`), `contract_clause_rules`.
- `App\Services\Tenant\ClauseLibraryService` : créer un bloc, éditer le brouillon, publier, nouvelle version, règles de proposition, `proposedFor(contractKind, employeeType)` (blocs présélectionnés et blocs proposés, dans l'ordre de leur catégorie), corbeille.
- S-41 `/contract-clauses` : bibliothèque par catégorie, recherche, versions et différences entre deux versions, règles de proposition, aperçu PDF d'un bloc avec un employé fictif (`DocumentRenderer`, UX/UI §13.4).

**Critère de fin** : pour une nature de contrat et un type d'employé, la liste des blocs proposés et présélectionnés est exacte ; une version publiée ne se modifie plus.

### W08.1.5 — Mise en place

- Liste de démarrage du RH : créer les blocs de la bibliothèque et leurs règles.
- Seeder **de démonstration** (refusé en production) : quelques blocs pour un CDI, un CDD et un stage.

### W08.1.6 — Documentation et livraison

- `02-reference/` : contenu riche, champs de fusion (liste complète), blocs, versions, règles de proposition.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W08.1 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Assainissement | Balises et attributs interdits retirés ; pastilles conservées ; injections |
| Fusion | Champ inconnu, champ sensible sans droit à l'enregistrement, masquage à la lecture, valeur vérifiée seulement |
| Versions | Publication, immuabilité d'une version publiée, nouvelle version, différence |
| Proposition | Par nature, par type d'employé, présélection, bloc sans règle (ajout manuel seulement) |
| Provisionnement | Aucun bloc dans une entreprise neuve |
| Droits | `contract_library` ; délégation, exclusion ; autre entreprise |

## 8. Critères de sortie

- Tests ciblés W08.1 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.2 (branche I) : le RH constitue sa bibliothèque de blocs et ses règles.
- Documentation et livraison de W08.1.6 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Rédaction d'un contrat, ajout de blocs, signataires, résolution des champs `contrat.*` | W08.2 |
| Courriers types | W12.3 |
| Charte graphique des documents | W16 |
