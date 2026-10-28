# E01 — FluxyRH Entreprise · Connexion, accès et administration

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E00

## 1. Objet

Ouvrir l'app à ses utilisateurs : connexion par mot de passe et 2FA, connexion **carte + PIN** pour qui l'a activée sur son téléphone, verrouillage par biométrie ou code du téléphone, profil (langue, thème, verrouillage, appareils, envois en attente), déconnexion, et les **écrans d'administration** de l'admin entreprise (utilisateurs, invitations, bornes, journal). À la fin d'E01, chaque rôle se connecte et retrouve ses onglets, en ligne comme hors ligne.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-MOB-05 | Verrouillage par biométrie ou code ; version minimale |
| F-NFC-05 | Connexion carte + PIN, choisie par l'utilisateur pour ses appareils |
| F-ADM-01, 02, 06, 08 (mobile) | Utilisateurs, invitations, connectés, journal pour l'admin |
| F-ORG-07 (mobile) | État des bornes, suspension |

À lire : APPFLOW §3.3, §4.2, §7 ; TRD §7, §17.1 ; UX/UI §7.2, §7.4 ; `02-reference/` (API d'authentification W02, connexion par carte W05, bornes W03).

## 3. Prérequis et décisions

E00 livré.

| Sujet | Proposition |
|---|---|
| Mot de passe expiré ou non conforme | L'app affiche « Changez votre mot de passe sur le web » avec le lien, comme le prévoit l'APPFLOW §7 |
| 2FA imposée non configurée | Même renvoi vers le web pour la configurer |
| Démarrage hors ligne | Jeton présent et profil en cache de moins de 7 jours → onglets avec le bandeau « Hors ligne » ; sinon « Connexion au réseau nécessaire » (APPFLOW §3.3) |
| Verrouillage | Proposé après la première connexion, activable et désactivable dans le Profil ; demandé au retour dans l'app après un délai (par défaut 5 minutes, réglable par l'utilisateur) |
| Connexion carte + PIN | Activée par l'utilisateur dans le Profil (carte active posée sur le téléphone + PIN de la carte) ; la lecture NFC est construite ici avec le composant `NfcZone`, réutilisé ensuite |

## 4. Étapes ordonnées

### E01.1 — Connexion

- Écran de connexion (logo de l'entreprise) : e-mail et mot de passe, défi 2FA (réponse 422 `two_factor`), mot de passe oublié (ouvre le web), messages du serveur traduits.
- Jeton enregistré dans le Keystore ; chargement de `/me` ; onglets du rôle (E00.8).
- Renvois au web (§3).

### E01.2 — Connexion par carte

- Composant `NfcZone` (react-native-nfc-manager) : « Posez votre carte au dos du téléphone » sur Android, feuille système Core NFC sur iPhone, lecture de l'URI de la carte, retours clairs (carte illisible, carte d'une autre entreprise).
- Activation de la connexion par carte dans le Profil (carte + PIN + clé d'appareil, W05.6) ; écran de connexion « Avec ma carte » ; 5 échecs → appareil révoqué, message explicite.

### E01.3 — Verrouillage et session

- Verrouillage biométrique ou code du téléphone (§3).
- Déconnexion : jeton et cache effacés, avertissement s'il reste des envois en attente.
- Déconnexion forcée par l'admin, rattachement suspendu, accès expiré, abonnement suspendu : retour à la connexion avec le message.

### E01.4 — Profil

- Onglet **Profil** : identité, langue, thème, verrouillage, connexion par carte, appareils enregistrés (retrait), **envois en attente** et **refusés à l'envoi** (E00.7), version de l'app, déconnexion.

### E01.5 — Écrans de l'admin entreprise

- Onglets **Utilisateurs** (liste, statut, suspendre, reprendre, révoquer avec motif), **Invitations** (liste, renvoyer, annuler ; la création reste au web), **Bornes** (état, dernier signal, suspendre), **Journal** (lecture, filtres) ; l'onglet **Cartes** arrive en E03.
- Aucun salaire, bulletin ni coordonnée bancaire (APPFLOW §4.2).

### E01.6 — Documentation et livraison

- `02-reference/` : connexion, verrouillage, profil, écrans d'administration.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E01 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Connexion | Mot de passe, 2FA, erreurs traduites, renvois au web, entreprise d'un autre flavor refusée |
| Carte | Activation, connexion, PIN faux, 5 échecs, carte désactivée |
| Session | Hors ligne avec cache valide et expiré, déconnexion forcée, 426 |
| Verrouillage | Activation, délai, empreinte ou Face ID, biométrie indisponible → code du téléphone |
| Admin | Actions, refus pour un autre rôle, aucune donnée sensible |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §3.3 sur téléphone avec une carte de test (W05.10), pour chaque rôle du jeu de démonstration.
- Documentation et livraison d'E01.6 faites.

## 7. Reporté

| Élément | Fichier |
|---|---|
| Activation de la carte, Ma carte, cartes de l'admin | E03 |
| Push et notifications | E08 |
