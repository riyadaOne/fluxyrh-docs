# E03 — FluxyRH Entreprise · Carte NFC et signature

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E02

## 1. Objet

Tout ce que l'app fait avec la carte employé : **activation** de sa carte avec son PIN, **Ma carte**, changement de PIN, déclaration de perte, **enregistrement du téléphone** pour le pointage, **accès rapide** au dossier en scannant une carte, ouverture de l'app quand une carte est approchée, gestion des cartes par l'admin et remise par le RH, et le composant de **signature** (`SignSheet`) réutilisé par les contrats, les bulletins, les documents et les courriers. À la fin d'E03, une carte de test (W05.10) s'active, s'utilise et se désactive depuis l'app.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-NFC-02 | Remise (RH), activation (EMP), désactivation |
| F-NFC-04 | Accès rapide au dossier filtré par les droits |
| F-NFC-06 | Signature d'actions avec ou sans carte |
| F-NFC-03 (app) | Carte approchée d'un téléphone : app ouverte selon le contexte |

À lire : APPFLOW §3.4, §5.5 ; TRD §13, §18.3 ; UX/UI §7.1, §7.4, §13.3 ; `02-reference/` (W05).

## 3. Prérequis et décisions

E02 livré ; cartes de test écrites avec une application NFC générique (W05.10).

| Sujet | Proposition |
|---|---|
| Ouverture de l'app par la carte | Filtre d'intention `NDEF_DISCOVERED` sur l'URI de badge de l'entreprise : si l'app est installée, elle s'ouvre ; la vérification de domaine (App Links, `autoVerify`) est finalisée en E10 avec l'empreinte du certificat. Sur iPhone, lecture NFC en arrière-plan et **Universal Links** (domaine associé), finalisés en E10 avec le fichier `apple-app-site-association` |
| Signature (`SignSheet`) | Résumé de ce qui est signé (titre, empreinte courte), puis au choix : **poser la carte**, ou confirmer par le **code ou la biométrie** du téléphone enregistré (décision de W05) ; le moyen est envoyé au serveur |
| Ma carte | Rendu serveur affiché dans une WebView (UX/UI §13.3), identique à la carte imprimée |

## 4. Étapes ordonnées

### E03.1 — Ma carte

- Statut, rendu de la carte, activation (carte posée + choix du PIN), changement de PIN, déclaration de perte (désactivation confirmée dans l'écran).
- Enregistrement du téléphone pour le pointage, confirmé par la carte (W05.7).

### E03.2 — Carte approchée du téléphone

- Intention NDEF (§3) ; selon le contexte (APPFLOW §3.4) : écran de pointage ouvert → pointage (E04) ; écran de signature ouvert → signature ; sinon : RH, MGR, DIR, PAIE → fiche de l'employé scanné (accès rapide, W05.5) ; ADM → carte dans la gestion des cartes ; EMP → Ma carte.

### E03.3 — Cartes de l'admin et remise par le RH

- ADM : onglet **Cartes** (suivi par statut, désactivation ; la préparation reste au web).
- RH : onglet **Cartes** (cartes livrées à remettre, remise confirmée, désactivation).

### E03.4 — Signature

- Composant `SignSheet` (§3) et écran « À signer » (S-68) : documents à accuser (W05.8) ; contrats, bulletins et courriers s'y ajoutent en E06, E07, E09.

### E03.5 — Documentation et livraison

- `02-reference/` : écrans de la carte, intention NDEF, signature.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E03 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Activation | Carte d'autrui, carte non remise, PIN, désactivation |
| Accès rapide | Chaque rôle, hors équipe pour un manager, données sensibles masquées |
| Intention | App fermée, ouverte, écran de pointage ou de signature au premier plan |
| Signature | Carte, code, biométrie, carte inactive, appareil non enregistré |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §3.4 et §5.5 avec des cartes de test.
- Documentation et livraison d'E03.5 faites.

## 7. Reporté

| Élément | Fichier |
|---|---|
| App Links vérifiés (`assetlinks.json`) | E10 |
| Activation et secours sur la borne | B03 |
