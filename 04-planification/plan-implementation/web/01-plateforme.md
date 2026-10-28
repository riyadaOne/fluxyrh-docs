# W01 — Plateforme

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W00

## 1. Objet

Construire l'espace de RIYADA ONE (`platform.fluxyrh.app`) : connexion des admins plateforme, création et provisionnement des entreprises, abonnements, modules, tableau de bord, journal, fiche « Application mobile », API plateforme pour la future Console et page d'accueil publique. À la fin de W01, l'admin plateforme crée une entreprise depuis l'interface, choisit son palier et ses modules, et peut la suspendre ou la résilier.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PLT-01 | Création et provisionnement d'une entreprise (l'invitation du premier admin est ajoutée en W02) |
| F-PLT-02 | Abonnement `Actif` ⇄ `Suspendu` → `Résilié`, blocage de l'espace |
| F-PLT-03 | Modules par entreprise, journalisés ; middleware `module:` |
| F-PLT-04 | Tableau de bord plateforme (les indicateurs d'effectifs et d'activité s'ajoutent en W02 et W04) |
| F-PLT-07 | Page d'accueil publique `fluxyrh.app` |
| F-PLT-08 | Fiche « Application mobile » : identifiants, export de configuration de build (l'envoi du lien d'installation est ajouté en W02) |
| F-PLT-09 | Factures des entreprises, émission proposée chaque mois (W01.11) |
| T-14 (début) | Sanctum, Scramble, premier contrat d'API (`/api/v1/platform`) |

À lire : PRD §7.1, §8.1 à §8.3 ; TRD §5.3 (provisionnement), §6, §7.1, §7.5, §17 ; APPFLOW §3.6, §4.1, §5.1 ; BACKEND SCHEMA §4.1 à §4.3, §6 (abonnement), §7 ; UX/UI §5, §6.1, §6.10, §14.

## 3. Prérequis

- W00 livré.
- Paquets installés par le développeur à l'étape concernée : `laravel/sanctum` (W01.8), `dedoc/scramble` (W01.8), `laravel/passkeys` (W01.2).

**Décisions à prendre avant de démarrer** :

| Sujet | Proposition |
|---|---|
| Création des admins plateforme | Par commande artisan `fluxyrh:platform-admin` (le premier comme les suivants) ; pas d'écran de gestion des admins en v1 (non prévu par l'APPFLOW) |
| 2FA des admins plateforme | **Obligatoire en production** : un admin sans 2FA confirmée y est renvoyé vers son activation ; désactivable hors production par configuration |
| Palier d'un abonnement | Choisi par l'admin plateforme à la création ; le dépassement selon le nombre d'employés actifs est signalé à partir de W04 |
| Facturation | FluxyRH calcule le prix mensuel et **émet les factures** des entreprises (W01.11) : PDF numéroté, statut à payer, payée ou annulée ; le paiement se fait hors système et la plateforme l'enregistre ; l'émission est **proposée** chaque mois à l'admin plateforme, jamais automatique |
| Page d'accueil `fluxyrh.app` | **Maquette proposée par Claude et validée avant W01.12** ; la vraie page est construite en W01 |
| Enums manquants au BACKEND SCHEMA §7 | Ajout de `SubscriptionStatus` (`actif`, `suspendu`, `resilie`), `BillingFrequency` (`mensuelle`, `annuelle`), `SubscriptionPlanCode` (`moins_25`, `moins_75`, `moins_200`, `sur_devis`), `PlatformMetric` (W01.10) |

## 4. Rôles et statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Entreprise `companies.status` | `inactive` → `active` (fin du provisionnement) | SYS |
| Abonnement `company_subscriptions.status` | `actif` ⇄ `suspendu` → `resilie` | PLT |
| Module `company_modules` | présent (souscrit) ⇄ absent | PLT |

Un abonnement `suspendu` ou `resilie` bloque l'espace de l'entreprise : page « accès suspendu » au web, 403 à l'API. `resilie` est définitif ; l'archive des données à la résiliation est préparée hors système par RIYADA ONE.

## 5. Étapes ordonnées

### W01.1 — Enums et compléments de spécification

- Enums `App\Enums\General\` : `SubscriptionStatus`, `BillingFrequency`, `SubscriptionPlanCode`, `ModuleCode` (BACKEND SCHEMA §7), `PlatformMetric`. Chaque enum porte son libellé traduit (fr, en, ar) et sa couleur de statut quand il est affiché en badge.
- Mise à jour du BACKEND SCHEMA §7 avec les enums ajoutés.

**Critère de fin** : enums testés (valeurs stockées, libellés dans les trois langues).

### W01.2 — Identité et connexion plateforme

- Migrations générales : `users` (BACKEND SCHEMA §4.1, toutes colonnes), `platform_admins`, `passkeys` (structure du paquet).
- Models `User`, `PlatformAdmin` et factories.
- Garde `platform` ; contrôleurs dédiés de connexion, déconnexion, défi 2FA, passkeys ; mot de passe oublié.
- Middleware `EnsurePlatformHost` (routes plateforme seulement sur `PLATFORM_DOMAIN`) et `EnsurePlatformAdmin`.
- 2FA obligatoire en production (décision §3) ; limites de débit `login` et `two-factor` (TRD §7.5).
- Commande `fluxyrh:platform-admin` (création d'un admin, mot de passe saisi par le développeur, jamais affiché ni journalisé).
- Écrans : connexion, défi 2FA, activation 2FA imposée, mot de passe oublié (layout `auth`).

**Critère de fin** : un admin créé par la commande se connecte avec mot de passe + 2FA, puis avec une passkey ; un utilisateur non admin est refusé ; les routes plateforme sont introuvables sur un sous-domaine d'entreprise.

### W01.3 — Paramètres de l'admin plateforme

- `/settings` (layout `platform`, navlist UX/UI §5.3) : profil, mot de passe, 2FA (codes de secours), passkeys, apparence, langue.

**Critère de fin** : chaque réglage modifie le compte et est journalisé (sauf apparence).

### W01.4 — Plans, modules et prix

- Migrations générales : `subscription_plans`, `modules`, `subscription_plan_module_prices`, `company_modules`, `company_subscriptions` (BACKEND SCHEMA §4.2).
- Models et factories.
- Seeder des plans et des prix (PRD §8.3) : 4 paliers, 6 modules (`identite` hors pack), prix des modules par palier (×1 ; ×1,5 ; ×2) ; aucun montant dans le code.
- `App\Services\Platform\SubscriptionPricingService` : prix mensuel d'un abonnement = pack si les 5 modules du pack sont actifs, sinon socle + modules ; + Identité si souscrit ; prix négocié pour `sur_devis` ; annuel = mensuel × 12 − 10 %.

**Critère de fin** : tests du calcul pour chaque palier, avec et sans pack, avec Identité, en annuel, et l'exemple du PRD (199 900 + 14 900 = 214 800).

### W01.5 — Création et provisionnement d'une entreprise

- Migration : ajout à `companies` de `mobile_android_package`, `mobile_ios_bundle_id`, `mobile_android_url`, `mobile_ios_url` (utilisés en W01.9).
- Validation du slug : minuscules, chiffres, tirets ; mots réservés (`platform`, `www`, `api`, `admin`, `mail`…) ; longueur compatible avec le nom de base MySQL (64 caractères) ; **non modifiable** après création.
- `App\Services\Platform\CompanyService::create()` : crée l'entreprise `inactive`, son abonnement `actif`, ses modules, puis lance le provisionnement.
- `CompanyProvisioningService` (W00.6) complété : étapes abonnement et modules, passage à `active`, journal plateforme. Exécuté dans un job (création de base et migrations) ; en cas d'échec, l'entreprise reste `inactive` avec l'étape en erreur et un bouton « Reprendre » (étapes idempotentes).
- Écrans `/companies` : liste (statut, palier, modules, prix mensuel), création (nom, slug, fuseau, devise, langue officielle, palier, fréquence, prix négocié si `sur_devis`, modules), fiche entreprise (onglets Identité, Abonnement, Modules, Application mobile ; Journal de l'entreprise côté plateforme).
- Modification : nom, fuseau, langue officielle. La devise reste modifiable jusqu'en W09 (verrouillage à la première rubrique de paie).

**Critère de fin** : depuis l'interface, une entreprise est créée, sa base existe sur MySQL, son sous-domaine affiche la page d'attente ; un provisionnement interrompu reprend sans erreur.

### W01.6 — Abonnements

- `App\Services\Platform\SubscriptionService` : `suspend()`, `resume()`, `terminate()` (définitif), `changePlan()`, `changeFrequency()` ; chaque transition vérifie l'état de départ, s'écrit en transaction et se journalise.
- Blocage de l'espace : `ResolveCompany` (W00.5) ou un middleware dédié renvoie la page « accès suspendu » (web) ou 403 (API) si l'abonnement n'est pas `actif`. `CheckCompanyAccess` (W02) reprendra ce contrôle pour les sessions ouvertes.
- Écran `/subscriptions` : liste de tous les abonnements (filtres statut, palier, fréquence), actions avec confirmation et motif pour suspension et résiliation.

**Critère de fin** : suspendre bloque immédiatement le sous-domaine ; reprendre le rouvre ; un abonnement résilié ne peut plus changer d'état.

### W01.7 — Modules

- `App\Services\Platform\CompanyModuleService` : activation et désactivation, journalisées (F-PLT-03) ; le prix est recalculé.
- `App\Services\Tenancy\ModuleGate` : `enabled(ModuleCode)` pour l'entreprise courante, mis en cache pour la requête.
- Middleware `EnsureModule` (alias `module`) : 404 « module non souscrit » au web, réponse d'erreur dédiée à l'API (TRD §6.2).
- `CompanyFactory::withoutModules()` et `withModules([...])` (TRD §24).
- Onglet « Modules » de la fiche entreprise.

**Critère de fin** : une route de test protégée par `module:pilotage` répond pour une entreprise qui a le module et renvoie « module non souscrit » sinon, au web comme à l'API.

### W01.8 — API plateforme

- Installation de Sanctum (jetons à UUID, suppression logique) et de Scramble.
- Migration générale `personal_access_tokens` (BACKEND SCHEMA §4.1) ; ability `platform`.
- Chaîne `api` plateforme : `EnsurePlatformHost` → `EnsureSupportedAppVersion` (426, version minimale de la Console en configuration) → `auth:sanctum` → `EnsurePlatformAdmin`.
- Points d'API `/api/v1/platform` : `login` (mot de passe + 2FA, 422 `two_factor`), `logout`, `me`, `dashboard` (indicateurs), `companies` (liste, fiche : statut, palier, modules ; l'effectif s'ajoute en W04, les factures en W01.11), `activity-log` (lecture) : tout ce que la Console lit (C02). La file des cartes arrive en W05.
- Commande `api:contract` et test « contrat à jour » (TRD §17.2).

**Critère de fin** : un client HTTP de test se connecte, liste les entreprises, est refusé sans 2FA, sans ability `platform` ou sous la version minimale ; le contrat OpenAPI est généré.

### W01.9 — Fiche « Application mobile »

- Onglet de la fiche entreprise : identifiant Android, bundle iOS, liens des stores (uniques entre entreprises).
- Export de la configuration de build (flavor) : fichier téléchargeable avec nom de l'app, identifiants, URL de l'API (`https://{slug}.fluxyrh.app`), slug, couleur de fond de l'icône adaptative : format complet dès W01.9.
- Colonnes `mobile_android_sha256` (empreinte du certificat de signature Android) et `mobile_ios_team_id` (identifiant d'équipe Apple) sur `companies`, champs de la fiche ; routes `/.well-known/assetlinks.json` et `/.well-known/apple-app-site-association` servies par chaque sous-domaine d'entreprise (vides tant que les champs ne sont pas renseignés) ; BACKEND SCHEMA mis à jour.
- L'envoi du lien d'installation après acceptation d'une invitation est ajouté en W02.

**Critère de fin** : export téléchargé conforme ; doublon d'identifiant refusé.

### W01.10 — Tableau de bord et journal plateforme

- Migrations générales : `platform_statistics_snapshots`, `platform_dashboard_widget_selections`.
- Commande planifiée nocturne `fluxyrh:platform-snapshot` : nombre d'entreprises par statut, abonnements par palier et par statut, revenu récurrent mensuel. Les indicateurs d'activité (connexions, W02) et d'effectifs (employés actifs, dépassement de palier, W04) s'ajoutent dans ces modules.
- `/dashboard` : widgets choisis et ordonnés par chaque admin (UX/UI §6.10), sans donnée nominative ni salariale.
- `/activity-log` : journal plateforme (filtres entreprise, action, auteur, période ; export).

**Critère de fin** : le tableau de bord affiche les valeurs du dernier instantané ; le revenu récurrent correspond au calcul de W01.4.

### W01.11 — Factures des entreprises

- Paquets installés par le développeur : `barryvdh/laravel-dompdf`, `khaled.alshamaa/ar-php`.
- Création de `App\Services\Documents\DocumentRenderer` (rendu HTML → PDF, A4, trois langues, arabe par ar-php), utilisé ici pour la première fois ; en-tête de RIYADA ONE (identité légale saisie dans les paramètres de la plateforme).
- Migrations générales `platform_invoices` (entreprise, numéro, période, palier, montant, devise FCFA, statut, dates d'émission et de paiement, référence de paiement, PDF et empreinte) et `platform_invoice_lines` (socle, pack, modules, option Identité, remise annuelle) ; BACKEND SCHEMA §4.2 mis à jour.
- `App\Services\Platform\InvoiceService` : chaque mois, l'écran **propose** les factures à émettre (montants calculés par W01.4) ; l'admin plateforme les relit et les émet (aucune émission automatique) ; numéro `FAC-{annee}-{sequentiel}` sans trou ; PDF figé ; statut `a_payer` → `payee` (paiement fait hors système, enregistré par la plateforme) ou `annulee` (motif, avoir non prévu en v1).
- Écran plateforme `/invoices` ; onglet Factures de la fiche entreprise ; l'admin de l'entreprise consulte et télécharge ses factures dans son espace (Configuration, onglet Abonnement).

**Critère de fin** : les factures d'un mois correspondent au calcul de W01.4 ; numérotation continue ; une facture payée ou annulée ne change plus.

### W01.12 — Page d'accueil publique

- `fluxyrh.app` (layout `public`) : présentation noir et blanc, sans prix ni formulaire, coordonnées de RIYADA ONE, trois langues, mode sombre, lien discret vers la plateforme (UX/UI §14) ; d'après la maquette validée (§3).

**Critère de fin** : page lisible en fr, en, ar (RTL), clair et sombre, sur mobile et sur ordinateur.

### W01.13 — Documentation et livraison

- `02-reference/` : espace plateforme (écrans, services, API, commandes) ; BACKEND SCHEMA §7 mis à jour (W01.1).
- `07-exploitation/` : création d'un admin plateforme, création et reprise d'un provisionnement.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W01 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Connexion | Mot de passe + 2FA, passkey, 2FA imposée en production et non hors production, utilisateur non admin refusé, limites de débit, routes plateforme absentes des sous-domaines |
| Création | Slug invalide, réservé, en double, trop long ; provisionnement complet ; reprise après échec ; journal |
| Prix | Chaque palier, pack, socle + modules, Identité hors pack, annuel −10 %, `sur_devis` |
| Factures | Proposition mensuelle sans émission automatique, montant égal au calcul, numérotation sans trou, PDF figé, transitions |
| Abonnement | Chaque transition autorisée ; transitions interdites (`resilie` → tout) ; blocage web et API immédiat |
| Modules | Activation et désactivation journalisées ; route `module:` ouverte ou fermée, web et API |
| API | Connexion, 2FA, ability, version minimale (426), contrat à jour |
| Application mobile | Unicité des identifiants, export |
| Tableau de bord | Instantané nocturne, aucune donnée nominative |

## 7. Critères de sortie

- Tests ciblés W01 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.1 jusqu'à l'activation de l'entreprise (l'invitation du premier admin est recettée en W02).
- Documentation et livraison de W01.13 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Invitation du premier admin à la création, lien d'installation de l'app | W02 |
| Indicateurs de connexions | W02 |
| Effectifs, dépassement de palier | W04 |
| File des cartes à encoder (web et API) | W05 |
| Saisie des empreintes et publication des apps | E10 |
| Écrans de la Console | C00 à C02 |
