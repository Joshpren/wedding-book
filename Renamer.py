import os


def clean_filename(filename):
    # Verbotene Zeichen und ihre Ersetzungen
    forbidden_chars = {':': '-', ' ': '_'}

    # Durchlaufe die verbotenen Zeichen und ersetze sie im Dateinamen
    for char, replacement in forbidden_chars.items():
        filename = filename.replace(char, replacement)

    return filename


def process_files(directory):
    # Erhalte eine Liste aller Dateien im angegebenen Verzeichnis
    files = os.listdir(directory)

    # Durchlaufe alle Dateien im Verzeichnis
    for file in files:
        # Baue den vollständigen Pfad zur Datei
        file_path = os.path.join(directory, file)

        # Überprüfe, ob es sich um eine Datei handelt (kein Verzeichnis)
        if os.path.isfile(file_path):
            # Bereinige den Dateinamen
            new_filename = clean_filename(file)

            # Baue den vollständigen Pfad zum neuen Dateinamen
            new_file_path = os.path.join(directory, new_filename)

            # Benenne die Datei um
            os.rename(file_path, new_file_path)

            # Gib eine Meldung aus
            print(f"Datei umbenannt: {file} -> {new_filename}")


if __name__ == "__main__":
    # Passe den Pfad zum gewünschten Verzeichnis an
    target_directory =input("Which directory?")
    if target_directory == None:
        target_directory = "resources/target"

    if os.path.exists(target_directory):
        # Verarbeite die Dateien im Verzeichnis
        process_files(target_directory)
    else:
        print(f"No directory \"{target_directory}\" has been found")
