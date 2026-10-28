# W05 — Cartes NFC

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W04

## 1. Objet

Construire tout le côté serveur de la carte NFC employé : cycle de la carte de sa préparation à sa désactivation, file d'encodage de la plateforme et API de la future Console, badge public vérifiable, accès rapide au dossier, activation et PIN, connexion carte + PIN, enregistrement des téléphones, **signature d'actions**, design neutre de la carte et cartes de test. À la fin de W05, une carte de test écrite avec une application NFC générique ouvre le badge public ; tout le reste est vérifié par des tests d'API en attendant les apps (E01, E03, B03, C01).

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-NFC-01 | Une carte par employé et par entreprise, identifiant opaque |
| F-NFC-02 | Cycle `Préparée` → `Encodée` → `Livrée` → `Remise` → `Active` ; `Désactivée` |
| F-NFC-03 | Badge public `En poste` / `Plus en poste` / `Inconnue` |
| F-NFC-04 | Accès rapide au dossier filtré par les droits de celui qui scanne (API) |
| F-NFC-05 | Connexion carte + PIN, option de l'entreprise, 5 essais, révocation |
| F-NFC-06 | `ActionSignatureService` ; premier usage : accusé de réception d'un document déposé par le RH |
| F-NFC-07 (socle) | Design neutre, aperçu, export PDF pour l'impression |
| F-PLT-05 | File des cartes à encoder (web plateforme et API Console), livraison |

À lire : PRD §7.5, §8.4 ; TRD §7.5, §12.2, §13, §17.1 ; APPFLOW §3.3, §3.4, §4.1, §5.5, §6.1 (S-16, S-18), §6.8 (S-69) ; BACKEND SCHEMA §5.1 (`card_design_settings`), §5.5, §9 (point 7) ; UX/UI §13.3, §14.

## 3. Prérequis et décisions

W04 livré.

| Sujet | Proposition |
|---|---|
| Recherche d'une carte par son identifiant | `nfc_cards.encrypted_identifier` est unique et sert à retrouver la carte (badge, pointage, signature) : une colonne chiffrée ne peut pas être cherchée (TRD §9.3). Remplacement par **`identifier_hash`** (HMAC-SHA256 de l'identifiant avec une clé dérivée de la DEK de l'entreprise, unique, cherchable) ; l'identifiant en clair n'est stocké nulle part, il n'existe que sur la puce et dans l'URI. BACKEND SCHEMA §5.5 mis à jour |
| PIN de la carte | Le schéma ne prévoit un PIN que par appareil de connexion (`card_login_devices.pin_hash`), alors que l'activation sur la borne demande aussi un PIN (APPFLOW §5.5). Proposition : **un seul PIN par carte**, `nfc_cards.pin_hash`, choisi à l'activation, utilisé pour la connexion carte + PIN et les actions sur la borne ; `card_login_devices` garde la clé d'appareil et le compteur d'essais. BACKEND SCHEMA mis à jour |
| Condition de préparation | Une carte n'est préparée que pour un employé `actif` dont l'**identité est vérifiée** (photo, nom imprimés sur la carte) et qui n'a pas d'autre carte en cours |
| Badge d'une carte désactivée | Affiche `Inconnue` (une carte perdue ou volée ne doit rien confirmer) ; `Plus en poste` pour une carte d'un employé sorti |
| Paiement de la carte | Hors système (PRD §8.4) : aucune donnée de paiement |
| Signature sans carte | Les documents remis à une personne (contrats, bulletins, documents, courriers, formulaires) peuvent être signés ou accusés **avec ou sans carte** : sans carte, sur le web par la confirmation du mot de passe de la personne, dans l'app par son code ou sa biométrie ; avec la carte, dans l'app. Le **pointage exige toujours la carte**. `action_signatures.nfc_card_id` devient facultatif et une colonne `method` (`carte`, `mot_de_passe`, `appareil`) est ajoutée ; PRD F-NFC-06 mis à jour |
| Option « connexion par carte » | Choisie par **chaque utilisateur** pour ses appareils (S-69 et Profil de l'app), pas par l'entreprise : la colonne `companies.card_login_enabled` est retirée du BACKEND SCHEMA ; PRD F-NFC-05 mis à jour |

## 4. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Carte `nfc_cards.status` | `preparee` → `encodee` → `livree` → `remise` → `active` → `desactivee` | ADM prépare ; PLT encode (Console) et livre (web) ; RH remet ; EMP active (téléphone ou borne) ; EMP (perte), RH ou ADM désactive ; SYS à la sortie |
| Appareil de connexion | enregistré → révoqué (5 échecs, désactivation de la carte, retrait par l'employé) | EMP ; SYS |
| Téléphone de pointage `employee_devices` | enregistré → révoqué | EMP (confirmation par la carte) ; EMP, RH |

Une carte qui n'est pas `active` ne permet ni pointage, ni signature, ni connexion.

## 5. Étapes ordonnées

### W05.1 — Enums et compléments de spécification

- `NfcCardStatus`, `SignatureAction`, `ClockingChannel` ; permissions `card_preparation`, `card_handover`.
- BACKEND SCHEMA §4.2 (retrait de `card_login_enabled`), §5.5 (`identifier_hash`, `pin_hash`) et APPFLOW §5.5 (condition de préparation, badge d'une carte désactivée) mis à jour.

### W05.2 — Cartes et cycle de vie

- Migrations d'entreprise : `nfc_cards` (avec `identifier_hash` et `pin_hash`), `card_design_settings`.
- `App\Services\Tenant\NfcCardService` : `prepare()` (§3), `markEncoded()`, `markDelivered()`, `handOver()`, `activate(card, pin)`, `deactivate(reason)`, préparation d'une nouvelle carte après désactivation ; une seule carte `active` et une seule carte en cours par employé ; transitions en transaction, journalisées.
- Désactivation par le système à la sortie de l'employé (branchée sur W04.1.7) ; révocation des appareils de connexion à toute désactivation.

**Critère de fin** : chaque transition et chaque transition interdite testées ; une seconde carte active est impossible.

### W05.3 — File d'encodage et livraison (plateforme)

- Écran plateforme `/nfc-cards` : file des cartes `preparee` de toutes les entreprises actives (parcours des bases, sans jointure), cartes `encodee` à livrer ; action « Livrer » (par lot et par entreprise).
- API `/api/v1/platform/nfc-cards` : file, **réservation** d'une carte (génération de l'identifiant opaque, 128 bits aléatoires, renvoyé une seule fois à la Console pour l'écriture), confirmation après relecture (`encodee`, `encoded_by`), verrouillage (`locked_at`), annulation d'une réservation non confirmée.

**Critère de fin** : un client de test réserve, confirme et verrouille une carte ; l'identifiant n'est jamais renvoyé deux fois ni stocké en clair.

### W05.4 — Écrans de l'entreprise

- S-16 `/nfc-cards` (ADM) : préparation unitaire et groupée, suivi par statut, désactivation, corbeille des préparations annulées.
- S-18 `/nfc-cards/handover` (RH) : cartes livrées à remettre, remise (confirmée par le RH), désactivation.
- S-69 `/me/card` : « Ma carte » (rendu identique à la carte imprimée), statut, déclaration de perte (désactivation), appareils de connexion et téléphones de pointage enregistrés, retrait d'un appareil.
- Onglet **Carte** de la fiche employé S-21 ; onglet **Cartes** de la Configuration (design, photo).
- Liste de démarrage de l'admin : préparation des premières cartes.

### W05.5 — Badge public et accès rapide

- Route publique `/badge/{identifiant}` (layout `public`) : logo et nom de l'entreprise, photo, nom, poste (valeurs vérifiées), badge `En poste` / `Plus en poste` / `Inconnue`, date et heure ; `noindex` ; limite `badge-verification` (20/min) ; chaque consultation journalisée sans donnée personnelle du visiteur au-delà de l'IP (UX/UI §14).
- API `/api/v1/{espace}/badge-link/{identifiant}` : RH, MGR (son équipe), DIR, PAIE reçoivent le dossier filtré par `PermissionService` et `FieldAccess` ; ADM reçoit la carte dans la gestion des cartes ; EMP reçoit « Ma carte » (APPFLOW §3.4).

**Critère de fin** : une carte de test approchée d'un téléphone sans l'app ouvre le badge correct ; un manager qui scanne une carte hors de son équipe ne reçoit aucun dossier.

### W05.6 — Activation, PIN et connexion par carte

- Activation par l'employé **connecté** sur son téléphone (lecture de sa carte + choix du PIN) : API `/employee/card/activate` ; activation sur la borne (carte + PIN) préparée pour B03 : API `/kiosk/card/activate`, signée par la borne.
- Changement de PIN (ancien PIN + carte).
- Migration d'entreprise `card_login_devices` ; mise en place depuis l'app (carte active + PIN + clé d'appareil) ; API publique `/card-login` (limite `card-login`) : identifiant de carte + PIN + clé d'appareil → jeton Sanctum de l'entreprise ; 5 échecs → appareil révoqué ; l'utilisateur active ou retire lui-même la connexion par carte de chacun de ses appareils (S-69).

**Critère de fin** : connexion carte + PIN réussie ; 5 échecs révoquent l'appareil ; une carte désactivée coupe immédiatement ses jetons.

### W05.7 — Téléphones de pointage

- Migration d'entreprise `employee_devices`.
- Enregistrement d'un téléphone pour le pointage personnel, confirmé par la lecture de la carte active (APPFLOW §3.3) : API `/employee/devices` ; retrait par l'employé ou le RH ; journalisé. Utilisé par le pointage en W06.2.

### W05.8 — Signature d'actions

- Migration d'entreprise `action_signatures` (ni modifiable ni supprimable).
- `App\Services\Tenant\ActionSignatureService::sign(action, subject, method, proof, documentHash)` : avec la carte, carte `active` appartenant au signataire et appareil enregistré ou borne active ; sans carte (§3), mot de passe confirmé (web) ou code ou biométrie de l'appareil enregistré (app) ; moyen enregistré, horodatage serveur, empreinte SHA-256 du document, journal. Le pointage n'accepte que la carte.
- Premier usage : **accusé de réception** d'un document déposé par le RH (W04.3.4) : API `/employee/documents/{id}/acknowledge`, `employee_documents.acknowledged_signature_id`. Les autres actions (`pointage`, `contrat`, `bulletin`…) sont branchées par W06.2, W08.3, W09.6, W12.3.

**Critère de fin** : une signature avec une carte d'un autre employé, une carte inactive ou un appareil non enregistré est refusée ; une signature ne peut être ni modifiée ni supprimée.

### W05.9 — Design neutre et impression

- `config/cards.php` avec le design `0` (neutre) ; rendu HTML serveur de la carte (recto, verso) utilisé par « Ma carte », l'aperçu de la Configuration et l'export.
- Export PDF des cartes à imprimer (par lot, traits de coupe) par `DocumentRenderer`.
- Test des débordements : nom et poste longs (40 caractères et plus), réduction ou retour à la ligne, jamais de texte coupé (UX/UI §13.3).

### W05.10 — Cartes de test

- Commande de développement `fluxyrh:dev-cards {slug} {nombre}` : prépare, encode et livre des cartes pour des employés de démonstration, affiche les URI à écrire sur des cartes NTAG avec une application NFC générique ; **refusée en production**.

**Critère de fin** : procédure documentée dans `05-recette/` ; une carte écrite à la main ouvre le badge.

### W05.11 — Documentation et livraison

- `02-reference/` : cycle de la carte, identifiant et empreinte, PIN, connexion par carte, signatures (protocole décrit pour l'équipe mobile).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W05 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Cycle | Toutes les transitions, transitions interdites, une seule carte active ou en cours, désactivation à la sortie |
| Préparation | Identité non vérifiée, employé sorti, carte déjà en cours : refus |
| Encodage | Réservation, confirmation, verrouillage, annulation ; identifiant jamais renvoyé deux fois |
| Badge | Trois états, limite de débit, `noindex`, journal, carte inconnue d'une autre entreprise |
| Accès rapide | Filtrage par rôle, périmètre d'équipe, `FieldAccess` (aucune donnée bancaire pour le RH) |
| PIN et connexion | Activation, changement de PIN, 5 échecs, connexion par carte activée puis retirée par l'utilisateur, révocation à la désactivation |
| Signature | Carte d'autrui, carte inactive, appareil inconnu, borne révoquée, mot de passe erroné, pointage sans carte refusé ; moyen enregistré ; immuabilité |
| Design | Débordements, export PDF |
| Droits | `card_preparation`, `card_handover` ; autre entreprise ; API plateforme réservée à la plateforme |

## 7. Critères de sortie

- Tests ciblés W05 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.5 côté web (préparation, livraison, remise, désactivation) et du badge public avec une carte de test.
- Documentation et livraison de W05.11 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Signature du pointage | W06.2 |
| Signature des contrats, accusé des bulletins, des courriers | W08.3, W09.6, W12.3 |
| 20 designs de carte aux couleurs de la charte | W16 |
| `assetlinks.json` (ouverture de l'app par la carte) | E10 |
| Activation, connexion par carte, scan dans l'app | E01, E03 |
| Activation et secours sur la borne | B03 |
| Encodage réel des cartes | C01 |
