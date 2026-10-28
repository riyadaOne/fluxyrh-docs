# MEP — Mise en production

Dépôts : `FluxyRH-web/app/` (scripts `deploy/debian/`), `FluxyRH-docs/` (exploitation) · Dépend de : C02

## 1. Objet

Mettre FluxyRH en service réel : serveur Debian **dédié** dimensionné à partir des mesures faites pendant le développement, scripts d'installation et de déploiement, exposition par Cloudflare, e-mails, **sauvegardes** quotidiennes et mensuelles avec copie externe et restauration testée, **supervision**, sécurité du serveur, puis ouverture de la première entreprise cliente avec son app. À la fin de MEP, FluxyRH v1.0 est en production.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PLT-06, NF-09, T-18 | Sauvegardes quotidiennes (30 jours) et mensuelles (12 mois), copie externe, restauration testée chaque mois |
| NF-10 | Disponibilité 99,5 % par mois, supervision |
| NF-11 | Performances mesurées sur le serveur de production |
| T-16, T-17 | Secrets hors dépôt, migrations des entreprises par `migrate-tenants.php` |

À lire : TRD §2, §22, §25 ; PRD §9 ; `05-recette/` (mesures de performance de W09.4, recettes complètes W16, E10, B03, C02).

## 3. Prérequis et décisions

Toutes les recettes web et mobiles consignées. Tous les secrets (clé maître, SMTP, Firebase, Cloudflare, accès SSH) sont créés et saisis **par le développeur**, jamais lus ni affichés par Claude.

| Sujet | Proposition |
|---|---|
| Hébergeur du serveur dédié | **Retenu** : un serveur dédié en Europe (Hetzner ou OVHcloud), l'accès passant par Cloudflare ; le choix peut encore changer au moment de la commande |
| Dimensionnement | Calculé à partir des mesures (taille d'une base type, durée de la paie de 200 employés, volume des fichiers) consignées en W09.4 et pendant les recettes (TRD §25.2) |
| Stockage des sauvegardes | **Retenu** : sauvegardes chiffrées gardées **en local** sur le serveur **et** copiées sur un stockage objet compatible S3 chez un autre fournisseur (Backblaze B2 ou Wasabi), chiffrées avant l'envoi |
| Supervision | **Retenu** : UptimeRobot (disponibilité) et Healthchecks.io (sauvegardes et tâches planifiées), alertes par e-mail |
| Clé maître | Sauvegardée **séparément** des données (coffre de mots de passe du développeur + copie hors ligne) ; procédure de rotation écrite |

## 4. Étapes ordonnées

### MEP.1 — Serveur

- Commande du serveur (§3) ; Debian, mises à jour automatiques de sécurité, pare-feu, aucun port ouvert au public hormis le tunnel Cloudflare ; SSH seulement via Cloudflare Access.
- `deploy/debian/install.sh` : Nginx, PHP 8.5-FPM (avec `intl`, `bcmath`, `sodium`), MySQL 8, Node pour la compilation, service `fluxyrh-queue`, cron `schedule:run`, utilisateur système dédié.

### MEP.2 — Déploiement

- `deploy/debian/deploy.sh` (TRD §25.2) : maintenance → `git pull --ff-only` → `composer install --no-dev` → `npm ci && npm run build` → migrations générales → `migrate-tenants.php` → synchronisation des articles d'aide (W10.5) → `storage:link`, `optimize` → rechargement de PHP-FPM et du worker → fin de maintenance.
- Procédure de retour arrière (version précédente et sauvegarde de la base).

### MEP.3 — Exposition et e-mails

- Cloudflare : DNS joker `*.fluxyrh.app`, `fluxyrh.app`, `platform.fluxyrh.app`, tunnel `cloudflared`, Access pour SSH.
- SMTP Google Workspace depuis `no-reply@fluxyrh.app`, SPF, DKIM, DMARC vérifiés.

### MEP.4 — Sauvegardes

- `deploy/debian/backup.sh` : `mysqldump --single-transaction` de la base générale et de chaque base d'entreprise + fichiers privés, chiffrement, copie locale sur le serveur et copie externe ; quotidiennes conservées 30 jours, mensuelles 12 mois (TRD §25.3).
- `deploy/debian/restore.sh` et **premier test de restauration** sur un environnement isolé, consigné ; test mensuel planifié.
- Procédure de préparation hors système d'une archive demandée par une entreprise (W10).

### MEP.5 — Supervision

- Disponibilité HTTP (accueil, plateforme, une entreprise), worker, espace disque, réussite des sauvegardes, expiration des certificats ; alertes par e-mail.
- Mesure des performances sur le serveur de production (page < 2 s, paie de 200 employés < 1 min) consignée.

### MEP.6 — Ouverture

- Création des admins plateforme (commande `fluxyrh:platform-admin`).
- Création de la première entreprise cliente, accompagnement de sa mise en place (listes de démarrage), app publiée (E10), bornes appairées (B01), cartes encodées (C01).
- Applications Borne et Console publiées (fiche Borne publique, Console en test interne).

### MEP.7 — Documentation et livraison

- `07-exploitation/` : installation, déploiement, retour arrière, sauvegarde et restauration, rotation de la clé maître, incidents, ajout d'une entreprise et de son app.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut MEP dans la ROADMAP ; PRD et TRD marqués « version 1.0 en production ».

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Déploiement | Déploiement à blanc, migration de plusieurs entreprises, retour arrière |
| Sauvegardes | Sauvegarde complète, copie externe, restauration réussie et vérifiée |
| Supervision | Alerte reçue sur un service arrêté, un disque plein simulé, une sauvegarde manquée |
| Sécurité | Aucun port ouvert hors tunnel, SSH impossible sans Access, en-têtes HTTPS |
| Performance | Objectifs NF-11 tenus en production |

## 6. Critères de sortie

- Première entreprise cliente en service, avec son app, ses bornes et ses cartes.
- Restauration testée et consignée ; supervision active.
- Documentation et livraison de MEP.7 faites.
