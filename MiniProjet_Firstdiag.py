def afficher_matrice(taille_grille, points_noirs, points_couverts):
    """Affiche la matrice de la grille avec les points noirs et les points couverts."""
    grille = [["0" for _ in range(taille_grille)] for _ in range(taille_grille)]
    for (x, y) in points_noirs:
        grille[x][y] = "N"  # Marque les points noirs
    for (x, y) in points_couverts:
        if grille[x][y] == "N":
            grille[x][y] = "C"  # Marque les points couverts
        else:
            grille[x][y] = "X"  # Marque les zones couvertes sans points noirs
    print("\nMatrice actuelle :")
    for ligne in grille:
        print(" ".join(ligne))
    print("\n")

def calculer_taille_carre(point1, point2):
    """Calcule la taille minimale d'un carré couvrant deux points noirs."""
    x_min, y_min = min(point1[0], point2[0]), min(point1[1], point2[1])
    x_max, y_max = max(point1[0], point2[0]), max(point1[1], point2[1])
    return max(x_max - x_min, y_max - y_min) + 1

def couvrir_points_noirs_diagonal(points_noirs, taille_grille):
    # Initialise une liste pour stocker les carrés utilisés et la qualité de la solution (surface totale)
    carres_utilises = []
    surface_totale = 0
    points_couverts = set()  # Ensemble pour suivre les points déjà couverts

    # Fonction pour ajouter un carré à la liste des carrés utilisés
    def ajouter_carre(coord, taille):
        nonlocal surface_totale
        surface_totale += taille ** 2
        carres_utilises.append((coord, taille))

        # Marque les points couverts par ce carré
        x, y = coord
        for i in range(taille):
            for j in range(taille):
                if x + i < taille_grille and y + j < taille_grille:
                    points_couverts.add((x + i, y + j))

    # Initialisation du premier carré partant de la diagonale pour le premier point noir
    point_initial = points_noirs[0]
    diag_initial = (min(point_initial[0], point_initial[1]), min(point_initial[0], point_initial[1]))
    taille_initial = calculer_taille_carre(diag_initial, point_initial)
    ajouter_carre(diag_initial, taille_initial)

    # Itération pour chaque point noir restant
    for point in points_noirs[1:]:
        if point not in points_couverts:
            # Analyse 1 : Agrandir le dernier carré pour inclure ce nouveau point noir
            dernier_carre = carres_utilises[-1]
            coord, taille = dernier_carre
            nouvelle_taille = calculer_taille_carre(coord, point)

            # Analyse 2 : Ajouter un nouveau carré démarrant depuis le point de la diagonale le plus proche
            diag_nouveau = (min(point[0], point[1]), min(point[0], point[1]))
            taille_nouveau_carre = calculer_taille_carre(diag_nouveau, point)

            # Calcul de surface pour comparaison
            surface_agrandie = nouvelle_taille ** 2
            surface_nouveau_carre = surface_totale + (taille_nouveau_carre ** 2)

            # Choisir l'option qui minimise la surface totale
            if surface_agrandie < surface_nouveau_carre:
                # Agrandir le carré existant
                carres_utilises[-1] = (coord, nouvelle_taille)
                surface_totale -= taille ** 2
                surface_totale += surface_agrandie
                ajouter_carre(coord, nouvelle_taille)
            else:
                # Ajouter un nouveau carré depuis la diagonale
                ajouter_carre(diag_nouveau, taille_nouveau_carre)

            print(f"Analyse pour le point {point}:")
            afficher_matrice(taille_grille, points_noirs, points_couverts)

    # Filtrer les carrés uniques en gardant uniquement le plus grand pour chaque point de départ sur la diagonale
    unique_carres = {}
    for coord, taille in carres_utilises:
        if coord not in unique_carres or unique_carres[coord] < taille:
            unique_carres[coord] = taille

    # Calcul final de la surface totale en utilisant les carrés uniques
    carres_utilises_final = [(coord, taille) for coord, taille in unique_carres.items()]
    surface_totale_final = sum(taille ** 2 for taille in unique_carres.values())

    return carres_utilises_final, surface_totale_final

# Demande à l'utilisateur de saisir la taille de la grille et les emplacements des points noirs
taille_grille = int(input("Entrez la taille de la grille carrée : "))
nombre_points = int(input("Entrez le nombre des emplacements des points noirs : "))
points_noirs = []

print("Entrez les coordonnées des points noirs (x, y) :")
for _ in range(nombre_points):
    x, y = map(int, input("Coordonnées (x y) : ").split())
    points_noirs.append((x, y))

# Appel de la fonction avec les entrées de l'utilisateur
carres, surface_minimale = couvrir_points_noirs_diagonal(points_noirs, taille_grille)

# Affiche les résultats finaux
print("Carrés utilisés :", carres)
print("Surface minimale couverte :", surface_minimale)
