# NOON Tech — site officiel

Site statique sans dépendance, compilation ou pisteur.

URL : https://noonelche-cyber.github.io/noon-tech-site/

## Publication

GitHub Pages : Deploy from a branch, main, /(root). Les modifications sur main sont publiées automatiquement. Ce dépôt contient uniquement le site public.

## Liens permanents pour les apps

Ajouter à l’URL de base :
- about/ : présentation de NOON Tech
- contact/ : contact et support
- apps/joder/, apps/vosotros/, apps/drek/, apps/trampa/ : présentation et téléchargement
- privacy/ : confidentialité du site
- privacy/joder/, privacy/vosotros/, privacy/drek/, privacy/trampa/ : confidentialité de chaque app

Les politiques des apps ne sont pas encore publiées. Compléter ces pages avec les pratiques réelles de chaque application avant de les soumettre aux Stores.

## Ajouter un lien Store

Dans apps.json, remplacer store: null par une URL HTTPS Google Play ou App Store. Le bouton s’affiche automatiquement sur la page permanente de l’app. Mettre également à jour le statut Coming soon dans index.html.

## Modifier le site

- index.html : accueil et cartes
- assets/style.css : présentation responsive
- apps.json : liens de téléchargement
- assets/store.js : affichage des boutons Store
- about/, contact/, privacy/ : pages éditoriales

Les icônes JODER!, VOSOTROS et TRAMPA proviennent des applications NOON Tech. Les marques typographiques NOON Tech et DREK! peuvent être remplacées par leurs futurs assets.

## Intégration Android

Ouvrir les URL HTTPS avec un navigateur ou un Custom Tab. Par exemple : https://noonelche-cyber.github.io/noon-tech-site/about/
