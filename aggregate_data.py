import os
import json
from collections import defaultdict


# Funkcja do załadowania aliasów z pliku, poprawiając format
def load_aliases(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()  # Wczytaj całą zawartość pliku
        content = content.replace("'", '"')  # Zastąp pojedyncze cudzysłowy podwójnymi
        aliases = json.loads(content)  # Teraz możemy załadować poprawiony JSON
    return aliases


# Funkcja do obliczenia PAI
def calculate_pai(root_directory, aliases, titan_list):
    alias_activity = defaultdict(lambda: {"total_activity": 0, "count": 0})
    character_titans = defaultdict(set)  # Słownik do przechowywania, które tytany miały już tę postać

    # Przetwarzanie folderów dla każdego tytana
    for titan in titan_list:
        folder_path = os.path.join(root_directory, titan)
        summed_file = os.path.join(folder_path, f"{titan}_summed.txt")

        print(f"Processing {summed_file}")  # Sprawdzamy, czy pliki są prawidłowo przetwarzane

        # Wczytaj dane z pliku {nazwa_tytana}_summed
        try:
            with open(summed_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Teraz przetwarzamy dane w formacie: postać: liczba
                    line = line.strip()
                    if ':' in line:
                        character, activity = line.split(":", 1)  # Podzielamy na postać i aktywność
                        character = character.strip()
                        activity = int(activity.strip())  # Usuwamy zbędne spacje i konwertujemy na int

                        #print(f"Found character: {character} with activity: {activity}")

                        # Sprawdzamy, czy postać znajduje się w słowniku aliasów
                        found_alias = None
                        for alias, characters in aliases.items():
                            if character in characters:
                                found_alias = alias
                                break

                        if found_alias:
                            #print(f"Mapping character {character} to alias {found_alias}")

                            # Śledzenie, na jakim tytanie pojawiła się postać
                            if titan not in character_titans[character]:
                                character_titans[character].add(titan)

                            # Dodajemy aktywność do aliasu
                            alias_activity[found_alias]["total_activity"] += activity

                            # Sprawdzamy, czy postać pojawiła się na więcej niż jednym wymaganym tytanie
                            if len(character_titans[character]) > 1:
                                alias_activity[found_alias]["count"] += 1
                            else:
                                alias_activity[found_alias]["count"] += 1
                        else:
                            print(f"Character {character} not found in aliases.")
        except FileNotFoundError:
            print(f"File {summed_file} not found. Skipping this titan.")

    # Oblicz PAI dla każdego aliasu
    result = {}
    for alias, data in alias_activity.items():
            result[alias] = data["total_activity"]

    return result


# Ścieżka do pliku ze słownikiem aliasów (players.txt)
players_file = "players.txt"

with open("titans.txt","r",encoding="utf8") as titans_file:
    titan_names = []
    for entry in titans_file:
        titan_names.append(entry.replace('\n', ''))

# Ścieżka do głównego katalogu
root_dir = "."

# Wczytaj aliasy
aliases = load_aliases(players_file)

# Oblicz PAI
pai_results = calculate_pai(root_dir, aliases, titan_names)

# Wyświetl wyniki
sorted_pai_results = sorted(pai_results.items(), key=lambda x: x[1], reverse=True)

with open("PAI_per_player.txt", mode="w", newline='', encoding="utf-8") as pai_file:
    for player, PAI in sorted_pai_results:
        pai_file.write(f"'{player}': {PAI}\n")

#for alias, pai in sorted_pai_results:
#     print(f"{alias}: PAI = {pai:.2f}")