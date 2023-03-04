import random
from POKELOAD import get_all_pokemons


def get_player_profile(pokemon_list):
    return {
        "player_name" : input("¿Cuál es tu nombre?"),
        "pokemon_inventory" : [random.choice(pokemon_list) for a in range(3)],
        "combats" : 0,
        "pokeballs" : 0,
        "health_potion" : 0
    }



def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0



def get_pokemon_info(pokemon):
    return "{} | lvl{} | health {}/{}".format(pokemon["name"],
                                              pokemon["level"],
                                              pokemon["current_health"],
                                              pokemon["base_health"])




def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        print("Elige con qué Pokemon lucharás")
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
            return player_profile["pokemon_inventory"][int(input("¿Cuál eliges?"))]
        except (ValueError, IndexError):
            print("Elección inválida")


def player_attack(player_pokemon, enemy_pokemon):
    #IMPLEMENTAR MULTIPLICADORES DE ATAQUE POR EL TIPO
    pass


def enemy_attack(player_pokemon, enemy_pokemon):
    pass


def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1,5)
        pokemon["current_exp"] += points

    while pokemon["current_exp"] >= 20:
        pokemon["current_exp"] -= 20
        pokemon["level"] += 1
        pokemon["current_health"] = pokemon["base_health"]
        print("Tu pokemon ha subido al nivel {}".format(get_pokemon_info(pokemon)))


def capture_with_pokeball(player_profile, enemy_pokemon):
    pass



def cure_pokemon(player_profile, player_pokemon):
    pass



def fight(player_profile, enemy_pokemon):
    print("NUEVO COMBATE")

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    print("Contrincantes: {} VS {}".format(get_pokemon_info(player_pokemon),
                                           get_pokemon_info(enemy_pokemon)))
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = None
        while action not in ["A", "P", "V", "C"]:
            action = input("¿Qué deseas hacer? [A]tacar, [P]okeball, Poción de [V]ida, [C]ambiar de Pokemon")

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            attack_history.append(player_pokemon)
        elif action == "P":
            #SI EL USUARIO TIENE POKEBALLS EN EL INVENTARIO, SE TIRA UNA. HAY PROBABILIDAD DE CAPTURARLO RELATIVA A LA SALUD RESTANTE
            #CUANDO SE CAPTURA, PASA A ESTAR EN EL INVENTARIO CON LA MISMA SALUD QUE TENIA
            capture_with_pokeball(player_profile, enemy_pokemon)
        elif action == "V":
            #SI EL USUARIO TIENE CURAS EN EL INVENTARIO, SE APLICA, CURA 50 DE VIDA HASTA LLEGAR A 50
            #SI NO TIENE CURAS, NO SE CURA
            cure_pokemon(player_profile, player_pokemon)
        elif action == "C":
            player_pokemon = choose_pokemon(player_profile)

        enemy_attack(enemy_pokemon, player_pokemon)

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            player_pokemon = choose_pokemon(player_profile)

    if enemy_pokemon["current_health"] == 0:
        print("¡Has ganado!")
        assign_experience(attack_history)

    print("FIN DEL COMBATE")
    input("Presiona ENTER para continuar")


def item_lottery(player_profile):



def main():
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        item_lottery(player_profile)

    print("Has perdido en el combate numero {}".format(player_profile["combats"]))



if __name__ == "__main__":
    main()
