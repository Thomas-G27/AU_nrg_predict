import csv
import re

def lire_gcode_et_sauvegarder_csv(fichier_gcode, fichier_csv):
    # Initialisation de la dernière position connue
    derniere_position = {'X': 0, 'Y': 0, 'Z': 0}

    # Regex pour détecter les coordonnées X, Y et Z
    regex_coord = re.compile(r'([XYZ])([-+]?\d*\.?\d+)')
    
    # Liste pour stocker les coordonnées
    coordonnees_time = []

    # Lecture du fichier G-code
    with open(fichier_gcode, 'r') as gcode_file:
        for ligne in gcode_file:
            if "G" in ligne[0]:
                ligne.strip()
                l = ligne.split(";",4)
                """
                if len(l) == 2:
                    coord = {}
                    
                    # Recherche des coordonnées dans la ligne
                    for match in regex_coord.finditer(l(1)):
                        
                        axe = match.group(1)  # 'X', 'Y', ou 'Z'
                        valeur = float(match.group(2))
                        derniere_position[axe] = valeur  # Mise à jour de la dernière valeur connue pour cet axe
        
                    # Ajout de la dernière position connue pour chaque axe
                    coord['X'] = derniere_position['X']
                    coord['Y'] = derniere_position['Y']
                    coord['Z'] = derniere_position['Z']
                    
                    # On ajoute les coordonnées extraites
                        
                    coordonnees.append(coord)
                """
                if len(l) == 4:
                    l_a = l[2].split(",")
                    l_b = l[3].split(",")
                    
                    #coordinates of end of acceleration
                    coord = {}
                    coord['X'] = float(l_a[0][2:])
                    coord['Y'] = float(l_a[1])
                    coord['Z'] = float(l_a[2])
                    print(l_a)
                    coord['T'] = float(l_a[3][:-2])
                    
                    coordonnees_time.append(coord)
                    
                    #coordinates of end of plateau
                    coord = {}
                    coord['X'] = float(l_b[0][2:])
                    coord['Y'] = float(l_b[1])
                    coord['Z'] = float(l_b[2])
                    coord['T'] = float(l_b[3][:-3])
                    
                    coordonnees_time.append(coord)
                    
                    #coordinates of end of instruction
                    coord = {}
                    for match in regex_coord.finditer(l[0]):
                        
                        axe = match.group(1)  # 'X', 'Y', ou 'Z'
                        valeur = float(match.group(2))
                        derniere_position[axe] = valeur  # Mise à jour de la dernière valeur connue pour cet axe
        
                    # Ajout de la dernière position connue pour chaque axe
                    coord['X'] = derniere_position['X']
                    coord['Y'] = derniere_position['Y']
                    coord['Z'] = derniere_position['Z']
                    coord['T'] = float(l[1][7:])
                    # On ajoute les coordonnées extraites
                        
                    coordonnees_time.append(coord)
                    
    # Écriture des coordonnées dans un fichier CSV
    with open(fichier_csv, 'w', newline='') as csvfile:
        champs = ['X', 'Y', 'Z','T']
        writer = csv.DictWriter(csvfile, fieldnames=champs)

        writer.writeheader()
        for coord in coordonnees_time:
            writer.writerow(coord)

# Utilisation de la fonction
fichier_gcode = 'output5.gcode'
fichier_csv = 'test_lect_file2.csv'
lire_gcode_et_sauvegarder_csv(fichier_gcode, fichier_csv)

print(f"Les coordonnées ont été sauvegardées dans {fichier_csv}.")
