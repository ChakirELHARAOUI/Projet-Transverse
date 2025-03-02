from typing import List, Tuple, Set
import sys


Candidate = Tuple[Tuple[int, int], int, str, Set[Tuple[int, int]]]

def afficher_matrice(taille: int, points_noirs: Set[Tuple[int, int]], covered: Set[Tuple[int, int]]) -> None:
    """Affiche la grille avec les points noirs et la couverture.
    Les cellules marquées 'N' sont des points noirs non couverts,
    'C' sont des points noirs couverts,
    et 'X' des cellules couvertes qui ne sont pas des points noirs."""
    grille = [["0" for _ in range(taille)] for _ in range(taille)]
    for (i, j) in points_noirs:
        grille[i][j] = "N"
    for (i, j) in covered:
        if grille[i][j] == "N":
            grille[i][j] = "C"
        else:
            grille[i][j] = "X"
    print("\nMatrice :")
    for ligne in grille:
        print(" ".join(ligne))
    print()

def generer_candidates(taille: int) -> List[Candidate]:
    """
    Génère tous les candidats de carrés dans une grille de taille 'taille'
    dont l'orientation est fixée :
      - Pour "main" : le carré a son coin supérieur gauche sur la diagonale principale, i.e. (a, a).
      - Pour "anti" : le carré a son coin supérieur droit sur l'antidiagonale, i.e. (a, taille-1-a).
        Dans ce cas, le coin supérieur gauche est (a, taille-1-a - s + 1) pour un carré de taille s.
    """
    candidats = []
    # Générer candidats pour la diagonale principale
    for a in range(taille):
        # la taille possible varie de 1 jusqu'à taille - a
        for s in range(1, taille - a + 1):
            top_left = (a, a)
            covered = {(i, j) for i in range(a, a+s) for j in range(a, a+s)}
            candidats.append((top_left, s, "main", covered))
    # Générer candidats pour l'antidiagonale
    for a in range(taille):
        for s in range(1, taille - a + 1):
            # Le coin supérieur droit doit être sur l'antidiagonale : (a, taille-1-a)
            # Alors le coin supérieur gauche est : (a, taille-1-a - s + 1)
            top_left_col = taille - 1 - a - s + 1
            if top_left_col < 0:
                continue
            top_left = (a, top_left_col)
            covered = {(i, j) for i in range(a, a+s) for j in range(top_left_col, top_left_col+s)}
            candidats.append((top_left, s, "anti", covered))
    return candidats

def couvrir_points_optimal(points: Set[Tuple[int, int]], candidats: List[Candidate]) -> Tuple[List[Candidate], int]:
    """
    Par backtracking, trouve une combinaison de candidats dont l'union recouvre tous les points noirs
    et dont la somme des aires (size²) est minimale.
    """
    best_solution = None
    best_area = sys.maxsize

    def backtrack(covered: Set[Tuple[int, int]], sol: List[Candidate], area: int, start: int):
        nonlocal best_solution, best_area
        if points.issubset(covered):
            if area < best_area:
                best_area = area
                best_solution = sol.copy()
            return
        if area >= best_area:
            return
        for i in range(start, len(candidats)):
            cand = candidats[i]
            # Considérer ce candidat seulement s'il recouvre au moins un point noir non couvert
            if not (cand[3] & (points - covered)):
                continue
            new_covered = covered.union(cand[3])
            backtrack(new_covered, sol + [cand], area + cand[1]**2, i+1)

    backtrack(set(), [], 0, 0)
    return best_solution, best_area

def saisir_entier(message: str) -> int:
    while True:
        try:
            valeur = int(input(message).strip())
            if valeur < 1:
                print("Veuillez entrer un entier positif.")
                continue
            return valeur
        except ValueError:
            print("Entrée invalide. Veuillez entrer un entier.")

def saisir_coordonnees(taille: int) -> Tuple[int, int]:
    """Demande à l'utilisateur de saisir une coordonnée (ligne et colonne)."""
    while True:
        try:
            ligne = int(input(f"Entrez la ligne (0 à {taille-1}) : ").strip())
            colonne = int(input(f"Entrez la colonne (0 à {taille-1}) : ").strip())
            if 0 <= ligne < taille and 0 <= colonne < taille:
                return (ligne, colonne)
            else:
                print(f"Erreur : les valeurs doivent être entre 0 et {taille-1}.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer des entiers.")

if __name__ == "__main__":
    # Saisie de la taille de la grille et des points noirs
    taille = saisir_entier("Entrez la taille de la grille carrée : ")
    nb_points = saisir_entier("Entrez le nombre de points noirs : ")
    points = set()
    print("Entrez les coordonnées des points noirs (ligne, colonne) :")
    for i in range(nb_points):
        coord = saisir_coordonnees(taille)
        points.add(coord)
    print("\nPoints noirs :", points)
    
    # Générer les candidats
    candidats = generer_candidates(taille)
    print(f"\n{len(candidats)} candidats générés.")
    
    # Rechercher la couverture optimale par backtracking
    solution, area = couvrir_points_optimal(points, candidats)
    if solution is None:
        print("Aucune solution trouvée.")
    else:
        print("\n=== Solution Optimale ===")
        for idx, cand in enumerate(solution):
            top_left, s, orient, cov = cand
            print(f"Carré {idx+1}: Coin supérieur gauche = {top_left}, Taille = {s}, Orientation = {orient}, Aire = {s*s}")
        print(f"\nSurface totale couverte : {area}")
        
        # Affichage final de la matrice
        final_covered = set()
        for cand in solution:
            final_covered.update(cand[3])
        afficher_matrice(taille, points, final_covered)
