# E04 — FluxyRH Entreprise · Pointage et temps

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E03

## 1. Objet

Pointer depuis son téléphone : **scanner le QR** affiché par la borne du site, **poser sa carte**, voir la confirmation avec le bouton « Inverser », et continuer à pointer **hors ligne**. Consulter son planning et ses pointages. Pour le manager : présences du jour, corrections dans le délai autorisé, heures sup établies à l'avance. Pour le RH : validation des heures sup réalisées. À la fin d'E04, le pointage par téléphone est recetté sur le terrain.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-TPS-02, F-MOB-02 | Pointage QR + carte sur le téléphone |
| F-TPS-03, NF-05 | Hors ligne, correction d'horloge par le serveur, fenêtre bornée |
| F-TPS-05, 06 (mobile) | Corrections, heures sup établies, validation |
| F-MOB-04 | Actions du manager et du RH |

À lire : APPFLOW §5.6, §5.7, §7 ; TRD §12 ; UX/UI §7.3 ; `02-reference/` (protocole de pointage W06.2).

## 3. Prérequis et décisions

E03 livré.

| Sujet | Proposition |
|---|---|
| QR avant l'app Borne | La Borne arrive après l'app Entreprise : pour recetter, le QR courant d'une borne de démonstration est affiché par la commande de développement de W06.2.8 (écran d'un ordinateur) |
| Caméra | `react-native-vision-camera` avec lecture de codes (composant `QrScanner`) ; seuls les QR `fluxyrh://clock` sont acceptés |
| Durée de « Inverser » | Lue dans la configuration de l'entreprise (W06.1.2), composant `CountdownButton` |
| iPhone | Même parcours ; la pose de la carte passe par la feuille système Core NFC, ouverte automatiquement après le scan du QR |
| Envoi | En ligne : envoi immédiat et résultat affiché. Hors ligne : « En attente d'envoi », file chiffrée (E00.7) ; le refus éventuel est affiché au retour du réseau dans « Refusés à l'envoi » |

## 4. Étapes ordonnées

### E04.1 — Pointer

- Onglet **Pointer** (UX/UI §7.3) : scan du QR, pose de la carte, sens déterminé (dernier pointage connu de l'appareil ou du serveur), confirmation (photo, nom, sens, heure, site), « Inverser » pendant la durée réglée, envoi ou mise en file.
- Messages de refus explicites (code expiré : « Rescannez le QR », carte non active, site non autorisé, téléphone non enregistré, rejeu, fenêtre dépassée, période clôturée).

### E04.2 — Mon temps

- Planning de la semaine et jours fériés (W06.1.6) ; mes pointages et journées du mois (acceptés, refusés avec motif, mention « travail de nuit ») ; heures sup établies et réalisées ; téléchargement de la feuille de temps.

### E04.3 — Manager

- Onglet **Équipe** : présences du jour (présent, en retard, absent, pas encore pointé), pointages refusés à traiter, correction d'une journée dans le délai réglé (motif obligatoire), heures sup établies à l'avance pour un ou plusieurs membres.

### E04.4 — RH

- Onglet **Validations**, heures sup réalisées : valider, refuser (motif), avertissement de plafond avec motif.

### E04.5 — Recette terrain

- Sur un site de démonstration, avec plusieurs téléphones Android et iPhone et des cartes de test : en ligne, hors ligne pendant quelques heures, horloge du téléphone volontairement décalée, retour du réseau ; résultats consignés dans `05-recette/`, dont la dérive des horloges (TRD §27).

### E04.6 — Documentation et livraison

- `02-reference/` : écrans de pointage et de temps.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E04 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Scan | QR valide, QR étranger, QR expiré |
| Carte | Sa carte, celle d'un autre, carte inactive |
| Sens | Alternance, inversion dans le délai, au-delà |
| Hors ligne | File, ordre d'envoi, idempotence, refus « fenêtre dépassée » |
| Manager | Correction dans et hors délai, sa propre journée refusée, heures sup établies |
| RH | Validation, refus, plafond |

## 6. Critères de sortie

- `npm run check` vert ; recette terrain d'E04.5 consignée.
- Documentation et livraison d'E04.6 faites.

## 7. Reporté

| Élément | Fichier |
|---|---|
| Pointage sur la borne | B02 |
