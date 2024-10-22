import csv

# Set power levels
POWER_ACCEL_X = 0.12*230    #need update
POWER_ACCEL_Y = 0.16*230    #need update
POWER_ACCEL_Z = 0.16*230    #need update
POWER_SPEED_X = [0.1*230]   #need update
POWER_SPEED_Y = [0.15*230]  #need update
POWER_SPEED_Z = [0.15*230]  #need update
POWER_BED_NOZ = 0.431*230   #Confirmed experimental Value
POWER_PLUGGED = 0.169*230   #Confirmed experimental Value
POWER_BRAKE = 0.0


def calculer_energie(time, is_acc, speed_lvl, dx, dy, dz):
    """
    calculates energie of line considering direction, acceleration and speed

    """
    pwr_accel = 0
    pwr_speed = 0
    if dz == 0 and (dx+dy) != 0:
        pwr_speed = POWER_SPEED_X[speed_lvl] * (dx/(dx+dy)) + POWER_SPEED_Y[speed_lvl] * (dy/(dx+dy))
        if is_acc == 1:
            pwr_accel = POWER_ACCEL_X * (dx/(dx+dy)) + POWER_ACCEL_Y * (dy/(dx+dy))
            
    elif dz != 0:
        pwr_speed = POWER_SPEED_Z[speed_lvl]
        if is_acc == 1:
            pwr_accel = POWER_ACCEL_Z
    energie = time * (POWER_PLUGGED + POWER_BED_NOZ + pwr_speed + pwr_accel)
    return energie 

def add_nrg_comsumption(in_file, out_file):
    last_x = 0
    last_y = 0
    last_z = 0
    last_t = 0
    with open(in_file, mode='r', newline='') as in_csvfile:
        lecteur_csv = csv.reader(in_csvfile)
        en_tete = next(lecteur_csv)  # Read head
        nrg_lines = []

        # Add head columns
        head = en_tete[:4]
        head.append('J')
        head.append('I')
        nrg_lines.append(head)

        # Read each ligne and calculates energy/current consumption
        for line in lecteur_csv:
            x = float(line[0])
            y = float(line[1])
            z = float(line[2])
            t = float(line[3])  # Total time
            a = int(line[4])    # Acceleration (can be -1, 0, or 1)
            
            #calculate orthogonals distances
            dx = abs(x-last_x); dy = abs(y-last_y); dz = abs(z-last_z); dt = t-last_t
            last_x = x        ; last_y = y        ; last_z = z        ; last_t = t
            
            # Calculate energie for csvline
            energie = calculer_energie(dt, a, 0, dx, dy, dz)

            # Add nrg and current to the line
            new_line = line[:4]
            new_line.append(energie)
            if dt !=0:
                i=energie/(230*dt)
            else :
                i=0
            new_line.append(i)
            nrg_lines.append(new_line)
            
            
    # Write everything in a new csv file
    with open(out_file, mode='w', newline='') as out_csvfile:
        write_csv = csv.writer(out_csvfile)
        write_csv.writerows(nrg_lines)

# Example of script use ----------
#fichier_entree = 'custom2.csv'  # Remplacer par le nom de votre fichier CSV
#fichier_sortie = 'custom_energy2.csv'  # Le fichier CSV avec la consommation d'énergie
#add_nrg_comsumption(fichier_entree, fichier_sortie)
