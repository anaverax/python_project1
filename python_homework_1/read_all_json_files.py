import json
import os

def read_json_files():
    team_data = {}
    
    # Alle JSON-Dateien im aktuellen Verzeichnis suchen
    json_files = [f for f in os.listdir() if f.endswith(".json") and "_" in f]
    
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                team_data[file] = data  # Datei als Schlüssel speichern
            except json.JSONDecodeError:
                print(f"Fehler beim Lesen von {file}")
    
    return team_data

def write_combined_json(team_data):
    if not team_data:
        print("Keine gültigen JSON-Dateien gefunden.")
        return
    
    # Namen aus den Dateien extrahieren
    team_names = "_".join([name.split("_")[0] for name in team_data.keys()])
    output_filename = f"team_{team_names}.json"
    
    # Datei im aktuellen Verzeichnis speichern
    output_path = os.path.join(os.getcwd(), output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(team_data, f, indent=4)
    
    print(f"Zusammengeführte JSON-Datei gespeichert als {output_path}")
    print(json.dumps(team_data, indent=4))

if __name__ == "__main__":
    team_data = read_json_files()
    write_combined_json(team_data)
