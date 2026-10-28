# W12.3 — Processus RH · Courriers et formulaires types

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W12.2 · Module payant `processus_rh` · Clôt le module W12

## 1. Objet

Produire les documents RH sans ressaisie : **courriers types** (modèles avec champs de fusion) envoyés **en masse** — un PDF par destinataire déposé dans son espace, un e-mail, un accusé de réception dans le système si exigé — et **formulaires types** demandés par l'employé (attestation de travail, de salaire…), préparés par le RH, bloqués si le dossier est incomplet. Réutilise l'éditeur et les champs de fusion des contrats (W08.1). À la fin de W12.3, le module Processus RH est complet.

## 2. Ce que chacun reçoit, produit, transmet

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **RH** | Éditeur et champs de fusion (W08.1) ; demandes de formulaires | Modèles de courrier ; campagnes envoyées ; formulaires `Prêt` / `Refusé` | Employés |
| **EMP** | Courriers ; formulaires prêts | Demandes de formulaires ; accusés de réception | RH : suivi des accusés |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PRO-03 | Courriers types, envoi en masse (PDF et e-mail), accusé de réception |
| F-PRO-04 | Formulaires types : `Demandé` → `Prêt` / `Refusé` → `Remis` |
| F-EMP-09 (formulaires) | Pas de formulaire type sur dossier incomplet |
| F-NFC-06 (courriers, formulaires) | Signatures d'action `courrier` et `formulaire` |

À lire : PRD §7.11 ; TRD §15, §19 ; APPFLOW §5.13, §6.7 (S-73, S-74), §6.8 (S-67, S-68) ; BACKEND SCHEMA §5.11 (courriers, formulaires) ; UX/UI §13.4.

## 4. Prérequis et décisions

W12.2 livré.

| Sujet | Proposition |
|---|---|
| Courriel d'un courrier | Le courrier peut contenir des champs sensibles : l'e-mail **ne joint jamais le PDF**, il porte un lien vers l'espace de l'employé (TRD §19) |
| Champs sensibles dans un modèle | Règle de W08.1 : un auteur n'insère que les champs qu'il a le droit de lire. Le RH peut utiliser la rémunération contractuelle, pas la paie |
| Attestation de salaire | Le RH voit toute la rémunération (décision 0003) : il prépare les attestations fondées sur le contrat ou sur les bulletins. Chaque type de formulaire garde le **rôle qui le traite** (`rh` par défaut, `gestionnaire_paie` possible) ; colonne ajoutée à `form_types` |
| PDF figés | Chaque PDF de courrier et de formulaire est figé avec son empreinte (`pdf_hash` ajouté aux tables concernées), comme les documents signés |
| Signature de la direction | Un modèle de courrier ou un type de formulaire peut **exiger la signature de la direction** (colonnes `requires_direction_signature` et signataire désigné, ajoutées au BACKEND SCHEMA) : avant l'envoi de la campagne ou la remise du formulaire, le document attend la signature du directeur désigné dans sa boîte S-81 (signature dans le système, avec ou sans carte) ; sa signature graphique est apposée en W16 |
| Passage à `Remis` | Au premier téléchargement par l'employé ; si le type exige un accusé, à l'accusé de réception (avec ou sans carte) |
| Formulaires par défaut | Créés à l'activation du module, avec leurs modèles de courrier, **rédigés dans la langue officielle** de l'entreprise (fichiers de langue) et modifiables : attestation de travail, attestation de salaire (contractuel), certificat de travail (employé sorti) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Campagne `letter_campaigns.status` | `brouillon` → `a_signer` (si la signature de la direction est exigée) → `envoyee` | RH ; DIR signe |
| Destinataire | PDF généré → e-mail envoyé → accusé (si exigé) | SYS ; EMP |
| Formulaire `form_requests.status` | `demande` → `a_signer` (si la signature de la direction est exigée) → `pret` / `refuse` (motif) → `remis` | EMP ; RH ou PAIE ; DIR ; EMP |

## 6. Étapes ordonnées

### W12.3.1 — Enums et permissions

- `LetterCampaignStatus`, `FormRequestStatus` ; permissions `letters`, `form_requests` liées au module.

### W12.3.2 — Modèles de courrier

- Migrations `letter_templates`, `letter_template_texts`.
- S-73 `/letters`, onglet Modèles : éditeur (W08.1), objet et corps par langue, catégorie, aperçu PDF sur un employé fictif.

### W12.3.3 — Campagnes

- Migrations `letter_campaigns`, `letter_campaign_recipients` (avec `pdf_hash`).
- `App\Services\Tenant\LetterCampaignService` : sélection des destinataires (structure, site, type, liste), aperçu pour un destinataire, envoi en **job par lots** (un PDF par destinataire dans sa langue officielle, valeurs vérifiées, `DocumentRenderer`, PDF figé ; dépôt dans « Mes documents » ; e-mail avec lien), suivi des accusés, relance des accusés manquants.
- S-73 : création, destinataires, aperçu, envoi, suivi (générés, envoyés, accusés).
- Élément « courrier à accuser » dans S-68 ; accusé de réception (`courrier`), avec ou sans carte.
- Signature de la direction (§4) : élément « courrier à signer » dans S-81 ; la campagne part après la signature.

### W12.3.4 — Formulaires types

- Migrations `form_types` (avec le rôle qui traite), `form_requests` (avec `pdf_hash`).
- Formulaires et modèles de courrier par défaut (§4) créés à l'activation du module dans la langue officielle.
- `App\Services\Tenant\FormRequestService` : `request()` (dossier complet si l'entreprise bloque les attestations et si le type l'exige, `CompletenessService::blocks()`), `prepare()` (PDF figé), `refuse(reason)`, `deliver()` (§4), signature de la direction quand le type l'exige (élément dans S-81) ; notifications.
- S-67 `/me/requests`, onglet Formulaires : demande, suivi, téléchargement ; S-74 `/form-requests` (RH, PAIE selon le type) : demandes à traiter, aperçu, préparer, refuser ; S-74, onglet Types.

### W12.3.5 — API et documentation

- `/api/v1/employee/form-requests`, `/employee/letters` (liste, PDF, accusé), `/hr/letters`, `/hr/form-requests`.
- `02-reference/` : courriers, formulaires ; article d'aide.
- `05-recette/` : recette complète du module Processus RH.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W12.3 (et W12) dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Courriers | Ciblage, langue, valeurs vérifiées, PDF figé, dépôt, e-mail sans pièce jointe, accusé de réception, relance, attente de la signature de la direction avant l'envoi quand le modèle l'exige |
| Champs sensibles | Champ de paie refusé dans un modèle du RH ; masquage pour un lecteur non autorisé |
| Formulaires | Dossier incomplet bloqué ; rôle qui traite ; transitions ; signature de la direction exigée avant `pret` quand le type l'exige ; `remis` au téléchargement ou à l'accusé |
| Module | Fermé sans le module |
| Droits | `letters`, `form_requests` ; employé limité à ses documents ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W12.3 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.13 ; recette complète du module consignée.
- Documentation et livraison de W12.3.5 faites ; W12 complet dans la ROADMAP.

## 9. Reporté

| Élément | Module |
|---|---|
| Charte graphique des courriers et formulaires | W16 |
| Demandes et accusés dans l'app | E09 |
