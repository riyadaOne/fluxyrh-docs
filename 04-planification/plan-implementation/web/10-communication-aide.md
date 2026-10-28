# W10 — Communication et centre d'aide

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09 · Clôt le socle

## 1. Objet

Terminer le socle avec ses fonctions transverses : **annonces ciblées** avec accusé de lecture, **notifications push** côté serveur (la cloche existe depuis W04.3), pages d'accueil par rôle avec les **tâches en attente**, **centre d'aide** trilingue (articles de RIYADA ONE et articles de l'entreprise). Les archives de données demandées par l'entreprise se font **hors système** (PRD F-PLT-06 mis à jour). À la fin de W10, le socle « FluxyRH Essentiel » est complet côté web et API.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-COM-01 (fin) | Push pour les événements clés ; tous les événements branchés |
| F-COM-03 | Annonces ciblées, publication, archivage, accusé de lecture |
| F-AID-01 | Articles par catégorie, trois langues, recherche, articles de l'entreprise |
| PRD §7.15 (socle) | Page d'accueil de chaque rôle avec ses tâches en attente |

À lire : PRD §7.14 à §7.16, §9 (NF-09) ; TRD §19, §25.3 ; APPFLOW §4, §5.18, §6.7 (S-70, S-90) ; BACKEND SCHEMA §4.1 (`push_devices`), §5.14, §5.15 (aide) ; UX/UI §6.10, §6.11.

## 3. Prérequis et décisions

W09 livré.

| Sujet | Proposition |
|---|---|
| Identifiants Firebase | Un projet Firebase par flavor (TRD §19) : le compte de service de chaque entreprise est déposé par l'admin plateforme sur la fiche « Application mobile » (W01.9), **chiffré par la clé maître**, jamais versionné ni affiché. Colonne à ajouter à `companies` (BACKEND SCHEMA mis à jour) |
| Push avant l'app | Le job d'envoi est testé avec un faux transport et l'appel FCM en mode `validate_only` ; l'envoi réel est recetté en E08 |
| Accusé de lecture d'une annonce | Par un bouton « J'ai lu » (web ou app), sans carte ; la carte reste réservée aux documents remis (F-NFC-06) |
| Articles de RIYADA ONE | Rédigés dans le code (fichiers par langue, versionnés) et synchronisés dans chaque entreprise par une commande (`is_platform` = 1, non modifiables par l'entreprise) ; l'entreprise ajoute ses propres articles |
| Recherche dans l'aide | Recherche simple sur titre et corps dans la langue de l'utilisateur ; recherche plein texte MySQL si le volume le justifie |
| Archives des données | **Hors système** : une demande d'archive (mensuelle ou à la résiliation) est traitée par RIYADA ONE hors de FluxyRH, à partir des sauvegardes (MEP) ; la table `company_archive_requests` et l'écran S-17 sont retirés (BACKEND SCHEMA, APPFLOW §5.20 et §6.1 mis à jour) |

## 4. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Annonce `announcements.status` | `brouillon` → `publiee` → `archivee` | RH, DIR |
| Article d'aide | `brouillon` → `publie` | ADM, RH (articles de l'entreprise) |

## 5. Étapes ordonnées

### W10.1 — Enums et permissions

- `AnnouncementType`, `AnnouncementStatus`, `AnnouncementTarget`, `HelpArticleStatus` ; permissions `announcements`, `help_articles`.

### W10.2 — Annonces

- Migrations `announcements`, `announcement_targets`, `announcement_reads`.
- `App\Services\Tenant\AnnouncementService` : brouillon, ciblage (tous, structure, site, rôle, personnes ; plusieurs cibles cumulées), publication (notification in-app et push aux destinataires), archivage, accusé de lecture, taux de lecture.
- S-70 `/announcements` (RH, DIR) : rédaction (texte riche assaini, W08.1), cibles, aperçu des destinataires, statistiques de lecture ; page `/announcements` de l'espace personnel avec « J'ai lu ».

### W10.3 — Push

- Migration générale `push_devices` ; colonne du compte de service Firebase sur `companies` (§3) et champ de dépôt sur la fiche « Application mobile ».
- API `/api/v1/push-devices` (enregistrement lié au jeton Sanctum, retrait à la déconnexion).
- Job `SendPushNotification` après commit : FCM HTTP v1 sans SDK, jeton d'accès OAuth du compte de service, langue officielle, **aucune valeur sensible** ; jetons invalides retirés.
- `NotificationCenterService` : push ajouté au canal in-app pour les événements clés (donnée à vérifier, demande à approuver, contrat à signer, bulletin publié, décisions, annonces, relances).

**Critère de fin** : chaque événement clé produit une notification in-app et un envoi push (faux transport) sans valeur sensible ; l'appel FCM `validate_only` réussit avec un compte de service de test.

### W10.4 — Accueils par rôle

- `/dashboard` de chaque rôle (socle, sans widgets) : **tâches en attente** regroupées (vérifications, approbations, congés, heures sup, contrats, périodes de paie, cartes à remettre…) avec liens, et indicateurs simples déjà construits (W06.4, W08.4) ; accueil `/me` de l'employé (complétion, soldes, à signer, annonces non lues).
- Les tableaux de bord à widgets restent au module Pilotage (W13).

### W10.5 — Centre d'aide

- Migrations `help_categories`, `help_category_translations`, `help_articles`, `help_article_translations`.
- Articles de RIYADA ONE (§3) : un article par parcours livré (W02 à W09), dans les trois langues ; commande de synchronisation, ajoutée à `deploy.sh` en MEP.
- S-90 `/help` : lecture pour tous (catégories, recherche, article), édition des articles de l'entreprise (ADM, RH) ; entrée « Aide » du menu utilisateur ; lien d'aide contextuel depuis les écrans principaux.

### W10.6 — API

- `/api/v1/employee/announcements` (liste, lu), `/hr/announcements`, `/help` (catégories, articles, recherche), `/me/dashboard` (tâches en attente pour l'accueil mobile).
- Contrat Scramble à jour.

### W10.7 — Documentation et livraison

- `02-reference/` : annonces, push, accueils, centre d'aide.
- `05-recette/` : **recette complète du socle** sur le jeu de démonstration (APPFLOW §3 à §5.11, §5.18).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W10 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Annonces | Chaque type de cible, cibles cumulées, publication, archivage, accusé, taux de lecture, destinataire hors cible |
| Push | Enregistrement et retrait des appareils, faux transport, jeton invalide retiré, aucune valeur sensible, compte de service jamais exposé |
| Accueils | Tâches en attente par rôle, périmètre (manager), aucune donnée sensible pour un rôle non autorisé |
| Aide | Trois langues, recherche, articles plateforme non modifiables, synchronisation idempotente |
| Droits | `announcements`, `help_articles` ; autre entreprise ; API |

## 7. Critères de sortie

- Tests ciblés W10 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette complète du socle consignée dans `05-recette/`.
- Documentation et livraison de W10.7 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Tableaux de bord à widgets, rapports | W13 |
| Réception des push, annonces et aide dans l'app | E08 |
| Sauvegardes techniques quotidiennes et mensuelles | MEP |
