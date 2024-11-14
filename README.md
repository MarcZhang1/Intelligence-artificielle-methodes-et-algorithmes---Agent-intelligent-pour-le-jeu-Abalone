
# Agent Intelligent pour le Jeu Abalone

Ce projet vise à implémenter un agent intelligent capable de jouer au jeu de stratégie **Abalone** dans le cadre du cours Intelligence artificielle : méthodes et algorithmes.

## Description du Projet

Le jeu Abalone est un jeu de stratégie en un contre un, où chaque joueur doit expulser un maximum de billes adverses hors du plateau pour remporter la partie. Le projet consiste à concevoir un agent automatique qui participe à un tournoi en utilisant une stratégie de jeu optimisée, basée sur les algorithmes d'intelligence artificielle.

## Structure du Code

- **my_player.py** : Fichier contenant l'implémentation de notre agent.

## Méthode Utilisée

L'agent utilise l'algorithme **Minimax** avec élagage **alpha-bêta**, qui évalue les actions possibles en minimisant les coups adverses et en maximisant les siens pour trouver la meilleure décision. Une **heuristique personnalisée** basée sur le nombre de pièces et la distance au centre du plateau guide les choix de l'agent.
