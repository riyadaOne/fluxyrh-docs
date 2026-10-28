# Livraison #002 — Alignement des spécifications et cohérence du plan — 2026-10-28

- **Réf. proposition** : #002 (analyse de cohérence du plan, puis option A de Q54 : mise à jour des spécifications document par document)
- **Réf. CDC** : PRD, TRD, APPFLOW, BACKEND SCHEMA, UX/UI DESIGN ; décisions 0001 et 0002
- **Dépôts touchés** : docs

## Fichiers créés

- `03-architecture/decisions/2026-10-28-0003-rh-voit-la-remuneration.md` : le RH voit toute la rémunération (lecture seule pour la paie), jamais la banque ; modifie P6.
- `03-architecture/decisions/2026-10-28-0004-souple-par-defaut.md` : principe « souple par défaut, durcissable par l'entreprise », règles de sécurité fixes, allègements retenus.

## Fichiers modifiés

- `04-planification/plan-implementation/` : corrections de cohérence A1 à A11 (heures sup établies à l'avance, variables de paie sans événements, signataires de contrat, signature de la direction sur courriers et formulaires, étapes web des fichiers mobiles déplacées dans le web : pointage de secours W06.1 à W06.3, code de sortie et son des bornes W03, configuration de borne W06.2, App Links et Universal Links W01.9, API de la Console W01.8) ; nouvelles exigences F-PLT-09 et F-TPS-08 dans la matrice ; identifiants légaux paramétrables (W02.9, W03.4).
- `01-specifications/PRD.md` (version 1.1) : résumé, acteurs, personas, exigences reformulées (F-EMP-07, F-TPS-05, F-CTR-01, F-CTR-02, F-PAY-05, F-PAY-07, F-PRO-02 à 04, F-TAL-01, F-TAL-04, F-CNF-01 à 04, F-PIL-04, F-MOB-01, F-IDN-05, F-ADM-07), nouvelles exigences F-PLT-09 (factures) et F-TPS-08 (pointage de secours), module Conformité, hors périmètre, décisions.
- `01-specifications/TRD.md` : §3, §7.1, §10.2, §11.1, §12, §13, §14.4, §15, §16, §17, §18, §19, §20, §25, §27, §28.
- `01-specifications/APPFLOW.md` : §2, §3, §4, §5.2, §5.3, §5.5 à §5.17, §5.20 (archives hors système), §5.21, §5.22 (factures, nouveau), §6, §7, §8.
- `01-specifications/BACKEND-SCHEMA.md` (version 1.1) : tables, colonnes, enums, cycles de vie et règles alignés (factures, identifiants légaux, invitations de compte, listes du dossier, justificatifs exigés, cartes, signatures, pointage de secours, heures sup, contrats par blocs et versions à signer, paiements sans virements, modèles de déclaration et de bilan social, propositions et exclusions de workflow ; retrait des archives, des formats de virement, des modèles de contrat et des textes par langue).
- `01-specifications/UXUI-DESIGN.md` (version 1.1) : principe U12 (signature), barre latérale, fiche employé, vérification, éditeur de contrat, approbations, composants, mobile Android et iOS, Borne, Console, codes de statut, langues, documents, page d'accueil, maquettes par module, décisions.
- `06-livraisons/2026-10-28-001-plan-implementation.md` : ROADMAP à 53 entrées.

## Tests ajoutés

Aucun (livraison documentaire).

## Écarts

Aucun : les spécifications et le plan disent désormais la même chose.

## Notes pour la suite

- Prochaine étape : proposition de W00 (amorçage technique).
- Identifiants de l'employé (Q56) : liste de types définie par l'entreprise, saisis par l'employé et vérifiés ; colonnes `cnps_number` et `niu` retirées de l'identité.
- Souple par défaut (décision 0004) : signataires de contrat pré-remplis (`contract_settings`), « Valider la sélection » sans argent en jeu, clôture des évaluations réglée par campagne, 2FA activée par l'utilisateur (`two_factor_required_roles` retirée), blocages du dossier incomplet réglables (congés, attestations, marquage « Payé », `incomplete_file_settings`).
- Rémunération et RH (Q57 à Q59, décision 0003) : PRD P6, TRD §9, APPFLOW, UX/UI, BACKEND SCHEMA et plan (W02.7, W04.2, W09.2 à W09.8, W11, W12.3, W13, W14) mis à jour.
