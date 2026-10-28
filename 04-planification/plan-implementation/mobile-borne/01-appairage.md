# B01 — FluxyRH Borne · Appairage

Dépôt : `FluxyRH-mobile/borne/` (fluxyrh-m-borne) · Dépend de : B00

## 1. Objet

Rattacher une borne neuve à **une entreprise et un site**, de façon sûre : l'admin affiche un QR d'appairage à usage unique (W03.5), la borne génère ses **clés dans le Keystore** (non exportables), scanne le QR, s'appaire en HTTPS épinglé, reçoit son jeton et sa **clé HMAC** chiffrée pour elle seule ; ensuite, chaque requête est **signée** et un **signal de vie** part toutes les 5 minutes. À la fin de B01, l'appairage réel remplace le client simulé de W03.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ORG-03, 07 | Appairage par QR unique, état et dernier signal, suspension, révocation, renouvellement de clé |
| T-11b | Jeton de 10 minutes, clé non exportable, requêtes signées, révocation immédiate |

À lire : APPFLOW §3.5 ; TRD §12.1, §12.5 ; `02-reference/` (protocole d'appairage et de signature, W03).

## 3. Prérequis et décisions

B00 livré.

| Sujet | Proposition |
|---|---|
| Clés | ECDSA P-256 pour signer, RSA-OAEP 2048 pour recevoir la clé HMAC (décision de W03), générées dans le Keystore, matérielles si l'appareil le permet |
| Épinglage du certificat | Sur `*.fluxyrh.app`, avec une clé de secours pour le renouvellement du certificat |
| Changement d'entreprise ou de site | Une borne appairée ne change pas d'entreprise : il faut la révoquer, effacer l'app (code admin) et l'appairer de nouveau |

## 4. Étapes ordonnées

### B01.1 — Appairage

- Écran « Borne non appairée » : génération des clés, scan du QR d'appairage, envoi (jeton, clés publiques, empreinte de l'appareil), réception et déchiffrement de la clé HMAC, stockage du jeton et de la clé dans le Keystore, configuration (`/kiosk/config` : entreprise, site, fuseau, pas du code, durée d'inversion, empreinte du code admin, langue).

### B01.2 — Requêtes signées et signal de vie

- Signature de chaque requête (corps et horodatage) ; signal de vie toutes les 5 minutes (version, batterie, pointages en attente, dérive d'horloge) ; nouvelle clé HMAC reçue dans la réponse après un renouvellement.
- Borne suspendue ou révoquée → écran « Borne désactivée ».

### B01.3 — Documentation et livraison

- `07-exploitation/` : appairer, renommer, suspendre, révoquer, remplacer une borne.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut B01 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Appairage | QR valide, expiré, déjà utilisé, réseau coupé pendant l'appairage |
| Sécurité | Clé non exportable, certificat non épinglé refusé, jeton copié sans la clé privée refusé par le serveur |
| Vie | Signal de vie, renouvellement de clé, suspension, révocation |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §3.5 avec une vraie tablette ; l'admin voit la borne active et son premier signal.
- Documentation et livraison de B01.3 faites.
