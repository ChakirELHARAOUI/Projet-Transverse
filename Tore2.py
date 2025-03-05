def wrap_coordinates(x, y, taille_grille):
    """Gère les coordonnées en mode tore (grille cyclique)."""
    return (x % taille_grille, y % taille_grille)

def calculer_taille_carre_tore(point1, point2, taille_grille):
    """Calcule la taille minimale d'un carré couvrant deux points noirs sur un tore."""
    x1, y1 = point1
    x2, y2 = point2

    # Distances normales
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Distances en passant par les bords opposés
    dx_tore = min(dx, taille_grille - dx)
    dy_tore = min(dy, taille_grille - dy)

    return max(dx_tore, dy_tore) + 1

def afficher_matrice(taille_grille, points_noirs, points_couverts):
    """Affiche la matrice en mode tore."""
    grille = [["0" for _ in range(taille_grille)] for _ in range(taille_grille)]
    
    # Placement des points noirs
    for (x, y) in points_noirs:
        grille[x][y] = "N"

    # Placement des points couverts
    for (x, y) in points_couverts:
        grille[x][y] = "X"  # X pour une zone couverte

    # Affichage
    print("\nMatrice finale :")
    for ligne in grille:
        print(" ".join(ligne))
    print("\n")

def ajouter_carre_tore(coord, taille, taille_grille, points_couverts):
    """Ajoute un carré tout en tenant compte des connexions en tore."""
    x, y = coord
    for i in range(taille):
        for j in range(taille):
            new_x, new_y = wrap_coordinates(x + i, y + j, taille_grille)
            points_couverts.add((new_x, new_y))

def couvrir_points_noirs_tore(points_noirs, taille_grille):
    """Couvre les points noirs en tenant compte de la topologie toroïdale."""
    carres_utilises = []
    surface_totale = 0
    points_couverts = set()

    # Fonction pour ajouter un carré
    def ajouter_carre(coord, taille):
        nonlocal surface_totale
        surface_totale += taille ** 2
        carres_utilises.append((coord, taille))
        ajouter_carre_tore(coord, taille, taille_grille, points_couverts)

    # Couvrir chaque point noir
    for point in points_noirs:
        if point not in points_couverts:
            taille_carre = 2  # Taille minimale pour garantir la couverture sur un tore
            ajouter_carre(point, taille_carre)

    return carres_utilises, surface_totale, points_couverts

# Saisie utilisateur
taille_grille = int(input("Entrez la taille de la grille carrée : "))
nombre_points = int(input("Entrez le nombre de points noirs : "))
points_noirs = []

print("Entrez les coordonnées des points noirs (x, y) :")
for _ in range(nombre_points):
    x, y = map(int, input("Coordonnées (x y) : ").split())
    points_noirs.append((x, y))

# Exécution du programme
carres, surface_minimale, points_couverts = couvrir_points_noirs_tore(points_noirs, taille_grille)

# Affichage des résultats finaux
print("\n=== Résultats finaux ===")
print("Carrés utilisés :", carres)
print("Surface minimale couverte :", surface_minimale)
afficher_matrice(taille_grille, points_noirs, points_couverts)  # Affichage final
