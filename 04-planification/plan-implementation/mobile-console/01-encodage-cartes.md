# C01 — FluxyRH Console · Encodage des cartes

Dépôt : `FluxyRH-mobile/console/` (fluxyrh-m-console) · Dépend de : C00

## 1. Objet

Encoder les cartes NFC préparées par les entreprises : prendre une carte dans la **file**, **réserver** son identifiant opaque, **écrire** l'URI de badge sur la puce, la **relire** pour vérifier, **confirmer** l'encodage, puis **verrouiller** la puce en lecture seule. À la fin de C01, les cartes de test de W05.10 sont remplacées par de vraies cartes encodées par la Console.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PLT-05 | File des cartes à encoder, encodage dans la Console |
| F-NFC-01, 02 | Identifiant opaque, aucune donnée en clair ; `Préparée` → `Encodée` |

À lire : APPFLOW §5.5 ; TRD §13 ; UX/UI §9 ; `02-reference/` (API d'encodage W05.3).

## 3. Prérequis et décisions

C00 livré ; un lot de cartes NTAG213, 215 ou 216 vierges.

| Sujet | Proposition |
|---|---|
| Verrouillage de la puce | **Définitif** (une puce verrouillée ne peut plus jamais être réécrite) : proposé après une relecture réussie, avec une confirmation explicite dans l'écran ; une carte non verrouillée reste réinscriptible en cas d'erreur |
| Réservation abandonnée | Si l'écriture échoue ou si l'admin abandonne, la réservation est annulée (W05.3) et la carte reste dans la file |
| Livraison | Reste au web plateforme (W05.3), par lot et par entreprise |

## 4. Étapes ordonnées

### C01.1 — File

- Onglet **Cartes** : cartes `preparee` de toutes les entreprises, par entreprise et par date ; nom de l'employé et entreprise pour l'impression et le tri.

### C01.2 — Encodage

- `NfcZone` d'écriture avec trois étapes visibles : écrire → relire → verrouiller ; réservation de l'identifiant (renvoyé une seule fois), écriture NDEF de `https://{slug}.fluxyrh.app/badge/{identifiant}`, relecture et comparaison, confirmation (`encodee`), verrouillage (§3).
- Messages clairs : carte déjà écrite, carte verrouillée, type de puce non pris en charge, carte retirée trop tôt.

### C01.3 — Documentation et livraison

- `07-exploitation/` : procédure d'encodage d'un lot de cartes.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut C01 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Encodage | Écriture, relecture identique, confirmation, verrouillage |
| Erreurs | Carte retirée, carte verrouillée, puce non prise en charge, réservation annulée |
| Bout en bout | Carte encodée → livrée (web) → remise (RH) → activée (E03 ou B03) → badge public |

## 6. Critères de sortie

- `npm run check` vert ; un lot de vraies cartes encodé et suivi jusqu'au pointage.
- Documentation et livraison de C01.3 faites.
