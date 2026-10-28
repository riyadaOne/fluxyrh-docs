# E10 — FluxyRH Entreprise · Marque blanche et publication

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E09

## 1. Objet

Produire **une app par entreprise**, sur Android et iOS : nom, icône, identifiants Android et iOS, URL de l'API, projet Firebase et signature propres, à partir de la configuration exportée par la plateforme (W01.9) ; vérifier le domaine pour que la carte ouvre l'app (App Links, Universal Links) ; publier sur Google Play et l'App Store et renseigner les liens des stores, qui partent ensuite avec les invitations. À la fin d'E10, la première entreprise cliente a son app sur le store.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-MOB-01 | Une app par entreprise, écrans selon les droits |
| F-PLT-08 (fin) | Format définitif de l'export de configuration, liens des stores |
| F-NFC-03 (app) | Ouverture vérifiée de l'app par l'URI de la carte |

À lire : TRD §18.1, §18.3, §25.5 ; APPFLOW §5.1 (fin) ; `02-reference/` (W01.9).

## 3. Prérequis et décisions

E09 livré. Pour chaque entreprise : icône et nom fournis par le client ; projets Firebase et leurs fichiers, clé de signature Android (keystore), certificats Apple, comptes Google Play et Apple Developer gérés **par le développeur**, jamais versionnés ni lus par Claude.

| Sujet | Proposition |
|---|---|
| Format de l'export | Fichier livré par W01.9 : nom de l'app, identifiants Android et iOS, URL de l'API, slug, couleur de l'icône adaptative |
| Signature | Une clé de téléversement par app, conservée hors dépôt par le développeur ; signature des builds par Google Play |
| App Links et Universal Links | Colonnes et routes livrées en W01.9 ; ici, l'empreinte du certificat Android et l'identifiant d'équipe Apple sont saisis sur la fiche « Application mobile » au moment de la publication |
| Build sous Windows | Android depuis un chemin court (piège 12), commandes Gradle données au développeur ; iOS sur le Mac ou le service de build choisi en E00 |
| Publication iOS d'une app en marque blanche | Apple refuse en général les apps produites depuis un même modèle si elles ne sont pas publiées par le propriétaire du contenu (règle 4.2.6 de l'App Store, **à vérifier dans les règles en vigueur au moment de la publication**) : **décision : publication depuis le compte Apple Developer de RIYADA ONE**, en assumant le risque d'un refus ; en cas de refus, repli sur un compte Apple ouvert par l'entreprise cliente |

## 4. Étapes ordonnées

### E10.1 — Flavors

- Génération d'un flavor Android et d'une cible iOS (scheme, bundle id) à partir du fichier exporté (W01.9) : identifiants, nom, icône, URL, fichiers Firebase du flavor (déposés par le développeur) ; flavor `demo` conservé.

### E10.2 — App Links et Universal Links

- Saisie de l'empreinte du certificat Android et de l'identifiant d'équipe Apple sur la fiche « Application mobile » (W01.9) ; vérification des deux fichiers servis par le sous-domaine de l'entreprise.
- Dans l'app : filtre d'intention `VIEW` avec `autoVerify` (Android) et domaine associé `applinks:{slug}.fluxyrh.app` (iOS) sur `https://{slug}.fluxyrh.app/badge/*`.

### E10.3 — Publication

- Android : build de release signé (commandes données au développeur), fiche Google Play (nom, icône, captures, politique de confidentialité), test interne, puis production.
- iOS : archive signée, fiche App Store Connect, TestFlight, soumission à la revue d'Apple depuis le compte de RIYADA ONE (§3) ; un refus éventuel et sa réponse sont consignés dans `07-exploitation/`.
- Liens des stores saisis sur la fiche « Application mobile » : ils partent avec les e-mails d'invitation (W02.3).

### E10.4 — Documentation et livraison

- `07-exploitation/` : procédure « nouvelle entreprise → nouvelle app » pas à pas.
- `05-recette/` : recette complète de l'app Entreprise sur le flavor du premier client.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E10 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Flavors | Deux apps d'entreprise installées côte à côte sur le même téléphone, Android et iPhone, chacune sur son entreprise |
| App Links, Universal Links | Carte approchée : ouverture vérifiée de la bonne app, sur Android et sur iPhone |
| Release | Build signé, version minimale respectée |

## 6. Critères de sortie

- App du premier client publiée ; procédure d'exploitation écrite ; recette complète consignée.
- Documentation et livraison d'E10.4 faites.
