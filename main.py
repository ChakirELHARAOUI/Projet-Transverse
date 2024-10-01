def couvrir_points_noirs(grille):
    points_couverts = []
    taille_grille = len(grille)
    surface_totale = 0
    
    # Parcours de la grille pour trouver des points noirs
    for i in range(taille_grille):
        for j in range(taille_grille):
            if grille[i][j] == 1:  # Si on trouve un point noir
                # Trouver la plus grande taille de carré possible
                taille_max = trouver_taille_max(grille, i, j)
                points_couverts.append(((i, j), taille_max))
                surface_totale += taille_max ** 2
    
    return points_couverts, surface_totale

def trouver_taille_max(grille, x, y):
    # Fonction pour déterminer la taille maximale du carré à partir de (x, y)
    taille = 1
    # Implémenter ici la logique pour vérifier la taille maximale possible
    return taille

# Exemple d'appel
grille = [
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0]
]

solution, surface = couvrir_points_noirs(grille)
print(f'Solution : {solution}, Surface totale : {surface}')
