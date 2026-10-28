# W04.2 — Dossier employé · Employé : complétion

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W04.1 · Suite : W04.3 (vérification)

## 1. Objet

Permettre à l'employé, **propriétaire** de ses données (P1, P2), de compléter puis de tenir à jour son dossier : identité, coordonnées, famille, contacts d'urgence, diplômes, coordonnées bancaires et pièces. Chaque soumission crée une **version** `À vérifier` d'un bloc, avec ses justificatifs ; la dernière version vérifiée reste en vigueur (P3). C'est aussi le module où apparaît la **première donnée sensible** (banque) : chiffrement, `FieldAccess`, journal des consultations et tests de non-fuite sont appliqués pour de bon. À la fin de W04.2, les dossiers sont remplis et attendent leur vérification (W04.3).

## 2. Ce que l'employé reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Un dossier `Actif` avec son affectation (W04.1) ; la liste de ses pièces obligatoires | Versions `À vérifier` de chaque bloc ; justificatifs ; pièces déposées | **RH** (W04.3) : identité, coordonnées, famille, contacts, diplômes, pièces ; **PAIE** (W04.3) : banque ; **DIR** (W04.3) : données d'un RH, banque d'un PAIE |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-EMP-03 (saisie) | Complétion, nouvelle version à chaque modification, valeur vérifiée conservée |
| F-EMP-05 (dépôt) | Dépôt des pièces par l'employé, remplacement, dates de délivrance et d'expiration |
| F-ADM-04, NF-02 | Champs bancaires chiffrés, lus par `FieldAccess`, tests de non-fuite |
| T-09, T-10 | Chiffrement des champs sensibles ; données vérifiables versionnées |

À lire : PRD §6 (P1 à P3, P6), §7.4 ; TRD §9, §10 ; APPFLOW §3.1 (fin), §4.7, §5.3, §5.4 ; BACKEND SCHEMA §5.4, §5.9 (`banks`), §8, §9 (points 1, 4) ; UX/UI §6.3, §6.5.

## 4. Prérequis et décisions

W04.1 livré. Paquet installé par le développeur : `intl-tel-input` (W04.2.3).

| Sujet | Proposition |
|---|---|
| Identifiants de l'employé | Les numéros propres à un pays (sécurité sociale, fiscal…) ne sont plus des colonnes de l'identité : l'entreprise définit la liste des **types d'identifiant** (libellé, obligatoire, affiché sur le bulletin ; onglet Dossier de S-15), et l'employé les saisit comme un bloc multiple vérifié par le RH ; aucun type livré (décision 0002) ; tables `employee_identifier_types`, `employee_identifiers`, `employee_identifier_versions` |
| Valeurs de l'identité | `Civility` (`m`, `mme`) et `Gender` (`masculin`, `feminin`) sont des enums. La **situation matrimoniale** et le **type de pièce d'identité** sont des **listes paramétrées par l'entreprise** (tables `marital_statuses`, `national_id_types` : code, libellé, actif), créées au provisionnement avec des valeurs de départ (célibataire, marié, marié polygame, divorcé, veuf ; CNI, passeport, carte de séjour, autre) libellées dans la langue officielle ; l'entreprise les modifie et en ajoute (onglet Dossier de S-15). Les colonnes deviennent `marital_status_id`, `national_id_type_id`. Nationalité et pays en ISO 3166-1 alpha-2 |
| Justificatif obligatoire | **Paramétrable par l'entreprise**, bloc par bloc (identité, coordonnées, membre de la famille, membre à charge, contact d'urgence, diplôme, banque), dans un onglet **Dossier** de S-15 (RH) ; table `verifiable_block_settings` (`block`, `proof_required`) ajoutée au BACKEND SCHEMA ; tant que rien n'est réglé, aucun justificatif n'est exigé |
| Justificatif bancaire | Un RIB est une donnée bancaire : le RH ne doit pas le voir. Ajout à `document_types` d'une colonne `sensitive_category` (nulle ou `bancaire`) ; type système `justificatif_bancaire` créé au provisionnement ; tout document de ce type est lu par `FieldAccess`. BACKEND SCHEMA §5.4 mis à jour |
| Modification pendant une vérification | Un bloc n'a qu'**une** version `À vérifier` à la fois : tant qu'elle n'est pas traitée, l'employé la corrige en place (journalisé) au lieu d'en créer une autre |
| Référentiel des banques | La table `banks` (BACKEND SCHEMA §5.9) est créée ici, car l'employé choisit sa banque. **Aucune liste livrée** (décision 0002) : le PAIE saisit les banques de l'entreprise dans S-58 « Banques », ouvert dès W04.2 |
| Journal des consultations sensibles | Une consultation des coordonnées bancaires par une autre personne que l'employé lui-même est journalisée (`sensitive_data_views`) |
| Fichiers | Disque privé, dossier par entreprise, PDF / JPEG / PNG, 10 Mo au plus, empreinte SHA-256 ; téléchargement seulement par une route autorisée |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Version d'un bloc ⟨V⟩ | (création) `a_verifier` ; correction en place tant qu'elle est `a_verifier` | EMP |
| Pièce `employee_documents` | (dépôt) `a_verifier` (si le type est vérifiable) ; remplacement par un nouveau dépôt | EMP |

La vérification (`verifiee`, `rejetee`) est construite en W04.3.

## 6. Étapes ordonnées

### W04.2.1 — Enums et compléments de spécification

- `VerificationStatus`, `FamilyRelationship`, `QualificationKind`, `PaymentChannel`, `Civility`, `Gender`.
- Migrations `marital_statuses`, `national_id_types` ; valeurs de départ créées au provisionnement dans la langue officielle ; listes gérées dans l'onglet Dossier de S-15.
- BACKEND SCHEMA §5.4 et §7 mis à jour (enums, `sensitive_category`, `verifiable_block_settings`).
- `SensitiveField` : champs bancaires (`holder_name`, `account_number`, `bank_code`, `branch_code`, `rib_key`, `iban`, `mobile_money_number`) dans la catégorie `bancaire`.

### W04.2.2 — Socle des données vérifiables

- Trait de migration et trait de model ⟨V⟩ (`status`, `submitted_by`, `submitted_at`, `verified_by`, `verified_at`, `rejection_reason`, `previous_version_id`) ; index (`employee_id`, `status`).
- `App\Services\Tenant\VerifiableDataService::submit()` (propriétaire uniquement, une version en attente par bloc, correction en place), lecture de la **valeur en vigueur** et de la **modification en attente** d'un bloc. `verify()` et `reject()` arrivent en W04.3.
- Migration `verification_proofs` ; `EmployeeDocumentService` : dépôt, empreinte, remplacement, téléchargement autorisé.
- Migration `employee_documents` ; `sensitive_category` ajoutée à `document_types` ; type système `justificatif_bancaire`.
- Migration `verifiable_block_settings` et onglet **Dossier** de S-15 (RH) : justificatif exigé ou non par bloc (§4) ; `submit()` refuse une version sans justificatif quand il est exigé.

**Critère de fin** : soumettre deux fois un bloc en attente ne crée qu'une version ; un tiers ne peut pas soumettre à la place du propriétaire ; un fichier n'est téléchargeable que par une personne autorisée.

### W04.2.3 — Blocs uniques : identité et coordonnées

- Migrations `employee_identity_versions`, `employee_contact_versions` ; pointeurs `current_identity_version_id`, `current_contact_version_id` ajoutés à `employees` (sans clé SQL, BACKEND SCHEMA §9 point 4).
- Formulaires : identité (photo recadrée, pièce d'identité en justificatif), coordonnées (téléphone international).

### W04.2.4 — Blocs multiples : famille, contacts d'urgence, diplômes, identifiants

- Migrations des entités et de leurs versions (BACKEND SCHEMA §5.4).
- Ajout, modification (nouvelle version), retrait d'une entité (version de retrait soumise à vérification, la valeur vérifiée restant en vigueur jusque-là).
- Identifiants de l'employé : migrations `employee_identifier_types`, `employee_identifiers`, `employee_identifier_versions` ; types gérés dans l'onglet Dossier de S-15 ; étape de l'assistant ; un identifiant obligatoire manquant compte dans la complétude (W04.3).

### W04.2.5 — Banque

- Migrations `banks`, `employee_bank_accounts`, `employee_bank_account_versions` (colonnes `enc` avec le cast `EncryptedWithCompanyKey`).
- S-58 `/banks` (PAIE, permission `bank_settings`) : liste, ajout, désactivation ; liste de démarrage du PAIE : saisir les banques de l'entreprise.
- Saisie par l'employé : moyen (`virement`, `mobile_money`…), banque, titulaire, numéros ; un seul compte principal ; justificatif de type `justificatif_bancaire`.
- `FieldAccess` appliqué partout ; migration `sensitive_data_views` et journalisation des consultations (§4).
- S-85 `/sensitive-views` (DIR, non délégable) : journal des consultations sensibles (qui, quoi, quand), filtres par personne consultée, par auteur et par période (TRD §9.4).
- Rotation d'une DEK : job de rechiffrement des colonnes chiffrées (reporté de W00.7), testé sur les comptes bancaires.

**Critère de fin** : aucune valeur bancaire lisible en base ; l'ADM et le RH ne voient ni l'onglet Banque ni le RIB, au web, à l'API, dans le journal d'audit ; chaque consultation par le PAIE est journalisée.

### W04.2.6 — Pièces

- S-62 `/me/documents` : pièces attendues (obligatoires pour son type d'employé, puis facultatives), dépôt, remplacement, dates de délivrance et d'expiration (si le type en a), historique des versions.
- Les pièces déposées par le RH (`uploaded_by` = `rh`) et l'accusé de réception arrivent en W04.3 et W05.

### W04.2.7 — Assistant et dossier personnel

- S-60 `/me` : accueil personnel et **assistant de complétion** (UX/UI §6.5) : identité → coordonnées → famille → contacts d'urgence → diplômes → banque → pièces ; étapes sautables, « Enregistrer et continuer plus tard », récapitulatif des pièces obligatoires non déposées et de ce que leur absence bloquera (congés, attestations).
- Bandeau de complétion sur l'accueil tant que l'assistant n'est pas terminé ; redirection vers l'assistant après l'acceptation de l'invitation.
- S-61 `/me/file` : dossier par blocs, valeur en vigueur et modification en attente côte à côte, badge de statut, bouton « Modifier » (UX/UI §6.3).
- Layout `me` ; groupe « Mon espace » de la barre latérale pour les rôles qui ont un dossier.

**Critère de fin** : APPFLOW §5.3 (partie employé) et §5.4 recettés en fr, en, ar.

### W04.2.8 — Fiche employé côté RH (lecture)

- Onglets Identité, Coordonnées, Famille, Diplômes, Banque (selon `FieldAccess`), Documents de la fiche S-21 : valeur en vigueur, modification en attente, historique des versions. Aucune saisie par le RH (P1).

### W04.2.9 — API

- `/api/v1/employee/file` (blocs, valeur en vigueur, version en attente, historique), soumission et correction de chaque bloc, dépôt et téléchargement des pièces, `/employee/banks`.
- Ressources API filtrées par `FieldAccess` ; écritures idempotentes par UUID client (préparation du hors ligne de l'app, T-15).
- Contrat Scramble à jour.

### W04.2.10 — Documentation et livraison

- `02-reference/` : blocs vérifiables, pièces, banque, journal des consultations.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W04.2 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Versions | Première soumission, modification d'un bloc vérifié (valeur en vigueur inchangée), correction en place d'une version en attente, retrait d'une entité |
| Propriété | Seul le propriétaire soumet ; un RH, un manager, un ADM ne peuvent pas saisir pour lui |
| Justificatifs | Exigés ou non selon le réglage de l'entreprise ; types de fichier et taille ; téléchargement autorisé seulement |
| Banque | Chiffrement en base ; un seul compte principal ; **non-fuite** pour ADM et RH (écran, API, journal d'audit, justificatif) ; journal des consultations ; rechiffrement après rotation de la DEK |
| Pièces | Dépôt, remplacement, expiration, pièces attendues selon le type d'employé |
| Dossier sorti | Aucune soumission possible |
| API | Idempotence par UUID client ; autre entreprise ; contrat à jour |

## 8. Critères de sortie

- Tests ciblés W04.2 verts, dont la suite de non-fuite bancaire ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.3 (partie employé) et §5.4 sur le jeu de démonstration.
- Documentation et livraison de W04.2.10 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Vérification et rejet, valeur en vigueur mise à jour, complétude, relances, alertes d'expiration, pièces déposées par le RH, cloche | W04.3 |
| Accusé de réception d'un document | W05 |
| Pré-remplissage depuis Jobyflow | W15 |
| Assistant et dossier dans l'app, hors ligne | E02 |
