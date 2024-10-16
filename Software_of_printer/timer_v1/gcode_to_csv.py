import csv
import re

def gcode_into_csv(fichier_gcode, fichier_csv):
    # Initialisation de la dernière position connue
    derniere_position = {'X': 0, 'Y': 0, 'Z': 0}

    # Regex pour détecter les coordonnées X, Y et Z
    regex_coord = re.compile(r'([XYZ])([-+]?\d*\.?\d+)')
    
    # Liste pour stocker les coordonnées
    coordonnees_time = []
    time = 0.0
    # Lecture du fichier G-code
    with open(fichier_gcode, 'r') as gcode_file:
        for line in gcode_file:
            if "G" in line[0]:
                l_a = []
                l_b = []
                line.strip()
                l = line.split(";",4)
                
                if "=" not in l[1]:
                    l.pop(1)
                if len(l) == 4:
                    l_a = l[2].split(",")
                    l_b = l[3].split(",")
                elif len(l) == 3:
                    l_a = l[1].split(",")
                    l_b = l[2].split(",")
                    
                #coordinates of end of acceleration
                if len(l_a) > 2:
                    coord = {}
                    coord['X'] = float(l_a[0][2:])
                    coord['Y'] = float(l_a[1])
                    coord['Z'] = float(l_a[2])
                    coord['T'] = time + float(l_a[3])
                    coord['A'] = int(l_a[4][:-2])
                    
                    coordonnees_time.append(coord)
                    
                #coordinates of end of plateau
                if len(l_b) > 2:
                    coord = {}
                    coord['X'] = float(l_b[0][2:])
                    coord['Y'] = float(l_b[1])
                    coord['Z'] = float(l_b[2])
                    coord['T'] = time + float(l_b[3])
                    try: coord['A'] = int(l_b[4][:-2])
                    except: coord['A'] = int(l_b[4][:-3])
                    
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
                try:
                    time_and_acc = l[1].split(",")
                    time += float(time_and_acc[0][7:])
                    acc = int(time_and_acc[1])
                except:
                    time_and_acc = l[2].split(",")
                    time += float(time_and_acc[0][7:])
                    acc = int(time_and_acc[1])
                coord['T'] = time
                coord['A'] = acc

                coordonnees_time.append(coord)
                    
    # Écriture des coordonnées dans un fichier CSV
    with open(fichier_csv, 'w', newline='') as csvfile:
        champs = ['X', 'Y', 'Z', 'T', 'A']
        writer = csv.DictWriter(csvfile, fieldnames=champs)

        writer.writeheader()
        for coord in coordonnees_time:
            writer.writerow(coord)

# uncomment if debug is needed
#fichier_gcode = 'output8.gcode'
#fichier_csv = 'coord_with_infos.csv'
#gcode_into_csv(fichier_gcode, fichier_csv)

#print(f"Les coordonnées ont été sauvegardées dans {fichier_csv}.")
