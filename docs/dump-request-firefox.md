# Comment récupérer une requête dans Firefox
Il est parfois nécessaire de récupérer les requêtes effectuées par l'interface web de votre appareil afin de déboguer un problème ou d'implémenter une nouvelle fonctionnalité sur un appareil que nous ne possédons pas.
Voici comment procéder, en texte et en vidéo YouTube.

## Procédure

1. Ouvrez Firefox
2. Rendez-vous sur la page souhaitée dans l'interface web de votre modem
3. Allez dans Paramètres (les trois lignes horizontales en haut à droite) -> Plus d'outils -> Outils de développement Web
4. Dans les outils de développement, ouvrez l'onglet « Réseau »
5. (Optionnel) Définissez un filtre d'URL si vous connaissez celle que vous voulez enregistrer
6. Effectuez l'action nécessaire dans l'interface web
7. Trouvez la requête dans la liste (vérifiez ses en-têtes et son corps pour confirmer qu'il s'agit de la bonne)
8. Faites un clic droit sur la requête et sélectionnez « Enregistrer tout au format HAR », choisissez un nom explicite
9. Publiez ce fichier dans le fil de l'issue ou envoyez-le par e-mail au développeur pour analyse

## Vidéo explicative
https://youtu.be/DKKian-014E
