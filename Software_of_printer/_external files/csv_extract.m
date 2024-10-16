function coordonnees = csv_extract(fichier_csv)
    % Cette fonction lit un fichier CSV et renvoie un vecteur contenant
    % les coordonnées spatiales X, Y, Z pour chaque ligne.

    % Lire le fichier CSV
    data = readtable(fichier_csv);

    % Extraire les colonnes X, Y, Z
    X = data{:, 1};  % Première colonne (X)
    Y = data{:, 2};  % Deuxième colonne (Y)
    Z = data{:, 3};  % Troisième colonne (Z)

    % Combiner les coordonnées dans un vecteur de sortie
    coordonnees = [X, Y, Z];  % Chaque ligne du vecteur contient [X, Y, Z]
end
