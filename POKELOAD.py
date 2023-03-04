from pprint import pprint

from requests_html import HTMLSession
import pickle




pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": [],
    "current_exp": 0,
    "attacks": [],
    "attack_type": []
}


URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="



def get_pokemon(index):
    session = HTMLSession()
    url = "{}{}".format(URL_BASE, index)
    pokemon_page = session.get(url)
    new_pokemon = pokemon_base.copy()

    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text
    new_pokemon["type"] = []

    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])

    new_pokemon["attacks"] = []

    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        attack = {
            "name": attack_item.find("td", first=True). find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img",first=True).attrs["alt"],
            "min level": attack_item.find("th", first=True).text,
            "damage": int(attack_item.find("td")[3].text.replace("--", "0"))
        }
        new_pokemon["attacks"].append(attack)

    return new_pokemon


def get_all_pokemons():
    try:
        print("Cargando el archivo de Pokemon...")
        with open("pokefile.pkl", "rb") as pokefile:
            all_pokemons = pickle.load(pokefile)

    except FileNotFoundError:
        print("Archivo no encontrado. Cargando de internet")
        all_pokemons = []
        for index in range(151):
            all_pokemons.append(get_pokemon(index + 1))
            print("*", end="")

        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)
        print("\nTodos los Pokemon han sido descargados")

    print("Lista de Pokemon encontrados")
    return all_pokemons


def main():
    pprint(get_all_pokemons())



if __name__ == "__main__":
    main()
