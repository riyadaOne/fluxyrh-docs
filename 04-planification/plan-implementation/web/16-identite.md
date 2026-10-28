# W16 — Module Identité (chartes documentaires, designs de carte)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W15 · Option hors pack `identite` · Clôt l'application web

## 1. Objet

Habiller les **documents générés** (PDF, e-mails, carte employé) aux couleurs de l'entreprise, sans toucher à l'interface : **12 modèles** de charte, **palette fermée** de couleurs testées, en-tête et pied de page, **cachet**, **signature** de la direction (apposée seulement sur ce qu'elle a signé dans le système), **filigrane**, **20 designs de carte**, et **versions** de charte : un document garde à jamais la charte de sa génération. Sans le module, tout reste en charte neutre (W03.4, W05.9). À la fin de W16, l'application web est complète.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-IDN-02 | 12 modèles, aperçu sur des documents types avant activation |
| F-IDN-03 | Couleur de la palette, en-tête et pied, cachet, signature, filigrane |
| F-IDN-04, F-NFC-07 | 20 designs de carte aux couleurs de la charte |
| F-IDN-05 | Signature déposée par le directeur, apposée seulement sur les documents qu'il a signés dans le système ; cachet sur les documents officiels |
| F-IDN-06 | Versions de charte, document figé avec sa charte, retour au neutre à l'arrêt du module, journal |
| T-20 | `DocumentRenderer` et version de charte enregistrée sur chaque PDF |

À lire : PRD §7.18 ; TRD §15 (charte) ; APPFLOW §5.21, §6.1 (S-08, S-19) ; BACKEND SCHEMA §5.1 (`card_design_settings`), §5.16, §7 (`BrandingTemplate`, `BrandingColor`, `WatermarkKind`, `BrandingVersionStatus`), §8 ; UX/UI §13.3, §13.5.

## 3. Prérequis et décisions

W15 livré.

| Sujet | Proposition |
|---|---|
| Maquettes | **Prérequis bloquant** : Claude propose les maquettes des 12 modèles de charte et des 20 designs de carte ; elles sont validées avant de démarrer W16 (UX/UI §16, TRD §27) |
| Colonne de charte sur les PDF | Les tables qui portent un PDF (contrats, bulletins, destinataires de courriers, formulaires, déclarations, feuilles de temps exportées…) reçoivent ici `document_branding_version_id` (nul = neutre, valeur de tous les documents antérieurs), conformément au développement vertical |
| Documents portant la signature graphique | Tout document **signé par la direction dans le système** : contrats et avenants (W08.3), courriers et formulaires dont le modèle exige la signature de la direction (W12.3), et tout autre document qui en a besoin |
| Cachet | Apposé sur les contrats, avenants, attestations et courriers |
| Tests visuels | Rendu automatique de chaque modèle × chaque couleur × les 5 documents de l'aperçu × fr et ar, avec raison sociale longue et filigrane : aucune erreur, nombre de pages attendu ; plus une **planche de contrôle** PDF générée pour une relecture humaine (UX/UI §13.5) |
| Signature d'un directeur qui part | Révoquée automatiquement à sa sortie ou à son changement de rôle (APPFLOW §5.21) |

## 4. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Version de charte `document_branding_versions.status` | `brouillon` → `active` (l'ancienne `active` passe `archivee`) | ADM |
| Signature `branding_signatures` | déposée → révoquée (par le directeur, ou par le système à sa sortie) | DIR ; SYS |

## 5. Étapes ordonnées

### W16.1 — Enums, permissions, module

- `BrandingTemplate`, `BrandingColor` (palette de `config/branding.php`), `WatermarkKind`, `BrandingVersionStatus` ; permission `document_branding` (S-19 socle en lecture, réglages avec le module).

### W16.2 — Données

- Migrations `document_branding_versions`, `branding_signatures` ; `document_branding_version_id` ajouté aux tables portant un PDF (§3).
- Fichiers du cachet et des signatures sur le disque privé, chiffrés par la DEK, PNG ou SVG assaini, taille limitée, 300 dpi minimum.

### W16.3 — Rendu

- 12 gabarits Blade versionnés `resources/views/documents/brands/{template}` (en-tête, pied, titres, tableaux, bloc des signataires), trois langues dont l'arabe ; couleurs injectées en valeurs hexadécimales (dompdf ne lit pas les variables CSS) ; filigrane sous le texte.
- `DocumentBrandingService::current()` : version active si le module est souscrit, sinon neutre (BACKEND SCHEMA §8) ; `DocumentRenderer` enregistre la version utilisée sur chaque PDF ; un PDF n'est jamais régénéré avec une autre charte.
- Cachet selon le type de document ; signature graphique d'un directeur seulement si le document porte une `action_signature` de cette personne (§3).
- Layout des e-mails surchargé par la charte (logo, bouton et filet en couleur, pied), texte brut toujours joint.

### W16.4 — Écrans

- S-19 `/document-branding` (ADM) : sans le module, charte neutre en lecture seule et présentation du module ; avec le module, réglages à gauche, aperçu à droite (Bulletin · Contrat · Attestation · E-mail · Carte, documents fictifs non enregistrés), activation confirmée, historique des versions.
- S-08 `/settings/signature` (DIR, propriétaire seulement) : dépôt avec aperçu, remplacement, retrait.

### W16.5 — Designs de carte

- 20 designs recto / verso dans `config/cards.php`, aux couleurs de la charte active ; choix dans S-19 (onglet Carte) avec aperçu en direct ; `card_design_settings.structure_index` de 1 à 20 ; design neutre si le module est coupé.
- Tests de débordement de W05.9 étendus aux 20 designs.

### W16.6 — Tests visuels

- Rendu automatique de toutes les combinaisons (§3) et planche de contrôle ; relecture humaine consignée dans `05-recette/`.

### W16.7 — Documentation et livraison

- `02-reference/` : chartes, versions, signatures, designs de carte ; article d'aide.
- `05-recette/` : **recette complète de l'application web** (socle et modules) avant le passage au mobile.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W16 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Versions | Activation (ancienne archivée), version active non modifiable, document figé avec sa version, retour au neutre à l'arrêt du module, journal |
| Rendu | Toutes les combinaisons sans erreur ; couleur hors palette refusée ; filigrane ; e-mails |
| Cachet | Présent sur les bons documents seulement |
| Signature | Déposée par le directeur seul ; apposée seulement avec sa signature dans le système ; révoquée à sa sortie ; fichier chiffré |
| Carte | 20 designs, débordements, design neutre sans le module |
| Droits | `document_branding` ; S-08 propriétaire seulement ; autre entreprise |

## 7. Critères de sortie

- Tests ciblés W16 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Planche de contrôle relue ; recette APPFLOW §5.21.
- **Recette complète de l'application web** consignée.
- Documentation et livraison de W16.7 faites ; W16 complet dans la ROADMAP : l'application web est terminée, la phase E00 peut démarrer.

## 8. Reporté

| Élément | Module |
|---|---|
| « Ma carte » dans l'app (WebView du rendu serveur) | E03 |
