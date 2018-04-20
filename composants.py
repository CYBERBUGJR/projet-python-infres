#!/usr/bin/python3
from itertools import cycle, chain, product, repeat
from functools import reduce
from random import shuffle, choice, random


LONGUEURS_BATEAUX = [2, 3, 3, 4, 4, 5]
ORDINAL = 0x2680

CASE_NON_JOUE = "\033[94m" + chr(0x2610) + "\033[0m"
# CASE_TOUCHE = "\x1b[6;30;42m" + chr(0x2611) + "\x1b[0m"
CASE_TOUCHE = "\033[92m" + chr(0x2611) + "\033[0m"
CASE_BLANC = "\033[91m" + chr(0x2612) + "\033[0m"

HORIZONTAL = 0
VERTICAL = 1

ORIENTATIONS = (VERTICAL, HORIZONTAL)


class Conventions:
    """Classe contenant des attributs et des méthodes statiques"""

    plateau_nb_lignes = 10
    plateau_nb_colonnes = 10

    navires_longueur = [2, 3, 3, 4, 4, 5]

    @staticmethod
    def generer_nom_ligne(x):
        return chr(65 + x)

    @staticmethod
    def generer_nom_colonne(y):
        return str(y)

    @staticmethod
    def generer_nom_case(x, y):
        return Conventions.generer_nom_ligne(x) +\
               Conventions.generer_nom_colonne(y)


class Case:
    instances = {}
    jouees = set()

    def __str__(self):
        return "Case({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "<Case({}, {})>".format(self.x, self.y)

    def __init__(self, x, y):
        # Aggrégation des coordonnées
        self.x = x
        self.y = y
        # On souhaite pouvoir accéder à une case à partir de ses coordonnées
        Case.instances[x, y] = self

        # Génération du nom de la case
        self._generer_nom()
        # On souhaite pouvoir accéder à une case à partir de son nom
        Case.instances[self.nom] = self

        # Suivi de l'évolution de la case
        self.jouee = False
        self.navire = None  # Non reliée à un navire pour l'instant.

    def _generer_nom(self):
        """Cette méthode peut être surchargée facilement"""
        self.nom = Conventions.generer_nom_case(self.x, self.y)

    def jouer(self):
        """décrit ce qu'il se passe lorsque l'on joue une case"""
        self.jouee = True
        self.jouees.add(self)

        if self.navire is not None:
            if len(self.navire.cases - self.jouees) == 0:
                return "Coulé !!"
            else:
                return "Touché !"
        else:
            return"Manqué !"

    @classmethod
    def generer_cases(cls):
        for x, y in product(range(Conventions.plateau_nb_lignes),
                            range(Conventions.plateau_nb_colonnes)):
            Case(x, y)

    def __str__(self):
        """Surcharge de la méthode de transformation en chaîne"""
        if not self.jouee:
            return CASE_NON_JOUE
        elif self.navire is None:
            return CASE_BLANC
        return CASE_TOUCHE


class Navire:
    instances = []
    cases_occupees = set()

    def __str__(self):
        return "Navire {} {}".format(self.longueur, self.orientation)

    def __init__(self, longueur):
        self.longueur = longueur
        self.orientation = choice(ORIENTATIONS)
        self.touche = False
        self.coule = False

        # performance / lisibilité:
        nb_lignes = Conventions.plateau_nb_lignes
        nb_colonnes = Conventions.plateau_nb_colonnes
        nb2l = Conventions.generer_nom_ligne
        nb2c = Conventions.generer_nom_colonne

        while True:
            if self.orientation == HORIZONTAL:
                rang = choice(range(nb_lignes))
                premier = choice(range(nb_colonnes + 1 - longueur))
                lettre = nb2l(rang)
                chiffres = [nb2c(x) for x in range(premier, premier + longueur)]
                self.cases = {Case.instances[l + c]
                              for l, c in product(repeat(lettre, longueur), chiffres)}
            else:
                rang = choice(range(nb_colonnes))
                premier = choice(range(nb_lignes + 1 - longueur))
                chiffre = nb2c(rang)
                lettres = [nb2l(x) for x in range(premier, premier + longueur)]
                # Créer le navire
                self.cases = {Case.instances[l + c]
                              for l, c in product(lettres, repeat(chiffre, longueur))}

            for existant in Navire.instances:
                if self.cases.intersection(existant.cases):
                    # Une case du navire se recoupe avec un navire existant
                    # La navire n'est pas bien placé, on le replace
                    break  # break relatif au "for existant in navires:"
            else:
                # Ajouter le navire au conteneur de navires
                Navire.instances.append(self)
                # Informer la case qu'elle contient un navire.
                for case in self.cases:
                    case.navire = self
                # Rajouter ces cases aux cases occupees :
                Navire.cases_occupees |= self.cases
                break  # break relatif au "while True:"

    @classmethod
    def generer_navires(cls):
        for longueur in Conventions.navires_longueur:
            Navire(longueur)


class Plateau:

    def __init__(self):
        # On crée les cases:
        Case.generer_cases()

        # On crée les navires:
        Navire.generer_navires()

        # performance / lisibilité:
        nb_lignes = Conventions.plateau_nb_lignes
        nb_colonnes = Conventions.plateau_nb_colonnes
        nb2l = Conventions.generer_nom_ligne
        nb2c = Conventions.generer_nom_colonne

        # On génère ici les labels pour faciliter l'affichage
        self.label_lignes = [nb2l(x) for x in range(nb_lignes)]
        self.label_colonnes = [nb2c(x) for x in range(nb_colonnes)]

    trait_horizontal = "\033[93m" + " \u23BC\u23BC" + "\u236D\u23BC\u23BC\u23BC" * 10 + "\u236D\033[0m\n"

    def affichage(self):
        result = "\033[93m   \u23D0 " + " \u23D0 ".join(self.label_colonnes) + " \u23D0\033[0m\n"

        iter_label_lignes = iter(self.label_lignes)

        for x, y in product(range(Conventions.plateau_nb_lignes),
                            range(Conventions.plateau_nb_colonnes)):

            # Trait horizontal pour chaque nouvelle ligne
            if y == 0:
                result += self.trait_horizontal
                result += "\033[93m {}\033[0m".format(next(iter_label_lignes))

            case = Case.instances[x, y]
            result += "\033[93m \u23D0\033[0m " + str(case) + ""

            # Affichage de la barre verticale droite du tableau:
            if y == 9:
                result += "\033[93m \u23D0\033[0m\n"
        # Affichage de la dernière ligne horizontale
        result += self.trait_horizontal + "\n\n\n"

        return result


    def tester_fin_jeu(self):
        """Permet de tester si le jeu est terminé ou non"""
        return not len(Navire.cases_occupees - Case.jouees)

    def jouer_un_coup(self, nom_case):
        """Permet de gérer la saisie d'un coup à jouer"""
        # Retrouver la case à partir de son nom
        case = Case.instances[nom_case]
        # Tester si la case a déjà été jouée
        if case.jouee:
            return "Cette case a déjà été jouée, merci d'en choisir une autre"
        else:
            return case.jouer()
