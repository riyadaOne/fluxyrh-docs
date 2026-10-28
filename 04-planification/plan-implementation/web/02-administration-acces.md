# W02 — Administration et accès

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W01

## 1. Objet

Ouvrir l'espace de l'entreprise à ses utilisateurs : invitation et rattachement, connexion web et mobile, politique de mot de passe et 2FA, matrice des droits par écran, mécanique des champs sensibles, utilisateurs connectés, configuration de l'entreprise et journal d'audit. À la fin de W02, l'admin plateforme crée une entreprise, son premier admin reçoit l'invitation, définit son mot de passe, se connecte, configure l'entreprise, invite d'autres admins, règle les droits et consulte le journal ; l'API d'authentification mobile est prête.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ADM-01, 02 | Invitation (comptes admin sans dossier), rattachement, fin d'accès |
| F-ADM-03 | Matrice des droits, délégations, exclusions, écrans de module grisés |
| F-ADM-04 | `FieldAccess` et enum `SensitiveField` (mécanique ; appliquée par chaque module qui stocke un champ sensible) |
| F-ADM-05 | Politique de mot de passe, 2FA imposée par rôle |
| F-ADM-06 | Utilisateurs connectés, déconnexion forcée |
| F-ADM-07 | Configuration : identité de l'entreprise, langue officielle, fuseau, devise (onglets matricule, pointage, relances ajoutés par W04 et W06) |
| F-ADM-08 | Écran du journal d'audit, filtres, export |
| F-COM-02 | Premier e-mail transactionnel : invitation |
| F-PLT-01, 08 (fin) | Invitation du premier admin à la création ; lien d'installation de l'app après acceptation |
| F-MOB-05 (serveur) | Version minimale d'app imposée par l'API (426) |
| T-05, T-09, T-14 | Contrôles côté serveur, champs sensibles, contrat d'API |

À lire : PRD §6 (P6), §7.2 ; TRD §6, §7, §8, §9, §17, §21 ; APPFLOW §3.1 à §3.3, §4.2, §5.2, §5.19, §6.1, §7, §8 ; BACKEND SCHEMA §4.1, §5.1, §5.15, §7, §8 ; UX/UI §5, §6.1, §6.2, §6.9.

## 3. Prérequis

- W01 livré.
- Paquet installé par le développeur : `openspout/openspout` (exports, W02.8).

**Décisions à prendre avant de démarrer** :

| Sujet | Proposition |
|---|---|
| Stockage de l'invitation « compte sans dossier » | Le BACKEND SCHEMA ne prévoit que `employee_invitations`, dont l'affectation (poste, structure, site) est obligatoire et n'existe qu'à partir de W03. Ajout d'une table d'entreprise **`account_invitations`** : `id`, `email`, `first_name`, `last_name`, `role` (= `admin_entreprise`), `access_ends_at` dt?, `status` = `brouillon`, `token_hash` str64?, `sent_at`, `expires_at`, `accepted_at`, `user_company_id` uuid?, `invited_by` ⇢ uc ? (nul pour une invitation de la plateforme). Même cycle `InvitationStatus`, même page `/invitation/{jeton}`, même service. BACKEND SCHEMA §5.3 mis à jour |
| Rôles invitables en W02 | `admin_entreprise` seulement (sans dossier, APPFLOW §8). Les invitations RH, PAIE, DIR, MGR, EMP portent un dossier et arrivent en W04.1 |
| Changement de rôle d'un rattachement | Non prévu par les spécifications ; à trancher en W04.1, quand les rôles avec dossier existent |
| Version minimale des apps | Une valeur par app (`entreprise`, `borne`, `console`) en configuration d'environnement, lue par `EnsureSupportedAppVersion` ; en-têtes `X-App-Id` et `X-App-Version` |
| Format des exports | CSV et XLSX |
| Permissions d'écran | L'enum `Permission` grandit avec les écrans : W02 ajoute `users`, `invitations`, `connected_users`, `activity_log`, `configuration` ; chaque module ajoute les siennes |

## 4. Rôles et statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Invitation `account_invitations.status` | `brouillon` → `envoyee` → `acceptee` / `expiree` / `annulee` ; `expiree` → renvoi | PLT (premier admin), ADM ; la personne accepte ; SYS fait expirer après 7 jours |
| Rattachement `user_company.status` | `invite` → `actif` ⇄ `suspendu` → `revoque` | Créé `invite` à l'envoi ; `actif` à l'acceptation ; ADM suspend, reprend, révoque ; SYS révoque à `access_ends_at` |

La révocation n'efface ni l'identité ni l'historique ; elle supprime les sessions et révoque les jetons.

## 5. Étapes ordonnées

### W02.1 — Enums et compléments de spécification

- `App\Enums\General\UserCompanyRole`, `UserCompanyStatus` ; `App\Enums\Tenant\InvitationStatus`, `Permission` (valeurs de W02, rôles par défaut, `requiredModule()`), `SensitiveField` (catégories et champs, vide de champs tant qu'aucun module n'en stocke).
- BACKEND SCHEMA : table `account_invitations` (§5.3), mention de la croissance progressive de `Permission` (§7).

**Critère de fin** : enums testés ; spécification à jour.

### W02.2 — Rattachements

- Migrations générales : `user_company`, `password_histories` ; ajout de `company_id` à `sessions`.
- Model `UserCompany` et factory (un état par rôle et par statut).
- `App\Services\Tenant\RattachementService` : `activate()`, `suspend()`, `resume()`, `revoke(reason)`, `expire()` (système) ; vérification de l'état de départ, transaction, journal, purge des sessions et jetons à la suspension et à la révocation.
- `CompanyContext::currentRattachement()`.

**Critère de fin** : chaque transition et chaque transition interdite testées ; une révocation coupe une session ouverte.

### W02.3 — Invitations de compte

- Migration d'entreprise `account_invitations`.
- `App\Services\Tenant\InvitationService` : `createDraft()`, `send()` (rattachement `invite`, jeton haché, lien signé valable 7 jours), `resend()`, `cancel()`, `accept()` (compte neuf : mot de passe selon la politique de l'entreprise ; compte existant : « se connecter pour accepter »), tâche planifiée `expire()`.
- Page publique `/invitation/{jeton}` (layout `auth`) : jeton invalide, expiré, annulé ou déjà utilisé traités par des messages clairs.
- E-mail d'invitation (F-COM-02) dans la langue officielle ; après acceptation, e-mail du lien d'installation de l'app si les liens des stores sont renseignés (F-PLT-08).
- Plateforme : champ « e-mail du premier admin » à la création d'une entreprise ; étape de provisionnement « inviter le premier admin » ; état de l'invitation sur la fiche entreprise, renvoi possible.

**Critère de fin** : parcours APPFLOW §3.1 (branche « compte sans dossier ») recetté pour un compte neuf et pour une personne déjà rattachée à une autre entreprise.

### W02.4 — Connexion web de l'entreprise

- Fortify configuré pour les sous-domaines d'entreprise (inscription désactivée) : connexion par mot de passe ou passkey, défi 2FA, mot de passe oublié, confirmation du mot de passe.
- Une identité ne se connecte que si elle a un rattachement `actif` dans l'entreprise de l'hôte.
- Chaîne `web` complète (TRD §6.2) : `SetLocale` → `ResolveCompany` → `SetPasskeysAllowedOrigin` → `CheckCompanyAccess` → `EnforcePasswordPolicy`. `CheckCompanyAccess` déconnecte avec message si le rattachement est suspendu, révoqué ou arrivé à `access_ends_at`, ou si l'abonnement n'est pas actif (reprend le contrôle de W01.6).
- Limites de débit `login`, `two-factor`.
- Arrivée sur `/dashboard` du rôle (APPFLOW §3.2).

**Critère de fin** : APPFLOW §3.2 recetté ; une personne rattachée à A ne peut pas se connecter sur B.

### W02.5 — Politique de mot de passe et 2FA

- Migrations d'entreprise : `password_policies` (une ligne, valeurs par défaut du BACKEND SCHEMA §5.1), `two_factor_required_roles`.
- `App\Services\Tenant\PasswordPolicyService` : règles de l'entreprise ; nouveau mot de passe conforme à la politique **la plus stricte** des entreprises actives de la personne ; historique des N derniers ; expiration.
- Middleware `EnforcePasswordPolicy` : changement imposé (S-07) si le mot de passe a expiré ou n'est pas conforme ; configuration de la 2FA imposée si le rôle l'exige.
- Onglet « Mots de passe » de la Configuration (W02.9).

**Critère de fin** : un mot de passe non conforme ou expiré impose le changement ; une personne rattachée à deux entreprises reçoit la règle la plus stricte ; la 2FA imposée à un rôle bloque l'accès jusqu'à sa configuration.

### W02.6 — Droits par écran

- Migrations d'entreprise : `role_permission_overrides`, `permission_exclusions`.
- `App\Services\Tenant\PermissionService::allows(Permission)` : rôles par défaut + délégations − exclusions ; module manquant prioritaire (TRD §8) ; mise en cache pour la requête.
- Protection des routes Livewire (middleware et autorisation dans les composants) ; barre latérale filtrée par rôle, permission et module (UX/UI §5.2).
- Écran S-04 `/roles-permissions` (ADM, non délégable) : matrice écrans × rôles, défauts signalés, écrans de modules non souscrits grisés, panneau « Exclusions », rappel fixe « les champs sensibles ne se délèguent pas » (UX/UI §6.9). Changements journalisés, effet immédiat.

**Critère de fin** : délégation, exclusion et module manquant testés sur une route de chaque écran de W02, au web et à l'API.

### W02.7 — Champs sensibles

- `App\Support\FieldAccess::canRead(SensitiveField, ?Employee)` et `canWrite()` : matrice **codée** du TRD §9.1 (catégories `remuneration_contractuelle`, `remuneration_paie`, `bancaire`), jamais délégable ; l'admin entreprise n'a jamais accès ; « employé concerné » branché quand le dossier existe (W04).
- `ActivityLogger` : valeurs avant / après d'un champ sensible stockées chiffrées et affichées selon `FieldAccess`.
- Outil de test de **non-fuite** : assertion réutilisable qui vérifie qu'une réponse web, une réponse API ou un export ne contient aucune valeur sensible d'un jeu de données ; chaque module qui stocke un champ sensible l'applique à ses écrans, exports et points d'API.
- Le journal des consultations sensibles (`sensitive_data_views`, TRD §9.4) est créé avec la première donnée sensible (coordonnées bancaires, W04.2).

**Critère de fin** : matrice de `FieldAccess` testée rôle par rôle et catégorie par catégorie.

### W02.8 — Utilisateurs, connectés, journal

- S-02 `/users` : rattachements de l'entreprise (rôle, statut, fin d'accès, dernière connexion) ; suspendre, reprendre, révoquer (motif), modifier la fin d'accès.
- S-03 `/invitations` : invitations de compte (créer, envoyer, renvoyer, annuler) ; corbeille des invitations annulées.
- S-05 `/connected-users` : sessions web actives et jetons mobiles utilisés récemment ; déconnexion forcée d'une session ou d'un jeton, journalisée (TRD §7.3).
- S-06 `/activity-log` : filtres (utilisateur, action, objet, période), détail avec valeurs avant / après selon `FieldAccess`, IP, appareil ; export CSV et XLSX.

**Critère de fin** : chaque écran testé pour l'ADM, pour un rôle délégué, pour une personne exclue ; une déconnexion forcée coupe effectivement la session ou le jeton.

### W02.9 — Configuration de l'entreprise

- Migrations d'entreprise `company_profile`, `company_legal_identifiers`.
- S-10 `/configuration` (navlist UX/UI §5.3), onglets de W02 :
  - **Entreprise** : raison sociale, nom commercial, logo (disque privé), adresse, ville, téléphone, e-mail, secteur, et **identifiants légaux** (liste paramétrable : libellé, valeur, affiché ou non sur les documents, ordre ; table `company_legal_identifiers` ajoutée au BACKEND SCHEMA, colonnes `rccm`, `niu`, `cnps_employer_number` retirées de `company_profile`) ;
  - **Langue, fuseau, devise** : modifient `companies` par un service (devise modifiable jusqu'au verrouillage de W09.1) ;
  - **Mots de passe** : politique et rôles soumis à la 2FA (W02.5).
- Les onglets Matricule (W04.1), Relances (W04.3), Pointage (W06.1) sont ajoutés par leurs modules.
- Tout changement journalisé avec valeurs avant / après.

**Critère de fin** : chaque onglet enregistre et journalise ; le logo apparaît dans le layout et l'e-mail d'invitation.

### W02.10 — Espaces de travail

- `/dashboard` par rôle ; pour l'ADM, **liste de démarrage** (APPFLOW §5.2) dont chaque module ajoute ses étapes (W02 : configuration de l'entreprise, politique de mot de passe).
- Paramètres personnels `/settings` (UX/UI §5.2) : profil, mot de passe (S-07), 2FA et codes de secours, passkeys, apparence, langue.
- Barre latérale : groupe « Administration » (utilisateurs, invitations, rôles et permissions, connectés, journal) ; menu utilisateur (Paramètres, Configuration, Déconnexion). L'entrée « Aide » arrive en W10.

**Critère de fin** : liste de contrôle UX/UI §17 passée sur chaque écran de W02, en fr, en, ar.

### W02.11 — Expiration des accès

- Tâche planifiée quotidienne : rattachements dont `access_ends_at` est dépassé → `revoque` (`logAsSystem`), jetons révoqués (TRD §7.4).

**Critère de fin** : test avec horloge simulée ; la personne est déconnectée à la requête suivante même avant le passage de la tâche.

### W02.12 — API d'authentification et d'administration

- Chaîne `api` d'entreprise (TRD §6.3) : `ResolveCompany` → `EnsureSupportedAppVersion` (426) → `auth:sanctum` → `EnsureApiRattachement` (ability `company:{id}`) → `EnsureApiRole` → `EnsureApiPermission` → `module:`.
- Points d'API : `/login` (2FA → 422 `two_factor`, limite `api-login`), `/logout`, `/me` (profil, rôle, permissions, modules souscrits, droits par champ), `/me/locale` ; `/admin/users`, `/admin/invitations`, `/admin/connected-users`, `/admin/activity-log`.
- Réponses traduites selon `Accept-Language` ; contrat Scramble à jour.

**Critère de fin** : un jeton émis pour A est refusé sur B ; version trop ancienne → 426 ; contrat à jour.

### W02.13 — Plateforme

- Instantané nocturne : indicateurs de connexions (sessions et jetons actifs par entreprise) ; widget du tableau de bord plateforme.
- Fiche entreprise : état de l'invitation du premier admin, nombre d'utilisateurs par statut.

**Critère de fin** : indicateurs visibles sur le tableau de bord plateforme, sans donnée nominative.

### W02.14 — Documentation et livraison

- `02-reference/` : accès, rôles, permissions, champs sensibles, API d'authentification.
- `05-recette/` : comptes de démonstration (admin plateforme, admin entreprise).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W02 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Invitation | Compte neuf, compte existant, jeton invalide, expiré, annulé, réutilisé ; expiration automatique ; renvoi ; invitation du premier admin par la plateforme |
| Rattachement | Toutes les transitions, transitions interdites, effet immédiat sur sessions et jetons, fin d'accès |
| Connexion | Mot de passe, passkey, 2FA, 2FA imposée, mot de passe expiré, entreprise d'un autre rattachement, abonnement suspendu, limites de débit |
| Mot de passe | Règles, politique la plus stricte, historique, expiration |
| Droits | Rôle par défaut, délégation, exclusion, module manquant prioritaire, au web et à l'API |
| Champs sensibles | Matrice complète de `FieldAccess` ; l'ADM n'a jamais accès |
| Connectés | Déconnexion forcée d'une session web et d'un jeton mobile |
| Journal | Filtres, export, valeurs avant / après, immuabilité |
| API | Jeton lié à l'entreprise, 426, `/me` complet, contrat à jour |

## 7. Critères de sortie

- Tests ciblés W02 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §3.1 (compte sans dossier), §3.2, §5.19, et du début de §5.2 (configuration).
- Documentation et livraison de W02.14 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Invitations avec dossier (RH, PAIE, DIR, MGR, EMP), onglet Matricule, changement de rôle | W04.1 |
| Périmètre d'équipe (`TeamScope`), « employé concerné » dans `FieldAccess` | W04 |
| Journal des consultations sensibles | W04.2 |
| Connexion carte + PIN (`/card-login`) | W05 |
| Enregistrement des appareils push | W10 |
| Connexion dans l'app (écrans) | E01 |
