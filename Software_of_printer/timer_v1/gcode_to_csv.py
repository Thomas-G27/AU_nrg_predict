import csv
import re

def gcode_into_csv(fichier_gcode, fichier_csv):
    # Initialization 
    derniere_position = {'X': 0, 'Y': 0, 'Z': 0}

    # Regex to detect coords X, Y and Z
    regex_coord = re.compile(r'([XYZ])([-+]?\d*\.?\d+)')
    regex_speed = re.compile(r'F([-+]?\d*\.?\d+)')
    # List with all coordinates
    coordonnees_time = []
    time = 0.0
    F_val = 0
    # Gcode reading
    with open(fichier_gcode, 'r') as gcode_file:
        for ligne in gcode_file:
            if "G" in ligne[0]:
                l_a = []
                l_b = []
                ligne.strip()
                l = ligne.split(";",4)
                
                ####-------planning modifications to extract speed--------####
                
                #getting the plateau feedrate/speed
                F_match = regex_speed.search(l[0])
                if F_match:
                    last_F_val = F_val
                    F_val = float(F_match.group(1))
                ####------------------------------------------------------####
                
                #Get read of unwanted comments and get eoa/eop vectors
                if "=" not in l[1]:
                    l.pop(1)
                if len(l) == 4:
                    l_a = l[2].split(",")
                    l_b = l[3].split(",")
                elif len(l) == 3:
                    l_a = l[2].split(",")
                
                #coordinates of end of acceleration
                if l_a != []:
                    coord = {}
                    coord['X'] = float(l_a[0][2:])
                    coord['Y'] = float(l_a[1])
                    coord['Z'] = float(l_a[2])
                    coord['T'] = time + float(l_a[3])
                    coord['A'] = int(l_a[4][:-2])
                    
                    coordonnees_time.append(coord)
                    
                #coordinates of end of plateau
                if l_b != []:
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
                    axe = match.group(1)  # 'X', 'Y', or 'Z'
                    valeur = float(match.group(2))
                    derniere_position[axe] = valeur  # update last known value
    
                #update new coordinates
                coord['X'] = derniere_position['X']
                coord['Y'] = derniere_position['Y']
                coord['Z'] = derniere_position['Z']
                
                #removed try/except since i puted the pop contition line 31-ish
                time_and_acc = l[1].split(",")
                time += float(time_and_acc[0][7:])
                acc = int(time_and_acc[1])
                
                coord['T'] = time
                coord['A'] = acc

                coordonnees_time.append(coord)
                    
    #write all coordinates in the order in a csv file
    with open(fichier_csv, 'w', newline='') as csvfile:
        champs = ['X', 'Y', 'Z', 'T', 'A']
        writer = csv.DictWriter(csvfile, fieldnames=champs)

        writer.writeheader()
        for coord in coordonnees_time:
            writer.writerow(coord)

#uncomment if debug is needed or to test ----------
#fichier_gcode = 'out.gcode'
#fichier_csv = 'custom2.csv'
#gcode_into_csv(fichier_gcode, fichier_csv)
