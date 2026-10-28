# B03 — FluxyRH Borne · Activation de carte et pointage de secours

Dépôt : `FluxyRH-mobile/borne/` (fluxyrh-m-borne), avec une étape dans `FluxyRH-web/app/` · Dépend de : B02

## 1. Objet

Permettre à un employé sans téléphone compatible d'**activer sa carte sur la borne** (carte posée + choix du PIN), et prévoir un **pointage de secours** pour un employé qui a perdu ou oublié sa carte, à faire valider par son manager. À la fin de B03, l'app Borne est complète.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-NFC-02 (borne) | Activation de la carte par l'employé sur la borne |
| PRD §11 (risque « perte de carte ») | Pointage de secours avec validation du manager |

À lire : APPFLOW §5.5, §5.6 ; PRD §11 ; `02-reference/` (W05.6, W06.2, W06.3).

## 3. Prérequis et décisions

B02 livré.

| Sujet | Proposition |
|---|---|
| Activation sur la borne | Bouton discret « Activer ma carte » : pose de la carte remise par le RH (statut `remise`), choix du PIN deux fois sur un clavier à l'écran, envoi signé (`/kiosk/card/activate`, W05.6) |
| Pointage de secours | Le PRD le prévoit (§11) mais les spécifications ne le décrivent pas. Retenu : bouton « Je n'ai pas ma carte » → saisie du **matricule** → **photo prise par la caméra de la borne** → pointage enregistré avec le statut **« à valider »** (nouvelle valeur de `ClockingStatus`), qui ne compte qu'après la validation du manager (écran des corrections, W06.3) ou son refus. BACKEND SCHEMA et APPFLOW §5.6 mis à jour |
| Abus du secours | Nombre de pointages de secours par employé et par mois limité (réglable par l'entreprise) ; au-delà, refus avec « adressez-vous à votre manager » |

## 4. Étapes ordonnées

### B03.1 — Serveur (web)

- Dans `FluxyRH-web/app/` : statut « à valider », photo de secours (disque privé), limite mensuelle dans les réglages du pointage, validation et refus par le manager dans les corrections (W06.3), tests.

### B03.2 — Activation de la carte

- Écran d'activation sur la borne (§3), retours clairs (carte non remise, carte d'une autre entreprise, PIN différents).

### B03.3 — Pointage de secours

- Écran « Je n'ai pas ma carte » (§3), photo, file hors ligne comme un pointage normal.

### B03.4 — Documentation et livraison

- `02-reference/` : activation et secours ; `05-recette/` : recette complète de l'app Borne.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut B03 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Activation | Carte remise, carte déjà active, PIN différents, hors ligne (refus clair : l'activation exige le réseau) |
| Secours | Matricule inconnu, photo, limite mensuelle, validation et refus du manager, hors ligne |

## 6. Critères de sortie

- `npm run check` vert ; recette complète de l'app Borne consignée.
- Documentation et livraison de B03.4 faites.
