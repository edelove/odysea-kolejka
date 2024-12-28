import os

def load_players_from_custom_format(players_file):
    players_dict = {}
    current_key = None

    with open(players_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if line.startswith("{") or line.startswith("}"):
                # Ignoruj otwarcie i zamknięcie nawiasów
                continue

            if ":" in line:
                # Klucz i wartość
                key, value = line.split(":", 1)
                key = key.strip().strip("'")
                value = value.strip().strip("[],").replace("'", "").split(", ")
                players_dict[key] = value
            else:
                print(f"Niepoprawna linia w players.txt: {line}")

    return players_dict


def generate_titan_report(titans_file, players_file, pai_file, output_file):
    # Wczytaj listę tytanów
    with open(titans_file, 'r', encoding='utf-8') as file:
        titans_list = [line.strip() for line in file]

    # Wczytaj mapowanie aliasów i postaci
    player_aliases = load_players_from_custom_format(players_file)

    # Wczytaj dane PAI
    with open(pai_file, 'r', encoding='utf-8') as file:
        pai_data = {
            alias.strip("'"): int(pai)
            for alias, pai in (line.split(":") for line in file)
        }

    report = []

    # Generuj raport dla każdego tytana
    for titan in titans_list:
        titan_dir = titan
        summed_file = os.path.join(titan_dir, f"{titan}_summed.txt")
        count_file = os.path.join(titan_dir, f"{titan}_count.txt")

        if not os.path.exists(summed_file) or not os.path.exists(count_file):
            print(f"Missing files for titan: {titan}")
            continue

        # Wczytaj dane aktywności
        with open(summed_file, 'r', encoding='utf-8') as file:
            activity_data = {
                line.split(":")[0].strip(): int(line.split(":")[1].strip())
                for line in file
            }

        # Wczytaj dane ilości bić
        with open(count_file, 'r', encoding='utf-8') as file:
            battle_counts = {
                line.split(":")[0].strip("'"): int(line.split(":")[1].strip())
                for line in file
            }

        # Generuj tabelę dla tytana
        report.append(f"### {titan} ###")
        report.append(f"{'Alias gracza':15} | {'Nick postaci':25} | {'Ilość bić':10} | {'Aktywność':10} | {'PAI':5}")
        report.append("-" * 80)

        for nick, battles in battle_counts.items():
            activity = activity_data.get(nick, 0)
            alias = next(
                (alias for alias, nicks in player_aliases.items() if nick in nicks),
                "Nieznany"
            )
            if alias == "Nieznany":
                print(f"Nieznany alias dla postaci: {nick}")
            pai = pai_data.get(alias, 0)

            # Formatowanie wierszy
            report.append(
                f"{alias:15} | {nick:25} | {battles:10} | {activity:10} | {pai:5}"
            )

        report.append("")  # Dodaj pustą linię między tabelami

    # Zapisz raport do pliku
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(report))

    print(f"Raport zapisano w pliku {output_file}")


# Ścieżki do plików
titans_file = "titans.txt"
players_file = "players.txt"
pai_file = "PAI_per_player.txt"
output_file = "titan_report.txt"

# Wygeneruj raport i zapisz do pliku
generate_titan_report(titans_file, players_file, pai_file, output_file)
