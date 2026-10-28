# W08.2 — Contrats · Rédaction (RH)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W08.1 · Suite : W08.3 (signature)

## 1. Objet

Permettre au RH de rédiger le contrat d'un employé **par blocs** : à partir de la nature du contrat et du type d'employé, les blocs de la bibliothèque sont **proposés** (les présélectionnés sont insérés d'office) ; le RH les ordonne, en retire, en ajoute d'autres, écrit des blocs libres (qu'il peut enregistrer dans la bibliothèque), renseigne les conditions (nature, dates, période d'essai, horaires, **salaire de base**), **ajoute les signataires**, puis envoie pour signature, ce qui fige les valeurs de fusion et le PDF à signer. Le contrat est rédigé dans la **langue officielle** de l'entreprise. Le RH voit et rédige la rémunération contractuelle (exception de P6) ; l'admin entreprise ne la voit jamais. À la fin de W08.2, des contrats `À signer` attendent leurs signataires.

## 2. Ce que le RH reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Bibliothèque de blocs (W08.1) ; dossier vérifié et affectation (W04) | Contrat `Brouillon` puis `À signer`, PDF à signer figé, signataires ordonnés | **Signataires** (W08.3) : contrat à signer ; **paie** (W09.2) : salaire de base du futur contrat actif |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-CTR-02 (début) | `Brouillon` → `À signer` |
| F-CTR-04 | PDF à l'en-tête de l'entreprise ; rémunération contractuelle rédigée par le RH |
| T-09 | `base_salary` chiffré (catégorie `remuneration_contractuelle`), lu par `FieldAccess` |

À lire : PRD §6 (P6), §7.8 ; TRD §9, §15 ; APPFLOW §5.9, §6.4 (S-40) ; BACKEND SCHEMA §5.8, §8 ; UX/UI §6.7, §13.4.

## 4. Prérequis et décisions

W08.1 livré.

| Sujet | Proposition |
|---|---|
| Blocs proposés | À la création, `ClauseLibraryService::proposedFor()` (W08.1) : blocs présélectionnés insérés, autres blocs proposés dans un panneau ; le RH peut aussi prendre n'importe quel bloc de la bibliothèque. La colonne `contracts.contract_template_id` est retirée (BACKEND SCHEMA) |
| Bloc libre | Écrit dans le contrat ; bouton « Enregistrer dans la bibliothèque » qui en fait un nouveau bloc (brouillon à publier, W08.1) |
| Langue | Celle de l'entreprise au moment de la rédaction, enregistrée sur le contrat (`locale`) |
| Signataires | **Pré-remplis** (décision 0004) : l'employé (toujours) et le **signataire de l'entreprise par défaut**, réglé une fois dans la Configuration (onglet Contrats, table `contract_settings`) ; le RH ne les change, n'en ajoute ou ne modifie leur ordre que si besoin, parmi les rattachements actifs qui ont un dossier. `ContractParty` devient `employe` / `entreprise` ; modifiables jusqu'à la dernière signature : ajouter, retirer ou réordonner un signataire annule les signatures déjà faites, comme une modification du contrat. BACKEND SCHEMA §5.8 et §7 mis à jour |
| Deux PDF | Chaque signataire signe **l'empreinte du document qu'il a lu**, et le PDF final porte le bloc des signatures : ajout de `unsigned_pdf_path` et `unsigned_pdf_hash` (PDF à signer, figé à l'envoi) ; `pdf_path` / `pdf_hash` = PDF signé final (W08.3, T-13). Chaque modification en `À signer` crée une **nouvelle version** du PDF à signer ; les précédentes sont conservées (table `contract_signing_versions` : numéro, chemin, empreinte, date). BACKEND SCHEMA §5.8 mis à jour |
| Préalables à l'envoi | Employé `actif`, identité vérifiée (les champs du contrat viennent des valeurs vérifiées), tous les champs résolus, au moins un signataire de l'entreprise, dates cohérentes avec la nature (fin obligatoire pour CDD, stage, saisonnier ; période d'essai avant la fin) |
| Modification pendant la signature | Les discussions entre les parties se font **hors système**. Tant que toutes les signatures ne sont pas réunies, le contrat reste `À signer` et le RH le modifie **autant de fois que nécessaire**, sans changer son statut : chaque modification refige les valeurs et produit une nouvelle version du PDF à signer ; les signatures déjà apposées sur une version précédente restent dans l'historique mais ne valent plus, et chaque signataire signe la nouvelle version. BACKEND SCHEMA §8 mis à jour |
| Référence | `CTR-{annee}-{sequentiel}`, attribuée à la création, sous verrou |
| Plusieurs brouillons | Permis pour un même employé ; un seul contrat `actif` à la fois (contrôle à l'activation, W08.4) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Contrat `contracts.status` | (création) `brouillon` → `a_signer` ; modifications en `a_signer` sans changement de statut (§4) | RH |

`brouillon` et `a_signer` sont modifiables ; à partir de `signe`, le contrat est figé (BACKEND SCHEMA §8 mis à jour).

## 6. Étapes ordonnées

### W08.2.1 — Enums, permissions, spécification

- `ContractStatus`, `ContractParty` (`employe`, `entreprise`) ; permission `contracts` ; `SensitiveField` : `base_salary` (et avantages contractuels chiffrés) en `remuneration_contractuelle`.
- BACKEND SCHEMA §5.8 (deux PDF et leurs versions, signataires, retrait de `contract_template_id`) et §8 (contrat modifiable en `À signer`) mis à jour.

### W08.2.2 — Données

- Migrations `contracts` (sans `amends_contract_id` ni colonnes de fin, ajoutées en W08.4), `contract_blocks`, `contract_merge_values`, `contract_signatories`.
- Models, factories (états par statut).
- Migration `contract_settings` et onglet **Contrats** de la Configuration : signataire de l'entreprise par défaut (décision 0004).

### W08.2.3 — Service de rédaction

- `App\Services\Tenant\ContractService` :
  - `draft(employee, contractKind)` : conditions préremplies depuis l'affectation, blocs présélectionnés copiés (texte de la version publiée), langue officielle ;
  - édition du brouillon : conditions, blocs (ajouter depuis la bibliothèque, réordonner, retirer, bloc libre assaini, enregistrer un bloc libre dans la bibliothèque), champs ;
  - signataires : ajouter, ordonner, retirer (§4) ;
  - `sendForSignature()` : préalables (§4), résolution et **gel** de toutes les valeurs dans `contract_merge_values` (sensibles chiffrées), PDF à signer généré et figé avec son empreinte, journal, notification au premier signataire ;
  - `update()` en `a_signer` (§4) : nouvelle version du PDF à signer et des valeurs figées, signatures déjà apposées invalidées, signataires notifiés.
- Résolveurs `contrat.*` branchés dans `MergeFieldResolver`.

**Critère de fin** : un contrat envoyé ne change plus même si le dossier ou la bibliothèque changent ; un brouillon incomplet ou sans signataire de l'entreprise ne peut pas être envoyé.

### W08.2.4 — Écrans

- S-40 `/contracts` : liste (employé, nature, statut, dates ; salaire selon `FieldAccess`), filtres, corbeille des brouillons.
- Éditeur (UX/UI §6.7) : bibliothèque à gauche avec les **blocs proposés** en tête, contrat en blocs à droite, pastilles de champs, conditions du contrat, **signataires** (ajout, ordre), aperçu PDF à tout moment ; lecture seule dès `À signer` avec l'état des signatures.
- Onglet **Contrat** de la fiche S-21 : contrats de l'employé ; S-66 `/me/contract` : contrats de la personne.

### W08.2.5 — Confidentialité

- `FieldAccess` sur le salaire de base partout : liste, éditeur, PDF, aperçu, journal d'audit, API.
- Tests de **non-fuite** : l'ADM et le manager ne voient ni le salaire ni le PDF du contrat ; le RH, le PAIE, la direction et l'employé concerné le voient ; un signataire de l'entreprise voit le contrat qu'il doit signer.

### W08.2.6 — API

- `/api/v1/hr/contracts` (liste, détail, création, blocs proposés, signataires, envoi, retrait), `/employee/contracts` (lecture).
- Contrat Scramble à jour.

### W08.2.7 — Documentation et livraison

- `02-reference/` : rédaction par blocs, signataires, gel des valeurs, PDF à signer.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W08.2 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Rédaction | Blocs présélectionnés insérés, blocs proposés, ajout d'un bloc quelconque, bloc libre assaini et enregistré dans la bibliothèque, réordonnancement, langue officielle |
| Signataires | Pré-remplissage depuis la Configuration, ajout, ordre, signataire sans dossier refusé, au moins un signataire de l'entreprise |
| Envoi | Préalables (§4), gel des valeurs, PDF figé et empreinte, notification |
| Immuabilité | Toute modification refusée à partir de `signe` ; changement du dossier ou de la bibliothèque sans effet sur un contrat envoyé tant que le RH ne le modifie pas |
| Modification en `À signer` | Nouvelle version du PDF à signer et des valeurs, ancienne version conservée, signatures déjà apposées invalidées, statut inchangé |
| Non-fuite | ADM, MGR : aucun salaire (écran, PDF, API, journal) |
| Droits | `contracts` ; délégation, exclusion ; autre entreprise |

## 8. Critères de sortie

- Tests ciblés W08.2 verts, dont la non-fuite du salaire contractuel ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.9 jusqu'à `À signer`.
- Documentation et livraison de W08.2.7 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Copies papier, signatures dans le système, PDF signé | W08.3 |
| Activation, avenants, échéances, résiliation | W08.4 |
| Charte graphique du PDF | W16 |
