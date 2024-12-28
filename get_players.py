import ast
import os

def load_player_dict(file_path="players.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()  # Odczytujemy całą zawartość pliku
        return ast.literal_eval(file_content)

def get_player_list_per_titan(titans_file_path):
    # Wczytanie listy tytanów z pliku
    with open(titans_file_path, "r", encoding="utf8") as titans_file:
        titans_list = [line.strip() for line in titans_file if line.strip()]

    # Iterowanie po każdym tytanie
    for titan_name in titans_list:
        titan_folder = os.path.join(os.getcwd(), titan_name)  # Folder tytana w bieżącym katalogu
        if not os.path.exists(titan_folder):
            print(f"Titan folder '{titan_name}' does not exist!")
            continue

        # Pobranie listy folderów (graczy) w katalogu tytana
        players = [
            entry for entry in os.listdir(titan_folder)
            if os.path.isdir(os.path.join(titan_folder, entry))
        ]

        # Wyświetlenie wyników w konsoli
        print(f"=== {titan_name} ===")
        for player in sorted(players):
            print(player)
        print("\n")  # Dodatkowa linia dla czytelności

    # Ścieżka do pliku z listą tytanów

#Get characters per titan
titans_file_path = "titans.txt"
get_player_list_per_titan(titans_file_path)

#Get all Clan Members
#my_dict = load_player_dict()
#for key in my_dict:
    #print(key)