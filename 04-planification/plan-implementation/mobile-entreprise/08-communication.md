# E08 — FluxyRH Entreprise · Communication

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E07

## 1. Objet

Relier l'app aux événements de l'entreprise : **notifications push** (Firebase), liste des notifications, **accueil** avec les tâches en attente du rôle, **annonces** avec « J'ai lu », et **centre d'aide**. Un appui sur une notification ouvre directement l'écran concerné. À la fin d'E08, chaque événement clé du web arrive sur le téléphone.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-COM-01 | Notifications in-app et push |
| F-COM-03 | Annonces, accusé de lecture |
| F-AID-01 | Centre d'aide |

À lire : APPFLOW §5.18 ; TRD §19 ; `02-reference/` (W04.3, W10).

## 3. Prérequis et décisions

E07 livré ; projet Firebase du flavor `demo` créé par le développeur, `google-services.json` (Android), `GoogleService-Info.plist` et clé APNs (iOS) déposés par lui, jamais versionnés ; compte de service déposé sur la fiche de l'entreprise de démonstration (W10.3).

| Sujet | Proposition |
|---|---|
| Autorisation des notifications | Demandée après la première connexion, avec une phrase qui explique l'usage ; refus respecté, rappel discret dans le Profil |
| Contenu | Jamais de valeur sensible (TRD §19) : le détail se lit dans l'écran ouvert |
| Ouverture depuis une notification | Lien interne vers l'écran concerné ; si l'utilisateur n'a plus le droit, message clair |

## 4. Étapes ordonnées

### E08.1 — Push

- Firebase Messaging (app Entreprise), enregistrement de l'appareil (`/push-devices`, lié au jeton) à la connexion, retrait à la déconnexion ; réception au premier plan et en arrière-plan ; ouverture de l'écran concerné.

### E08.2 — Accueil et notifications

- Onglet **Accueil** : pointer, tâches en attente du rôle (`/me/dashboard`), soldes, annonces non lues ; écran des notifications (lu, non lu).

### E08.3 — Annonces et aide

- Annonces ciblées, « J'ai lu » ; centre d'aide (catégories, recherche, article) dans la langue de l'utilisateur.

### E08.4 — Documentation et livraison

- `02-reference/` : push, accueil, annonces, aide.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E08 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Push | Enregistrement, retrait, réception, ouverture, droits retirés |
| Accueil | Tâches par rôle |
| Annonces | Ciblage, « J'ai lu » |
| Aide | Trois langues, recherche |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §5.18 sur téléphone avec de vrais push.
- Documentation et livraison d'E08.4 faites.
