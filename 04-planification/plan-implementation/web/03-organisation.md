# W03 — Organisation, sites, bornes

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W02

## 1. Objet

Donner à l'entreprise son squelette : structure en arbre, référentiel des postes, sites, et bornes de site côté serveur (création, appairage sécurisé, signal de vie, suspension, révocation, renouvellement de clé). Poser aussi le **point de rendu unique des PDF** avec la charte neutre, utilisé pour la première fois par l'export de l'organigramme. À la fin de W03, l'admin a décrit son organisation, ses sites et ses bornes ; l'appairage est testé par un client simulé en attendant l'app Borne (B01).

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ORG-01 | Structure en arbre, code unique, responsable (le responsable, qui est un employé, est ajouté en W04.1) |
| F-ORG-02 | Sites, fuseau du site (site principal et sites de pointage de l'employé : W04.1 ; plannings applicables : W06.1) |
| F-ORG-03, 07 | Bornes : écran, appairage par QR à usage unique, état, signal de vie, suspension, révocation, renouvellement de clé |
| F-ORG-05 | Organigramme de la structure et export PDF (la hiérarchie des personnes s'y ajoute en W04.1) |
| F-ORG-06 (clés) | Clé HMAC propre à chaque borne, chiffrée par la DEK ; la réception des pointages hors ligne est en W06.2 |
| F-IDN-01, T-20 | `DocumentRenderer` et charte neutre |
| T-11b | Appairage par jeton de 10 min, clé non exportable, requêtes signées, révocation immédiate |

F-ORG-04 (hiérarchie, équipe directe et indirecte) est construit en W04.1, avec les employés.

À lire : PRD §7.3 ; TRD §12.1, §12.5, §15 (charte), §22 ; APPFLOW §3.5, §4.2, §5.2, §6.1, §6.2 (S-23) ; BACKEND SCHEMA §5.1 (`clocking_settings`), §5.2, §8 ; UX/UI §6.1, §8, §13.1.

## 3. Prérequis

- W02 livré.
- Paquets installés par le développeur à l'étape concernée : `endroid/qr-code` (W03.5) ; dompdf et ar-php sont installés depuis W01.11.

**Décisions à prendre avant de démarrer** :

| Sujet | Proposition |
|---|---|
| Écran des postes | Le référentiel `job_positions` n'a pas d'écran dans l'APPFLOW §6. Ajout d'un **écran séparé « Postes »** (`/job-positions`) dans le menu Administration, permission délégable `job_positions` (ADM et RH par défaut) ; APPFLOW mis à jour |
| Algorithmes de la borne | Signature des requêtes en **ECDSA P-256** ; réception de la clé HMAC chiffrée en **RSA-OAEP 2048 (SHA-256)** ; ces deux types de clés sont pris en charge par le Keystore Android depuis longtemps, contrairement à Ed25519. TRD §12.5 précisé |
| Version Android minimale des bornes | À fixer avec l'app Borne (B00) ; W03 n'en dépend pas |
| Renouvellement de la clé HMAC | La nouvelle clé est livrée à la borne dans la réponse à son signal de vie suivant, chiffrée avec sa clé publique ; l'ancienne reste acceptée pour les pointages **capturés** avant le renouvellement, pendant la fenêtre hors ligne |
| Alerte de borne silencieuse | Par e-mail à l'admin en W03 ; la notification in-app s'ajoute en W04.3 avec la cloche |

## 4. Rôles et statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Borne `kiosks.status` | `en_attente_appairage` → `active` ⇄ `suspendue` → `revoquee` | ADM crée, suspend, reprend, révoque ; la borne s'appaire ; SYS alerte si silencieuse |
| Jeton d'appairage | valide (10 min) → utilisé / expiré | ADM génère ; la borne consomme |

## 5. Étapes ordonnées

### W03.1 — Enums et compléments de spécification

- Enum `App\Enums\Tenant\KioskStatus` ; permissions `org_units`, `job_positions`, `sites`, `kiosks`, `org_chart` ajoutées à `Permission`.
- APPFLOW §6.1 (écran Postes), TRD §12.5 (algorithmes, renouvellement) mis à jour.

### W03.2 — Structure et postes

- Migrations d'entreprise : `org_units` (sans `head_employee_id`, ajouté en W04.1), `job_positions`.
- Models, factories ; arbre (`parent_id`), refus des cycles.
- `App\Services\Tenant\OrganizationService` : créer, déplacer dans l'arbre, renommer, supprimer (refusé s'il reste des sous-unités actives ; le contrôle « employés actifs » s'ajoute en W04.1), restaurer ; postes rattachés ou non à une unité ; unicité des codes avec restauration plutôt que recréation.
- S-11 `/org-units` : vue arbre et vue liste, corbeille.
- Écran **Postes** `/job-positions` : liste, création, rattachement facultatif à une unité, corbeille.

**Critère de fin** : arbre de 4 niveaux créé, déplacé, une branche supprimée puis restaurée ; un cycle refusé ; journal complet.

### W03.3 — Sites

- Migration d'entreprise `sites`.
- `App\Services\Tenant\SiteService` : créer, modifier, désactiver, réactiver ; fuseau du site (par défaut celui de l'entreprise).
- `CompanyTimezone` étendu au fuseau d'un site.
- S-12 `/sites` : liste, fiche (adresse, ville, fuseau, bornes du site), corbeille.

**Critère de fin** : un site dans un autre fuseau convertit correctement une heure ; un site désactivé n'est plus proposé.

### W03.4 — Rendu des documents et organigramme

- `DocumentRenderer` (créé en W01.11 pour les factures) étendu aux documents de l'entreprise : en-tête de l'entreprise (`company_profile`), pied avec référence et date, langue officielle, arabe par ar-php (UX/UI §13.1).
- `DocumentBrandingService::current()` renvoie la **charte neutre** ; les chartes versionnées s'ajoutent en W16. Les tables qui porteront un PDF auront `document_branding_version_id` nul = neutre (BACKEND SCHEMA §8).
- Polices des documents sous `storage/app/public/fonts/documents`.
- S-23 `/org-chart` : arbre de la structure (responsables et personnes ajoutés en W04.1), export PDF par `DocumentRenderer`.

**Critère de fin** : PDF de l'organigramme correct en fr et en ar (RTL), avec l'en-tête de l'entreprise.

### W03.5 — Bornes : création et appairage

- Migrations d'entreprise : `kiosks`, `kiosk_pairing_tokens` ; `clocking_settings` créée avec la seule colonne `kiosk_silence_alert_minutes` (les autres colonnes arrivent en W06.1).
- `App\Services\Tenant\KioskService` :
  - `create(name, site)` → `en_attente_appairage` ;
  - `issuePairingToken()` : jeton aléatoire stocké haché, valable 10 min, usage unique ; QR contenant l'URL de l'entreprise, l'identifiant de la borne et le jeton ;
  - `pair(token, publicSigningKey, publicEncryptionKey, deviceFingerprint)` : vérifie jeton (non expiré, non utilisé, borne en attente), enregistre les clés publiques, génère la clé HMAC (256 bits, chiffrée par la DEK), émet le jeton Sanctum `kiosk:{id}` (non lié à une personne), renvoie la clé HMAC chiffrée pour la borne, passe la borne `active`, consomme le jeton, journalise.
- Point d'API public `/api/v1/kiosk/pair` (limite `kiosk-pairing`).

**Critère de fin** : un client de test qui génère ses clés s'appaire, déchiffre sa clé HMAC et reçoit son jeton ; jeton expiré, réutilisé ou borne déjà active → refus.

### W03.6 — Bornes : requêtes signées et signal de vie

- Middleware `EnsureKiosk` (ability `kiosk:{id}`, borne `active`) et `VerifyKioskSignature` (signature ECDSA du corps et de l'horodatage, fenêtre de fraîcheur, refus d'un horodatage rejoué).
- Points d'API `/api/v1/kiosk/config` (entreprise, site, fuseau, pas du code, langue) et `/api/v1/kiosk/heartbeat` (version, batterie, pointages en attente, dérive d'horloge mesurée) ; `last_heartbeat_at` mis à jour.
- Tâche planifiée : borne `active` sans signal depuis `kiosk_silence_alert_minutes` → e-mail à l'admin (une alerte par période de silence).

**Critère de fin** : un jeton de borne volé, utilisé sans la clé privée, est refusé ; une requête rejouée est refusée ; une borne silencieuse déclenche une seule alerte.

### W03.7 — Bornes : cycle de vie et écran

- `KioskService` : `rename()`, `suspend()`, `resume()`, `revoke(reason)` (invalide jeton, clés publiques et clé HMAC ; les autres bornes ne sont pas touchées), `renewSecret()` (nouvelle clé livrée au signal de vie suivant), `reissuePairing()` pour une borne révoquée remplacée par un nouvel appareil (nouvelle borne).
- S-14 `/kiosks` : liste par site, état (badge), dernier signal, version, batterie, pointages en attente, dérive ; actions appairer (QR affiché avec compte à rebours), renommer, suspendre, reprendre, révoquer, renouveler la clé ; toutes journalisées.
- API d'administration `/api/v1/admin/kiosks` (liste, état, suspendre) pour l'onglet Bornes de l'app Entreprise.

**Critère de fin** : chaque transition et chaque transition interdite testées ; une borne suspendue ou révoquée reçoit 403 à sa requête suivante.

### W03.8 — Mise en place de l'entreprise

- Liste de démarrage de l'admin (W02.10) : structure, postes, sites, bornes.
- Barre latérale : entrées Structure, Postes, Sites, Bornes (Administration) et Organigramme (Collaborateurs).

### W03.9 — Documentation et livraison

- `02-reference/` : organisation, bornes (protocole d'appairage et de signature décrit pour l'équipe mobile), `DocumentRenderer`.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W03 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Structure | Arbre, déplacement, cycle refusé, suppression refusée avec sous-unités actives, restauration, unicité des codes |
| Sites | Fuseau du site, désactivation |
| Documents | Rendu PDF fr et ar, en-tête de l'entreprise, charte neutre |
| Appairage | Nominal ; jeton expiré, utilisé, inconnu ; borne non en attente ; limite de débit |
| Signature | Requête valide ; signature absente, fausse, horodatage périmé, rejoué ; jeton sans clé |
| Cycle de vie | Suspension, reprise, révocation, renouvellement de clé ; transitions interdites ; autres bornes non affectées |
| Signal de vie | Mise à jour de l'état ; alerte unique de borne silencieuse |
| Droits | ADM par défaut ; délégation et exclusion des permissions `org_units`, `job_positions`, `sites`, `kiosks`, `org_chart` ; autre entreprise |

## 7. Critères de sortie

- Tests ciblés W03 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.2 (structure, sites, bornes) et §3.5 avec le client d'appairage simulé.
- Documentation et livraison de W03.9 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Responsable d'une unité, hiérarchie des personnes, organigramme des personnes, sites de pointage de l'employé | W04.1 |
| Notification in-app de borne silencieuse | W04.3 |
| Réception des pointages de la borne, vérification du code temporel | W06.2 |
| Plannings applicables à un site | W06.1 |
| Appairage réel, mode kiosque, QR local | B01, B02 |
| Chartes versionnées | W16 |
