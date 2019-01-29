Il est très avantageux d'utiliser pypy3 avec ce code, mais ce n'est pas nécessaire.

Ce code utilise uniquement des bibliothèques standards.

# Tarot

Ce dépot contient tout le nécessaire pour simuler le jeu de tarot. La plateforme prend des joueurs en entrée qui doivent être capable de donner un mouvement parmi la liste des mouvements fournis par la plateforme.

Le code est divisé en plusieurs dossiers :

## Tests

Ce dossier contient tout les testes unitaires. La plupart des fonctions de base ont leurs fonction de test associée.

- *make test* lance le fichier test_all.py qui lance tout les tests à l'aide de la bibliothèque unittest.

## Players

Contient un fichier par joueur pouvant être utilisé. Un joueur avec une heuristique de base, un joueur aléatoire et une variante d'ucb sont implémenté.

## Tarot

Implémentation de la plateforme de jeu.

## Experiments

Contient une base de donnée qui stocke le résultat d'une partie en fonction des paramètres. Le but étant que plusieurs programme stocke le résultat de plusieurs expérimentation et on fusionne après.

# Autres fichiers

test_ai.py contient un exemple d'utilisation de la plateforme en utilisant un joueur ucb et lance un certain nombre de parties et affiche le résultat.
