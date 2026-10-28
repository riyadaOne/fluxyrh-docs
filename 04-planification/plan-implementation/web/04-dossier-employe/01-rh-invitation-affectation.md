# W04.1 — Dossier employé · RH : invitation et affectation

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W03 · Suite : W04.2 (employé), W04.3 (vérification)

## 1. Objet

Faire entrer les personnes dans l'entreprise. Le RH paramètre les types d'employé et de documents, invite chaque personne avec son affectation (poste, structure, site, manager, type, date d'embauche) ; à l'acceptation, le système crée le **dossier** avec un matricule automatique et ouvre la période d'emploi. W04.1 construit aussi la hiérarchie et le périmètre d'équipe, la fiche employé (en-tête et affectations), l'organigramme des personnes et la sortie simple. À la fin, le RH a invité toute l'entreprise ; chaque personne a un dossier `Actif` vide, prêt à être complété (W04.2).

## 2. Ce que le RH reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Structure, postes, sites (W03) ; rattachements (W02) | Types d'employé et de documents, pièces obligatoires ; invitations avec affectation ; dossiers `Actif` ; hiérarchie | **Employé** (W04.2) : un dossier à compléter ; **manager** : son équipe ; **plateforme** : effectifs |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-EMP-01 | Invitation avec affectation, dossier créé à l'acceptation, matricule automatique |
| F-EMP-02 | Types d'employé système et propres à l'entreprise, entrée dans la paie |
| F-EMP-05 (paramétrage) | Types de documents (dépôt, expiration, visibilité) ; le dépôt est en W04.2, l'alerte d'expiration en W04.3 |
| F-EMP-07 | Cycle `Actif` → `En sortie` → `Sorti`, réembauche ; dossier sorti en lecture seule |
| F-EMP-09 (paramétrage) | Pièces obligatoires par type d'employé ; le calcul de complétude est en W04.3 |
| F-ORG-04 | Manager de chaque employé, équipe directe et indirecte |
| F-ORG-01, 05 (fin) | Responsable d'une unité, organigramme des personnes |
| F-ADM-07 (matricule) | Onglet Matricule de la Configuration |
| F-PLT-04 (effectifs) | Effectifs par entreprise, dépassement de palier |

À lire : PRD §6 (P1, P2), §7.4 ; TRD §7.1, §8, §11 ; APPFLOW §3.1, §4.4, §4.6, §5.2, §6.1 (S-03, S-15), §6.2 (S-20, S-21, S-23, S-24), §8 ; BACKEND SCHEMA §5.1 (`employee_number_settings`), §5.3, §5.4 (`document_types`, `document_type_requirements`), §6, §8 ; UX/UI §6.1, §6.3.

## 4. Prérequis et décisions

W03 livré.

| Sujet | Proposition |
|---|---|
| Qui invite avec dossier | L'ADM n'invite qu'**un premier RH** (S-03, option « avec dossier », rôle `rh` seulement) ; ensuite **le RH invite tout le monde** par S-20, direction et PAIE compris (APPFLOW §5.2 mis à jour). Même table `employee_invitations`, même service |
| Admin entreprise avec dossier | Une invitation employé peut viser un compte admin existant (APPFLOW §8) : le rattachement garde le rôle `admin_entreprise` et reçoit un dossier |
| Équipe d'un manager | L'équipe est définie par la **hiérarchie** (`manager_employee_id`), quel que soit le rôle : une direction ou un RH qui a des subordonnés voit « Mon équipe ». Le rôle `manager` ne donne que les écrans par défaut |
| Décision en l'absence du manager direct | Le supérieur n'agit qu'en l'absence du manager direct (F-ORG-04) : l'absence n'existe qu'avec les congés, donc cette règle est construite en W07 ; en W04.1, seul le manager direct décide |
| Changement de rôle (reporté de W02) | L'ADM change le rôle d'un rattachement entre rôles avec dossier (`employe`, `manager`, `rh`, `gestionnaire_paie`, `direction`) ; motif obligatoire, journalisé, effet immédiat. Le passage depuis ou vers « admin sans dossier » passe par une invitation |
| Sortie sans module Processus RH | Le RH déclare la sortie (date, type ∈ `TerminationType`, motif) : `En sortie` jusqu'à la date, puis `Sorti` par le système. L'accès se coupe à la date de sortie, sans prolongation : un ancien employé qui a besoin d'un document (bulletin, certificat) le demande hors application, et le RH le télécharge pour lui. Le workflow de sortie complet est en W12.2 |
| Écritures sur deux bases à l'acceptation | `accept()` écrit dans la base générale (identité, rattachement) et dans celle de l'entreprise (dossier) : pas de transaction commune possible. Ordre fixé et étapes **idempotentes** (dossier créé d'abord, rattachement activé ensuite, invitation `acceptee` en dernier) ; une acceptation interrompue se rejoue sans doublon |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Invitation `employee_invitations.status` | `brouillon` → `envoyee` → `acceptee` / `expiree` / `annulee` | RH (ou ADM) ; la personne ; SYS (7 jours) |
| Rattachement | `invite` → `actif` | à l'envoi, puis à l'acceptation |
| Employé `employees.status` | (création) `actif` → `en_sortie` → `sorti` ; `sorti` → `actif` (réembauche) | SYS à l'acceptation ; RH déclare la sortie ; SYS à la date ; RH réembauche par invitation liée au dossier |
| Période d'emploi | ouverte → fermée | à l'embauche ; à la sortie |

## 6. Étapes ordonnées

### W04.1.1 — Enums et permissions

- `EmployeeStatus`, `PayFrequency`, `DocumentUploader`, `TerminationType` (BACKEND SCHEMA §7).
- Permissions `reference_types`, `employee_invitations`, `employees`.
- APPFLOW §6.1 (S-03 avec dossier) et §8 (équipe par la hiérarchie, changement de rôle) mis à jour.

### W04.1.2 — Types d'employé et de documents

- Migrations d'entreprise : `employee_types`, `document_types`, `document_type_requirements`.
- Création au provisionnement des **9 types par défaut** (`is_system`) avec leurs libellés dans la **langue officielle** de l'entreprise (tirés des fichiers de langue) ; modifiables (libellé, entrée dans la paie, fréquence par défaut) et désactivables, mais pas supprimables (leur code reste stable) ; l'entreprise ajoute ses propres types. Étape ajoutée à `CompanyProvisioningService` et rejouée sur les entreprises existantes par une commande de migration de données.
- Services de référentiel ; S-15 `/employee-types` et `/document-types` : création, modification, entrée dans la paie, fréquence par défaut, pièces obligatoires par type d'employé, corbeille.

**Critère de fin** : les 9 types par défaut sont présents dans une entreprise neuve, libellés dans sa langue officielle ; un type par défaut se modifie et se désactive mais ne se supprime pas.

### W04.1.3 — Dossier et matricule

- Migrations d'entreprise : `employee_number_settings`, `employees` (sans les pointeurs `current_*`, ajoutés en W04.2), `employment_periods`, `employee_position_history`, `employee_sites` ; ajout de `head_employee_id` à `org_units`.
- Models, factories (`Employee` avec états par statut et par rôle).
- `App\Services\Tenant\EmployeeService` : `nextEmployeeNumber()` selon le format (`{annee}`, `{sequentiel}`, préfixe) sous verrou, sans trou ni doublon ; création du dossier ; une seule période d'emploi ouverte ; historique d'affectation ; site principal toujours dans les sites de pointage.
- Onglet **Matricule** de la Configuration (format, longueur, aperçu, prochain numéro).

**Critère de fin** : 50 créations concurrentes donnent 50 matricules distincts et consécutifs ; le format est appliqué.

### W04.1.4 — Invitations avec dossier

- Migration d'entreprise : `employee_invitations` (sans `recruitment_import_id`, ajouté en W15).
- `InvitationService` étendu : invitation employé (rôle, type, poste, structure, site principal, manager, date d'embauche, fréquence de paie, fin d'accès), envoi, renvoi, annulation, expiration ; `accept()` crée le dossier `actif` (ou réactive un dossier sorti pour une réembauche : même matricule, nouvelle période d'emploi), ouvre la période d'emploi, écrit l'historique d'affectation, active le rattachement ; idempotent (§4).
- S-20 `/invitations/employees` : création unitaire, liste par statut, renvoi, annulation, corbeille ; S-03 enrichi de l'option « avec dossier », limitée au premier RH.
- Page `/invitation/{jeton}` : branche « dossier » (APPFLOW §3.1) ; à la fin, redirection vers l'espace personnel (l'assistant de complétion arrive en W04.2).

**Critère de fin** : APPFLOW §3.1 complet recetté (compte neuf, compte existant, réembauche, admin qui reçoit un dossier) ; une acceptation interrompue puis rejouée ne crée aucun doublon.

### W04.1.5 — Hiérarchie et périmètre d'équipe

- `App\Services\Tenant\TeamScope` : équipe directe et indirecte d'un employé (descente de `manager_employee_id`), refus des cycles et de l'auto-management, requêtes bornées en profondeur.
- `FieldAccess` : branchement de « l'employé concerné » (la personne voit ses propres champs sensibles).
- Changement de manager, de responsable d'unité : par le RH, journalisé, écrit dans l'historique d'affectation (les mutations formelles passent par les événements du module Processus RH en W12.1).
- Changement de rôle (§4), écran S-02.

**Critère de fin** : équipe de 3 niveaux correcte ; cycle refusé ; un manager ne voit rien hors de son équipe.

### W04.1.6 — Fiche employé, équipe, organigramme

- S-21 `/employees` : liste (recherche, filtres structure, site, type, statut, manager), corbeille ; fiche (UX/UI §6.3) avec l'en-tête (nom, matricule, poste, statut, structure, site, manager, type, date d'embauche) et les onglets **Affectations** (historique, sites de pointage) et **Journal** ; les autres onglets sont ajoutés par W04.2 et les modules suivants.
- S-24 `/team` : liste de l'équipe directe et indirecte (les présences et absences s'y ajoutent en W06.3 et W07).
- S-23 `/org-chart` : responsables d'unités et hiérarchie des personnes ; vue limitée à son équipe pour le manager ; export PDF.
- Le nom affiché vient de l'identité (`users`) tant que l'identité vérifiée n'existe pas (W04.3).

**Critère de fin** : chaque écran testé pour RH, DIR, MGR (périmètre), rôle délégué, personne exclue ; organigramme PDF des personnes en fr et ar.

### W04.1.7 — Sortie simple

- `EmployeeService::declareExit(date, type, reason)` → `en_sortie` ; tâche planifiée → `sorti` à la date, période d'emploi fermée, fin d'accès du rattachement (§4) ; dossier en lecture seule pour tous ; annulation possible tant que la date n'est pas passée.
- Contrôle ajouté à `OrganizationService` : suppression d'une unité refusée s'il y reste des employés actifs.

**Critère de fin** : un employé sorti n'est plus modifiable, n'apparaît plus dans les équipes actives et retrouve son dossier à la réembauche.

### W04.1.8 — API

- `/api/v1/hr/invitations` (liste, création, renvoi, annulation), `/hr/employees` (liste, fiche), `/manager/team`, `/admin/...` enrichi des invitations avec dossier ; `/me` complété du dossier (identifiant, matricule, affectation, manager).
- Contrat Scramble à jour ; refus testés (rôle, permission, périmètre, autre entreprise).

### W04.1.9 — Plateforme et mise en place

- Instantané nocturne : employés actifs par entreprise ; **dépassement de palier** signalé sur le tableau de bord plateforme et à l'admin de l'entreprise (e-mail ; cloche en W04.3).
- Liste de démarrage de l'admin : types d'employé et de documents, pièces obligatoires, invitation du premier RH (ADM) ; puis, côté RH, invitation de la direction, du PAIE, des managers et des employés.

### W04.1.10 — Documentation et livraison

- `02-reference/` : invitations, dossier, matricule, hiérarchie, sortie.
- `05-recette/` : jeu de démonstration (une entreprise de 30 employés sur 3 niveaux de hiérarchie, tous les rôles).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W04.1 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Référentiels | Types par défaut dans la langue officielle (fr, en, ar), modification, désactivation, suppression refusée, types ajoutés, pièces obligatoires par type |
| Matricule | Format, concurrence, pas de trou ni de doublon |
| Invitation | Tous les rôles avec dossier par le RH ; ADM limité au premier RH ; compte neuf, existant, réembauche, admin qui reçoit un dossier ; idempotence d'`accept()` ; expiration, annulation |
| Hiérarchie | Équipe directe et indirecte, cycle, auto-management, périmètre au web et à l'API |
| Rôle | Changement autorisé, interdit vers ou depuis l'admin sans dossier, journal |
| Sortie | Déclaration, passage automatique, lecture seule, fin d'accès, annulation, réembauche |
| Droits | Permissions `reference_types`, `employee_invitations`, `employees`, `org_chart` ; autre entreprise |
| Plateforme | Effectifs, dépassement de palier |

## 8. Critères de sortie

- Tests ciblés W04.1 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §3.1 et §5.2 jusqu'à l'invitation des employés, sur le jeu de démonstration.
- Documentation et livraison de W04.1.10 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Assistant de complétion, blocs vérifiables, dépôt des pièces | W04.2 |
| Vérification, complétude, relances, alertes d'expiration, cloche | W04.3 |
| Décision du supérieur en l'absence du manager direct | W07 |
| Désactivation de la carte à la sortie | W05 |
| Workflows d'entrée, de sortie, de mutation ; événements | W12 |
| Import Jobyflow | W15 |
| Écrans mobiles (équipe, employés, invitations) | E02 |
