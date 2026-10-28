# E06 — FluxyRH Entreprise · Contrats

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E05

## 1. Objet

Consulter son contrat et **signer dans l'app** les contrats qui attendent sa signature, avec sa carte ou avec le code ou la biométrie du téléphone ; pour les signataires de l'entreprise (direction par défaut), signer depuis **Approbations**. À la fin d'E06, la signature par carte des contrats est recettée sur le terrain.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-CTR-02 (mobile) | Signature des contrats dans l'ordre fixé par le RH |
| F-NFC-06 | Signature avec ou sans carte, moyen enregistré |

À lire : APPFLOW §5.9 ; UX/UI §7.4 (signature, valeur sensible) ; `02-reference/` (W08.3).

## 3. Prérequis et décisions

E05 livré.

| Sujet | Proposition |
|---|---|
| Lecture avant signature | Le PDF à signer s'affiche en entier dans l'app ; le bouton « Signer » n'apparaît qu'une fois la fin du document atteinte |
| Version en cours | Si le RH modifie le contrat pendant la signature, l'app recharge la nouvelle version et indique que la signature précédente ne vaut plus |
| Salaire | Visible par l'employé concerné et les signataires autorisés, masqué par défaut (`SensitiveValue`) |

## 4. Étapes ordonnées

### E06.1 — Mon contrat

- Onglet **Documents**, contrat actif et historique (PDF), avenants.

### E06.2 — Signer

- « À signer » (E03.4) : contrats en attente de la personne, à son rang ; lecture (§3), `SignSheet` (carte, code ou biométrie) ; état des signatures.
- Signataires de l'entreprise : élément « contrat à signer » dans **Approbations**.

### E06.3 — Documentation et livraison

- `02-reference/` : écrans des contrats.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E06 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Signature | Carte, code, biométrie, ordre, version périmée, carte d'autrui |
| Lecture | Bouton absent avant la fin du document |
| Confidentialité | Salaire masqué par défaut, absent pour un tiers |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §5.9 avec signature par carte sur téléphone.
- Documentation et livraison d'E06.3 faites.
