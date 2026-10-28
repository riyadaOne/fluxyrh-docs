# W08.3 — Contrats · Signature (signataires)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W08.2 · Suite : W08.4 (vie du contrat)

## 1. Objet

Faire signer le contrat **sur papier et dans le système** : des copies du PDF à signer sont téléchargées et imprimées pour la signature manuscrite, et **chaque signataire signe aussi dans FluxyRH**, avec sa carte ou sans carte (confirmation par son mot de passe), dans l'ordre fixé par le RH, pour laisser la trace (qui, quand, par quel moyen, sur quelle empreinte). À la dernière signature, le contrat passe `Signé` et le **PDF final** (avec le bloc des signataires) est figé avec son empreinte (T-13) ; le RH peut y joindre le scan de l'exemplaire papier signé. W08.3 crée aussi l'écran « À signer » de l'espace personnel, commun à tout ce qui se signe dans le système. La signature sans carte se fait sur le web dès W08.3 ; la signature par carte se fait dans l'app (E06), simulée ici par des tests d'API.

## 2. Ce que les signataires reçoivent, produisent, transmettent

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **RH** | Contrat `À signer` (W08.2) | Copies imprimées ; scan de l'exemplaire signé | Signataires ; dossier de l'employé |
| **Employé** | Contrat et son PDF | Signature manuscrite + signature dans le système | Signataire suivant |
| **Signataires de l'entreprise** | Contrat signé par les précédents (boîte S-81 pour la direction) | Signature manuscrite + signature dans le système | RH : contrat `Signé` (W08.4 l'activera) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-CTR-02 | `À signer` → `Signé` |
| F-NFC-06 | Signature d'action `contrat`, horodatée, journalisée, empreinte du document |
| T-13 | PDF signé figé avec empreinte SHA-256 |

À lire : PRD §7.8 ; TRD §13, §15 ; APPFLOW §3.4, §5.9, §6.6 (S-81), §6.8 (S-68) ; BACKEND SCHEMA §5.5 (`action_signatures`), §5.8 (`contract_signatories`) ; UX/UI §6.8, §13.4.

## 4. Prérequis et décisions

W08.2 livré.

| Sujet | Proposition |
|---|---|
| Copies papier | Le PDF à signer (figé à l'envoi) se télécharge et s'imprime autant de fois que nécessaire ; chaque copie porte la référence et l'empreinte courte du document, pour qu'un exemplaire papier se rattache sans doute au contrat du système |
| Signature dans le système | **Obligatoire pour chaque signataire**, même s'il a signé sur papier : c'est la trace. Elle se fait **sur le web** (confirmation par le mot de passe de la personne) ou **dans l'app** (carte, code ou biométrie), selon la décision de W05 ; le moyen utilisé est enregistré |
| Ordre | Celui fixé par le RH (W08.2) : un signataire ne signe qu'après les précédents |
| Scan de l'exemplaire signé | Le RH peut déposer le scan de l'exemplaire papier signé, comme pièce RH du dossier liée au contrat (colonne `signed_scan_document_id` sur `contracts`, BACKEND SCHEMA mis à jour) ; facultatif, il ne remplace pas les signatures dans le système |
| Signature à la borne | Non : la borne est un appareil partagé, sans lecture confortable d'un document long |
| Désaccord ou demande de changement | Se règle **hors système** : le RH modifie le contrat en `À signer` autant de fois que nécessaire (W08.2) ; chaque modification invalide les signatures déjà apposées, qui restent dans l'historique (`action_signatures` est immuable), et chacun signe la nouvelle version |
| Écran « À signer » | S-68 regroupe tout ce qui attend une signature de la personne : contrats (W08.3), documents à accuser (W05), puis bulletins (W09.6) et courriers (W12.3) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Signataire `contract_signatories` | en attente → signé (`action_signature_id`, `signed_at`) ; ordre imposé par `rank` | Chaque signataire |
| Contrat | `a_signer` → `signe` (dernière signature sur la version en cours, PDF final figé) | SYS |

## 6. Étapes ordonnées

### W08.3.1 — Spécification

- APPFLOW §5.9 et BACKEND SCHEMA §5.8 et §6 mis à jour (copies papier, signature dans le système obligatoire, scan, signataires multiples, modification en `À signer`).

### W08.3.2 — Service de signature

- `ContractService::sign(contract, signer, method, proof, documentHash)` : signataire attendu à son rang, preuve valide selon le moyen (carte `active` de ce signataire et téléphone enregistré, ou mot de passe confirmé, ou code de l'appareil), empreinte égale à `unsigned_pdf_hash` ; signature d'action `contrat` (W05.8) ; journal ; notification au signataire suivant.
- Dernière signature : contrat `signe`, `signed_at`, génération du **PDF final** (contenu identique au PDF à signer + bloc des signataires « Signé électroniquement dans FluxyRH le … » avec le moyen (carte ou mot de passe) et empreinte, UX/UI §13.4), écriture sans écrasement possible, `pdf_hash` ; notification au RH et à l'employé.
- `attachSignedScan(contract, file)` (RH) ; une signature porte toujours sur la **version en cours** du PDF à signer.

**Critère de fin** : signature hors ordre, par une autre carte, sur un appareil non enregistré ou sur une empreinte différente → refusée ; le PDF final est identique au PDF à signer, plus le bloc des signataires.

### W08.3.3 — Écrans

- S-40 : téléchargement et impression des copies à signer, suivi des signatures par contrat (qui a signé, quand, avec quelle carte), dépôt du scan signé.
- S-68 `/me/signatures` : éléments à signer de la personne (contrats, documents à accuser), lecture et téléchargement du PDF, bouton « Signer » (confirmation par mot de passe), QR « Ouvrir dans l'app » pour signer par carte.
- S-81 `/approvals` (direction) : élément « contrat à signer » avec le résumé (nature, dates, salaire selon `FieldAccess`), lecture du PDF ; la signature se fait dans l'app.

### W08.3.4 — API

- `/api/v1/employee/signatures` (liste de ce qui attend une signature), `/{espace}/contracts/{id}/sign`, téléchargement du PDF à signer et du PDF signé.
- Contrat Scramble à jour ; protocole de signature décrit pour l'équipe mobile (lecture de la carte, empreinte, appareil).

### W08.3.5 — Documentation et livraison

- `02-reference/` : circuit de signature, copies papier, PDF final, scan, versions du PDF à signer.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W08.3 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Ordre | Signataire avant son tour refusé ; personne non désignée refusée |
| Preuves | Carte d'autrui, carte inactive, appareil non enregistré, mot de passe erroné, empreinte différente |
| Fin du circuit | Statut `signe` seulement après **toutes** les signatures dans le système, PDF final, empreinte, immuabilité du fichier |
| Copies et scan | Copie portant référence et empreinte ; scan rattaché, facultatif, sans effet sur le statut |
| Modification en cours de signature | Signature sur une version périmée refusée ; signatures précédentes invalidées mais conservées ; chacun signe la nouvelle version |
| Non-fuite | Le salaire n'apparaît pas pour un tiers dans S-68, S-81, notifications, API |
| Droits | Seuls les signataires désignés ; autre entreprise |

## 8. Critères de sortie

- Tests ciblés W08.3 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.9 jusqu'à `Signé` avec un client de signature simulé et une copie papier.
- Documentation et livraison de W08.3.5 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Activation, avenants, échéances, résiliation | W08.4 |
| Signature dans l'app | E06 |
| Accusé des bulletins et des courriers dans S-68 | W09.6, W12.3 |
| Cachet et signature graphique de la direction sur le PDF | W16 |
