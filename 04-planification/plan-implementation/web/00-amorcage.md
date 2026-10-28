# W00 — Amorçage technique

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : —

## 1. Objet

Poser le socle technique sur lequel tous les modules s'appuient : projet Laravel, multi-entreprise, chiffrement par entreprise, journal d'audit, files d'attente, e-mails, langues, interface de base et outillage de tests. **Aucune fonction métier** : à la fin de W00, une entreprise créée en ligne de commande s'ouvre sur son sous-domaine et affiche une page vide dans le layout de l'application, en trois langues.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| T-01, T-02, T-03, T-17 | Base par entreprise, résolution par hôte, jobs reconnectés, migrations des entreprises |
| T-06 | UUID v7, suppression logique, `$fillable`, pas de JSON, montants décimaux |
| T-07, T-08 | Trois langues, `Money`, aucun montant ni devise en dur |
| T-09 (chiffrement) | Clé de données par entreprise, cast chiffré (l'accès par champ `FieldAccess` vient en W02) |
| T-16, T-19 | Secrets hors dépôt, Pint |
| F-ADM-08 (écriture), F-ADM-09 (composant), F-COM-02 (infrastructure) | Journal, corbeille, e-mails |
| NF-01, NF-03, NF-07, NF-13 | Cloisonnement, traçabilité, multilingue, conservation |

À lire avant de commencer : TRD §2 à §6, §9.3, §19 à §26 ; BACKEND SCHEMA §1 à §4, §5.15 (`activity_logs`, `activity_log_changes`) ; UX/UI DESIGN §2 à §5, §10, §11, §15, §17.

## 3. Prérequis

**Poste du développeur** (Windows) : PHP 8.5 avec `intl`, `bcmath`, `pdo_mysql`, `pdo_sqlite`, `sodium` ; Composer ; Node LTS ; MySQL 8 ; installateur Laravel ; mkcert ; Git.

**Décisions à prendre avant de démarrer** :

| Sujet | Proposition |
|---|---|
| Domaines de développement | `*.fluxyrh.test` (fichier hosts ou résolveur local) et `*.127.0.0.1.nip.io` en secours |
| Niveau Larastan | Niveau 6 au départ, relevé plus tard |
| Dépôt GitHub | `riyadaOne/fluxyrh-w-app`, privé, branche `main` |

## 4. Rôles et statuts traversés

Aucun rôle métier. Un seul statut : `CompanyStatus` (`inactive`, `active`) sur `companies`, nécessaire à la résolution. Les autres valeurs et le cycle d'abonnement arrivent en W01.

## 5. Étapes ordonnées

### W00.1 — Création du projet (développeur)

- Création du projet `FluxyRH-web/app/` à partir du **starter kit Livewire** de Laravel 13 (Livewire 4, Flux UI, Fortify). La commande exacte est vérifiée dans la documentation à jour au moment de l'étape, puis donnée au développeur.
- Installation de Laravel Boost (`boost:install`) ; vérification que le serveur MCP `laravel-boost` de `FluxyRH-docs/claude/mcp.json` se connecte.
- `git init`, premier commit, dépôt `riyadaOne/fluxyrh-w-app`.
- Paquets de développement : Larastan.
- Retrait de ce que le starter kit apporte et que FluxyRH n'utilise pas : inscription publique (TRD §7.1). Les écrans de connexion restent pour W02.

**Critère de fin** : `composer run dev` sert la page d'accueil ; `php artisan test` passe ; le MCP Boost répond.

### W00.2 — Conventions du projet

- `CLAUDE.md` du projet (généré par Boost) complété par une section FluxyRH : conventions du TRD §4.3 et §23, pièges du TRD §26, règles du multi-entreprise.
- `AppServiceProvider` : `Date::use(CarbonImmutable::class)`, `Model::shouldBeStrict()` hors production, `Model::preventLazyLoading()`.
- Traits et classes de base :
  - `App\Models\Concerns\` : UUID v7, suppression logique ;
  - `App\Models\Tenant\TenantModel` : connexion `tenant`, UUID v7, suppression logique ;
  - modèle de migration de référence (UUID, horodatages, `softDeletes`, contraintes nommées).
- `.env.example` complet, sans valeur secrète ; `.gitignore` vérifié (`.env`, clés, `storage/app/private`).
- Larastan configuré (`phpstan.neon`), Pint configuré.

**Critère de fin** : un model d'exemple de test respecte les conventions ; Larastan et Pint passent.

### W00.3 — Connexions et domaines

- `config/database.php` : connexion `general` (par défaut, `fluxyrh_general`) et connexion `tenant` (base réécrite à la volée).
- `config/fluxyrh.php` : `PLATFORM_DOMAIN`, `TENANT_BASE_DOMAIN`, alias de développement, préfixe des bases (`fluxyrh_ent_`).
- Fichiers de routes : `web.php` (accueil racine), `platform.php`, `tenant.php`, `settings.php`, `api.php`, `console.php`. Routes plateforme enregistrées dans `AppServiceProvider::register()` (piège 2).
- Dossiers de migrations : `database/migrations/` (générale) et `database/migrations/tenant/`.

**Critère de fin** : `platform.fluxyrh.test` et `{slug}.fluxyrh.test` atteignent chacun leur fichier de routes.

### W00.4 — Base générale minimale

- Enum `App\Enums\General\CompanyStatus` (`inactive`, `active`).
- Migration `companies` limitée aux colonnes du multi-entreprise : `id`, `name`, `slug`, `database_connection_name`, `currency_code`, `official_locale`, `timezone` (sans valeur par défaut : choisis à la création de l'entreprise, décision 0002), `status` = `inactive`. Les colonnes `mobile_*` (W01) et `card_login_enabled` (W05) sont ajoutées par leurs modules.
- Migration `company_data_keys` (BACKEND SCHEMA §4.2).
- Models `Company`, `CompanyDataKey` et leurs factories.

**Critère de fin** : migrations générales passées sur SQLite et sur MySQL.

### W00.5 — Résolution de l'entreprise

- `App\Services\Tenancy\TenantConnectionResolver::connectTo(Company)` : réécrit la base `tenant`, purge la connexion, applique le fuseau, charge la clé de données (W00.7).
- `App\Services\Tenancy\CompanyContext` (singleton) : `current()` ; `currentRattachement()` est ajouté en W02.
- Middleware `ResolveCompany` : slug lu depuis le **nom d'hôte**, alias de développement acceptés ; hôte inconnu ou entreprise `inactive` → 404. Placé avant `auth` (`prependToPriorityList`, piège 4) et global au groupe `web` (piège 3).
- Middleware `SetLocale` (langue de session, sinon langue officielle de l'entreprise, sinon `fr`).

**Critère de fin** : tests « hôte connu », « hôte inconnu », « entreprise inactive », « deux entreprises ne voient pas leurs données respectives ».

### W00.6 — Provisionnement et migrations des entreprises

- `App\Services\Tenancy\CompanyProvisioningService` : étapes **idempotentes** création de la base → migrations `tenant` → clé de données → journal. Les étapes métier (abonnement, modules, premier admin, pré-paramétrage de paie) s'ajoutent dans leurs modules (W01, W02, W09.1).
- Commande `fluxyrh:provision {slug}` : entreprise neuve uniquement, **efface la base**, confirmation obligatoire, refusée en production.
- Migration des entreprises existantes : commande `fluxyrh:migrate-tenants` (une entreprise ou toutes, arrêt propre à la première erreur) ; `deploy/debian/migrate-tenants.php` l'appelle (le reste de `deploy/debian/` est fait en MEP).

**Critère de fin** : deux entreprises provisionnées sur MySQL local ; une nouvelle migration `tenant` appliquée aux deux par la commande ; relancer le provisionnement d'une étape déjà faite ne casse rien.

### W00.7 — Chiffrement par entreprise

- Clé maître `FLUXYRH_MASTER_KEY` lue dans l'environnement (jamais en base, jamais versionnée) ; commande de génération pour le poste de développement.
- `App\Services\Tenancy\CompanyKeyService` : génération d'une DEK (AES-256-GCM), enveloppement par la clé maître, déballage et mise en cache pour la requête, une seule clé active par entreprise.
- Cast `App\Casts\EncryptedWithCompanyKey` (colonne `text`).
- Commande de rotation de la clé maître (ré-enveloppement des DEK). Le rechiffrement des données après rotation d'une DEK attend la première colonne chiffrée (W02 ou W04).

**Critère de fin** : aller-retour chiffrement / déchiffrement ; valeur illisible en base ; la clé d'une entreprise ne déchiffre pas la donnée d'une autre ; rotation de la clé maître sans perte.

### W00.8 — Journal d'audit (écriture)

- Migrations `tenant` : `activity_logs`, `activity_log_changes` (BACKEND SCHEMA §5.15), sans suppression logique.
- Migration générale : `activity_logs` (journal plateforme, miroir **sans valeurs**).
- `App\Services\ActivityLogger` : `log(action, subject, 'activity.key', params, before:, after:)`, `logAsSystem()` ; description stockée en fr, en, ar ; IP et appareil ; valeurs sensibles stockées chiffrées (le choix du champ sensible s'appuie sur l'enum créé en W02 ; d'ici là, aucune valeur sensible n'existe).
- Models en lecture seule (aucune mise à jour ni suppression possible par Eloquent).

L'écran du journal est construit en W02.

**Critère de fin** : une action écrit une ligne d'entreprise et une ligne plateforme sans valeurs ; modifier ou supprimer une ligne lève une exception.

### W00.9 — Files d'attente, tâches planifiées, e-mails

- `QUEUE_CONNECTION=database`, tables `jobs`, `job_batches`, `failed_jobs` ; cache et sessions en base.
- Classe de base `App\Jobs\TenantJob` : ne porte que `companyId` et des identifiants scalaires, appelle `connectTo()` dans `handle()` (piège 7, T-03).
- Planificateur : `routes/console.php` prêt ; les tâches arrivent avec leurs modules.
- E-mails : transport SMTP configuré par l'environnement ; layout d'e-mail neutre (logo et nom de l'entreprise), dans la **langue officielle** de l'entreprise ; classe de base des notifications e-mail mises en file après commit. Aucun e-mail métier n'est encore envoyé (premier usage : invitation, W02).

**Critère de fin** : un job de test exécuté par le worker se reconnecte à la bonne entreprise ; un e-mail de test part dans la langue officielle (vérifié dans le journal de mail local).

### W00.10 — Langues, devise, fuseau

- `lang/{fr,en,ar}/` : fichiers PHP par module (`common.php`, `activity.php`…), notation `__('module.key')` (piège 5) ; les trois langues livrées ensemble.
- `dir="rtl"` pour l'arabe dans tous les layouts ; polices arabes (UX/UI §4.3).
- `App\Support\Money` : formatage selon `companies.currency_code` et la langue, montant en lettres (fr, en, ar) ; calcul décimal (`brick/math` ou `bcmath`, à trancher à cette étape).
- `App\Support\CompanyTimezone` : conversion UTC ↔ fuseau de l'entreprise (le fuseau d'un site arrive en W03).
- Test de cohérence : chaque clé présente en fr existe en en et en ar.

**Critère de fin** : test de cohérence des fichiers de langue ; tests de `Money` (XAF sans décimales, montant en lettres dans les trois langues).

### W00.11 — Interface de base

- Tokens UX/UI §4 dans `resources/css/app.css` (couleurs de base et de statut, clair et sombre), polices Instrument Sans, IBM Plex Sans Arabic, IBM Plex Mono ; thème Clair / Sombre / Système.
- Layouts squelettes (UX/UI §5.1) : `app/sidebar` (barre latérale vide, menu utilisateur avec langue, thème et déconnexion), `platform`, `me`, `auth`, `public`. Les entrées de menu sont ajoutées par chaque module.
- Composants transverses (UX/UI §6.1, §6.11, §10) : badge de statut (enum → couleur de statut), écran de liste type (recherche, filtres, pagination, état vide), **corbeille** réutilisable (onglet « Corbeille », restauration journalisée, F-ADM-09), modale de confirmation, sélecteur de langue.
- Page d'attente de l'espace entreprise (« espace en préparation »), remplacée en W02 par la connexion.

**Critère de fin** : la page d'attente s'affiche en fr, en, ar (RTL), en clair et en sombre ; liste de contrôle UX/UI §17 passée sur les composants.

### W00.12 — Outillage de tests

- `phpunit.xml` : base générale SQLite en mémoire, base d'entreprise en fichier SQLite temporaire.
- Trait `Tests\Concerns\InteractsWithCompanies` : `createActiveCompany()`, connexion à l'entreprise, nettoyage.
- `CompanyFactory` (états `active`, `inactive`) ; `withoutModules()` arrive en W01 avec les modules.
- Factories des models d'entreprise dans `database/factories/Tenant/`.
- Tests d'architecture : aucun `$guarded = []`, aucun model sans UUID, aucun model d'entreprise sur la connexion `general`, aucun job portant un model d'entreprise.

**Critère de fin** : la suite W00 passe en moins de 30 s ; les tests d'architecture échouent sur un contre-exemple volontaire.

### W00.13 — Environnement de développement

- `composer run dev` : serveur, worker, Vite, proxy TLS local (mkcert, utile aux passkeys en W02).
- Résolution des sous-domaines locaux documentée (hosts ou résolveur, nip.io en secours).
- Seeder de développement : deux entreprises de démonstration provisionnées (`demo`, `essai`).
- Vérifications sur MySQL des points invisibles en SQLite : longueur des noms de contraintes (piège 6), provisionnement, chiffrement.

**Critère de fin** : depuis un poste propre, la procédure documentée mène à `https://demo.fluxyrh.test` en moins de 15 minutes.

### W00.14 — Documentation et livraison

- `02-reference/` : architecture réelle (connexions, middlewares, services de tenancy, commandes).
- `07-exploitation/` : procédure d'installation du poste de développement.
- Livraison `06-livraisons/`, ligne au `JOURNAL.md`, statut W00 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Résolution | Hôte connu, inconnu, alias de développement, entreprise inactive |
| Cloisonnement | Une donnée créée dans l'entreprise A est introuvable depuis B (NF-01) |
| Jobs | Un job se reconnecte à son entreprise ; un job portant un model est refusé (test d'architecture) |
| Chiffrement | Aller-retour, illisible en base, clé d'une autre entreprise refusée, rotation de la clé maître |
| Journal | Écriture entreprise + miroir plateforme sans valeurs, `logAsSystem`, immuabilité |
| Langues | Cohérence des clés fr / en / ar, RTL |
| Money | Format XAF, montant en lettres dans les trois langues |
| Corbeille | Suppression logique, restauration journalisée |
| Provisionnement | Idempotence, refus en production, migration de toutes les entreprises |

## 7. Critères de sortie

- Tests ciblés W00 verts ; suite complète lancée par le développeur.
- Pint et Larastan sans erreur.
- `https://demo.fluxyrh.test` et `https://essai.fluxyrh.test` affichent la page d'attente, chacune avec son nom, en trois langues.
- Vérifications MySQL de W00.13 faites.
- Documentation et livraison de W00.14 faites.

## 8. Reporté

- Écran du journal, `FieldAccess`, permissions : W02.
- Notifications in-app et cloche : W04.3.
- Push : W10 (serveur) et E08 (app).
- Scripts de production `deploy/debian/` (sauf `migrate-tenants.php`), sauvegardes : MEP.
