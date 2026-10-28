# B02 — FluxyRH Borne · Pointage

Dépôt : `FluxyRH-mobile/borne/` (fluxyrh-m-borne) · Dépend de : B01

## 1. Objet

Faire de la borne le point de pointage du site : elle affiche en permanence un **QR dynamique généré localement** (sans réseau), que les employés scannent avec l'app Entreprise, et elle **lit les cartes** des employés qui pointent directement sur elle. Elle confirme en plein écran (photo, nom, Entrée ou Sortie, bouton « Inverser »), refuse avec un motif clair, et garde les pointages dans une **file chiffrée et signée** quand le réseau manque. À la fin de B02, un site pointe toute une journée, avec ou sans réseau.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ORG-06 | QR local, file hors ligne, envoi au retour du réseau |
| F-MOB-02, F-TPS-02 | Pointage par la carte sur la borne |
| F-TPS-03, NF-05 | Fenêtre hors ligne, horloge corrigée par le serveur, anti-rejeu |

À lire : APPFLOW §5.6 ; TRD §12 ; UX/UI §8 ; `02-reference/` (protocole de pointage W06.2).

## 3. Prérequis et décisions

B01 livré.

| Sujet | Proposition |
|---|---|
| Confirmation hors ligne | Pour afficher le nom et la photo même sans réseau, la borne garde en cache **chiffré** la liste des cartes actives des employés autorisés sur son site (empreinte de la carte, nom, photo), mise à jour avec sa configuration ; le serveur reste seul juge à la réception |
| Carte inconnue de la borne | Hors ligne, une carte absente du cache est quand même mise en file avec la mention « à vérifier par le serveur » ; en ligne, le serveur répond immédiatement |
| Fin de la confirmation | Après la durée d'inversion réglée par l'entreprise, ou dès qu'une autre carte est posée (UX/UI §8) |
| Son | Bip distinct pour succès et refus, désactivable par l'admin dans la configuration de la borne |

## 4. Étapes ordonnées

### B02.1 — QR dynamique

- Code temporel calculé localement avec la clé HMAC de la borne (TRD §12.1) ; QR `fluxyrh://clock?k={borne}&s={pas}&c={code}` noir sur blanc, au moins 60 % de la largeur, barre de renouvellement du pas ; heure, date, entreprise, site, « Posez votre carte ici » avec la flèche vers le lecteur.

### B02.2 — Pointage par la carte

- Lecture NFC continue ; sens déterminé (dernier pointage connu de cette carte) ; confirmation plein écran (fond `success` pour Entrée, `neutral` pour Sortie, photo, nom, heure), `CountdownButton` « Inverser » ; refus plein écran `danger` 3 s avec le motif.

### B02.3 — File hors ligne

- File chiffrée (MMKV, clé du Keystore), chaque pointage signé par la borne, UUID v7, `captured_at` ; envoi par lots au retour du réseau, `sent_at` ; pastille « Hors ligne · N pointages en attente » ; nombre en attente dans le signal de vie.

### B02.4 — Recette terrain

- Un site de démonstration pendant une journée : arrivées groupées du matin, coupure du réseau de plusieurs heures, téléphones des employés qui scannent le QR de la borne (E04), cartes posées sur la borne ; résultats et dérive d'horloge consignés dans `05-recette/`.

### B02.5 — Documentation et livraison

- `02-reference/` : écrans et file de la borne.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut B02 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| QR | Changement de pas, horloge de la borne décalée, code vérifié par le serveur |
| Carte | Carte active, inactive, d'un autre site, inconnue hors ligne |
| Hors ligne | File signée, envoi au retour du réseau, fenêtre dépassée, idempotence |
| Affichage | Lisibilité, plein écran, carte suivante qui ferme la confirmation |

## 6. Critères de sortie

- `npm run check` vert ; recette terrain de B02.4 consignée.
- Documentation et livraison de B02.5 faites.
