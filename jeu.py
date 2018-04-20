#!/usr/bin/python3

from saisie import (
    demander_saisie_oui_ou_non,
    demander_saisie_case,
)

from composants import (
    Case,
    Navire,
    Plateau,
)


def jouer_une_partie():
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide

    plateau = Plateau()

    while True:
        while True:
            print(plateau.affichage())
            nom_case = demander_saisie_case("Choisissez une case (lettre + chiffre)")
            print(plateau.jouer_un_coup(nom_case))

            if plateau.tester_fin_jeu():
                # Si le jeu est terminé, on quitte la fonction
                print(plateau.affichage())
                print("Bravo. Le jeu est terminé !")
                return


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def jouer():
    while True:
        jouer_une_partie()

        if not choisir_de_rejouer():
            return
