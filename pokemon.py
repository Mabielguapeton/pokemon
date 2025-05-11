import random 
import time

class Movimiento:
    def __init__(self, nombre, tipo, poder, precision=100, pp=15, es_buff=False, turnos_recarga=0):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder
        self.precision = precision
        self.pp = pp
        self.es_buff = es_buff
        self.turnos_recarga = turnos_recarga
        self.turnos_restantes = 0

class Pokemon:
    def __init__(self, nombre, tipo, nivel, hp, ataque, defensa, velocidad, habilidad=None):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp_max = hp
        self.hp_actual = hp
        self.ataque_base = ataque
        self.ataque = ataque
        self.defensa_base = defensa
        self.defensa = defensa
        self.velocidad = velocidad
        self.movimientos = []
        self.habilidad = habilidad
        self.turno_actual = 0
        self.ultimo_movimiento = None

    def agregar_movimiento(self, movimiento):
        if len(self.movimientos) < 5:
            self.movimientos.append(movimiento)

    def usar_habilidad(self):
        if self.habilidad == "Regeneracion":
            curacion = int(self.hp_max * 0.05)
            self.hp_actual = min(self.hp_max, self.hp_actual + curacion)
            print(f"{self.nombre} usó Regeneracion y recuperó {curacion} HP!")
        elif self.habilidad == "Ataque Plus":
            self.ataque = int(self.ataque_base * 1.5)
            print(f"{self.nombre} aumentó su ataque!")
        elif self.habilidad == "Defensa Plus":
            self.defensa = int(self.defensa_base * 1.5)
            print(f"{self.nombre} aumentó su defensa!")

def crear_movimientos():
    movimientos = {
        "normal": [
            Movimiento("Placaje", "normal", 80, turnos_recarga=1),
            Movimiento("Arañazo", "normal", 80, turnos_recarga=1),
            Movimiento("Golpe Cabeza", "normal", 80, turnos_recarga=1)
        ],
        "especial": {
            "fuego": Movimiento("Llamarada", "fuego", 150, turnos_recarga=2),
            "agua": Movimiento("Hidrobomba", "agua", 150, turnos_recarga=2),
            "tierra": Movimiento("Terremoto", "tierra", 150, turnos_recarga=2),
            "oscuridad": Movimiento("Golpe Umbrío", "oscuridad", 150, turnos_recarga=2),
            "luz": Movimiento("Destello Final", "luz", 160, turnos_recarga=2),
            "basico": Movimiento("Golpe Definitivo", "basico", 170, turnos_recarga=2)
        },
        "buff": {
            "ataque": Movimiento("Fuerza Bruta", "normal", 0, es_buff=True, turnos_recarga=1),
            "defensa": Movimiento("Escudo Protector", "normal", 0, es_buff=True, turnos_recarga=1)
        }
    }
    return movimientos

def crear_pokemons(movimientos):
    
    pokemons = [
        Pokemon("Charmander", "fuego", 10, 1500, 85, 50, 70, "Ataque Plus"),
        Pokemon("Squirt", "agua", 10, 1500, 70, 90, 30, "Defensa Plus"),
        Pokemon("Frekni", "tierra", 10, 1500, 90, 80, 25),
        Pokemon("Negas", "oscuridad", 10, 1500, 80, 50, 80, "Ataque Plus"),
        Pokemon("Arthur Morgan", "luz", 10, 1500, 80, 75, 60),
        Pokemon("Guardián", "basico", 10, 1500, 85, 80, 50, "Regeneracion")
    ]
    
    for pokemon in pokemons:
        for movimiento in movimientos["normal"]:
            pokemon.agregar_movimiento(movimiento)
        pokemon.agregar_movimiento(movimientos["especial"][pokemon.tipo])
        if pokemon.habilidad in ["Ataque Plus", "Defensa Plus"]:
            tipo_buff = "ataque" if pokemon.habilidad == "Ataque Plus" else "defensa"
            pokemon.agregar_movimiento(movimientos["buff"][tipo_buff])
    
    return pokemons

def mostrar_barra_vida(pokemon):
    porcentaje = (pokemon.hp_actual / pokemon.hp_max) * 100
    barras = int(porcentaje / 5)
    print(f"{pokemon.nombre}: [{'=' * barras}{' ' * (20 - barras)}] {pokemon.hp_actual}/{pokemon.hp_max} HP")

def mostrar_texto(texto, delay=0.03):
    for letra in texto:
        print(letra, end='', flush=True)
        time.sleep(delay)
    print()

def elegir_pokemon(pokemons_disponibles):
    print("\nElige tu Pokémon:")
    for i, pokemon in enumerate(pokemons_disponibles, 1):
        print(f"{i}. {pokemon.nombre} ({pokemon.tipo}) - HP: {pokemon.hp_max} - Ataque: {pokemon.ataque} - Defensa: {pokemon.defensa}")
    
    while True:
        try:
            eleccion = int(input("Opción: ")) - 1
            if 0 <= eleccion < len(pokemons_disponibles):
                return pokemons_disponibles[eleccion]
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número.")

def elegir_rival(pokemons_disponibles, jugador):
    print("\nElige el Pokémon rival:")
    for i, pokemon in enumerate(pokemons_disponibles, 1):
        if pokemon != jugador:
            print(f"{i}. {pokemon.nombre} ({pokemon.tipo}) - HP: {pokemon.hp_max} - Ataque: {pokemon.ataque} - Defensa: {pokemon.defensa}")
    
    while True:
        try:
            eleccion = int(input("Opción: ")) - 1
            if 0 <= eleccion < len(pokemons_disponibles) and pokemons_disponibles[eleccion] != jugador:
                rival = pokemons_disponibles[eleccion]
                print(f"\n¡Has elegido enfrentarte a {rival.nombre}!")
                return rival
            else:
                print("Opción inválida o no puedes elegir tu propio Pokémon. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número.")

def calcular_daño(atacante, defensor, movimiento):
    ventajas = {
        "fuego": ["tierra"],
        "agua": ["fuego"],
        "tierra": ["agua"],
        "oscuridad": ["basico"],
        "basico": ["luz"],
        "luz": ["oscuridad"]
    }
    multiplicador = 1.5 if defensor.tipo in ventajas.get(movimiento.tipo, []) else 1
    daño = (movimiento.poder * atacante.ataque / defensor.defensa) * multiplicador
    return int(daño)

def aplicar_buff(pokemon, movimiento):
    if movimiento.nombre == "Fuerza Bruta":
        pokemon.ataque = int(pokemon.ataque_base * 1.5)
        print(f"{pokemon.nombre} aumentó su ataque!")
    elif movimiento.nombre == "Escudo Protector":
        pokemon.defensa = int(pokemon.defensa_base * 1.5)
        print(f"{pokemon.nombre} aumentó su defensa!")

def elegir_mejor_movimiento(rival, jugador):
    
    movimientos_disponibles = []
    
    for movimiento in rival.movimientos:
        if movimiento.turnos_restantes <= 0:
            movimientos_disponibles.append(movimiento)
    
    if not movimientos_disponibles:
        print(f"{rival.nombre} está recuperándose!")
        return None
    
    mejor_movimiento = None
    max_daño = 0
    
    for movimiento in movimientos_disponibles:
        if movimiento.es_buff:
            
            if movimiento.nombre == "Fuerza Bruta" and rival.ataque <= rival.ataque_base:
                return movimiento
            
            elif movimiento.nombre == "Escudo Protector" and rival.defensa <= rival.defensa_base:
                return movimiento
        else:
            daño = calcular_daño(rival, jugador, movimiento)
            
            ventajas = {
                "fuego": ["tierra"],
                "agua": ["fuego"],
                "tierra": ["agua"],
                "oscuridad": ["basico"],
                "basico": ["luz"],
                "luz": ["oscuridad"]
            }
            es_super_efectivo = jugador.tipo in ventajas.get(movimiento.tipo, [])
            
            if es_super_efectivo:
                daño *= 1.5
            
            if daño > max_daño:
                max_daño = daño
                mejor_movimiento = movimiento
    
    return mejor_movimiento if mejor_movimiento else random.choice(movimientos_disponibles)

def actualizar_recargas(pokemon):
    for movimiento in pokemon.movimientos:
        if movimiento.turnos_restantes > 0:
            movimiento.turnos_restantes -= 1

def turno_jugador(jugador, rival):
    print("\nTus movimientos disponibles:")
    movimientos_disponibles = []
    
    for i, movimiento in enumerate(jugador.movimientos, 1):
        if movimiento.turnos_restantes <= 0:
            print(f"{i}. {movimiento.nombre} ({movimiento.tipo}) - Poder: {movimiento.poder}")
            movimientos_disponibles.append(movimiento)
        else:
            print(f"{i}. {movimiento.nombre} (Recarga: {movimiento.turnos_restantes} turnos)")
    
    if not movimientos_disponibles:
        print("¡Todos tus movimientos están en recarga! Pierdes este turno.")
        return
    
    while True:
        try:
            opcion = int(input("Elige movimiento: ")) - 1
            if 0 <= opcion < len(jugador.movimientos):
                movimiento = jugador.movimientos[opcion]
                if movimiento in movimientos_disponibles:
                    break
                else:
                    print("Ese movimiento está en recarga. Elige otro.")
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número.")
    
    jugador.ultimo_movimiento = movimiento
    
    if movimiento.es_buff:
        aplicar_buff(jugador, movimiento)
    else:
        daño = calcular_daño(jugador, rival, movimiento)
        rival.hp_actual = max(0, rival.hp_actual - daño)
        print(f"{jugador.nombre} usó {movimiento.nombre}!")
        print(f"¡{rival.nombre} recibió {daño} de daño!")
    
    # Aplicar recarga
    movimiento.turnos_restantes = movimiento.turnos_recarga

def turno_ia(rival, jugador):
    movimiento = elegir_mejor_movimiento(rival, jugador)
    
    if movimiento is None:
        return
    
    rival.ultimo_movimiento = movimiento
    
    if movimiento.es_buff:
        aplicar_buff(rival, movimiento)
    else:
        daño = calcular_daño(rival, jugador, movimiento)
        jugador.hp_actual = max(0, jugador.hp_actual - daño)
        print(f"\n{rival.nombre} usó {movimiento.nombre}!")
        print(f"¡{jugador.nombre} recibió {daño} de daño!")
    
    
    movimiento.turnos_restantes = movimiento.turnos_recarga

def iniciar_batalla(jugador, rival):
    print(f"\n¡Comienza la batalla! {jugador.nombre} vs {rival.nombre}!")
    
    
    jugador.hp_actual = jugador.hp_max
    jugador.ataque = jugador.ataque_base
    jugador.defensa = jugador.defensa_base
    for m in jugador.movimientos:
        m.turnos_restantes = 0
    
    rival.hp_actual = rival.hp_max
    rival.ataque = rival.ataque_base
    rival.defensa = rival.defensa_base
    for m in rival.movimientos:
        m.turnos_restantes = 0
    
    turno = 1
    
    while jugador.hp_actual > 0 and rival.hp_actual > 0:
        print(f"\n--- Turno {turno} ---")
        mostrar_barra_vida(jugador)
        mostrar_barra_vida(rival)
        
        
        actualizar_recargas(jugador)
        actualizar_recargas(rival)
        
        if jugador.velocidad >= rival.velocidad:
            turno_jugador(jugador, rival)
            if rival.hp_actual <= 0:
                break
            turno_ia(rival, jugador)
        else:
            turno_ia(rival, jugador)
            if jugador.hp_actual <= 0:
                break
            turno_jugador(jugador, rival)
        
        
        if jugador.habilidad == "Regeneracion":
            jugador.usar_habilidad()
        if rival.habilidad == "Regeneracion":
            rival.usar_habilidad()
        
        turno += 1
        time.sleep(1)
    
    mostrar_barra_vida(jugador)
    mostrar_barra_vida(rival)
    
    if jugador.hp_actual > 0:
        print(f"\n¡Ganaste! {rival.nombre} se debilitó!")
    else:
        print(f"\n¡Perdiste! {jugador.nombre} se debilitó!")

def menu_principal():
    movimientos = crear_movimientos()
    pokemons_disponibles = crear_pokemons(movimientos)
    
    while True:
        mostrar_texto("\nBienvenido a Poquemon!")
        print("1. Nueva batalla")
        print("2. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            jugador = elegir_pokemon(pokemons_disponibles)
            rival = elegir_rival(pokemons_disponibles, jugador)
            iniciar_batalla(jugador, rival)
            
            while True:
                print("\n¿Qué deseas hacer?")
                print("1. Revancha (mismos Pokémon)")
                print("2. Nueva batalla (elegir Pokémon nuevo)")
                print("3. Volver al menú principal")
                print("4. Salir del juego")
                
                opcion_post = input("Elige una opción: ")
                
                if opcion_post == "1":
                    iniciar_batalla(jugador, rival)
                elif opcion_post == "2":
                    break  
                elif opcion_post == "3":
                    return menu_principal()  
                elif opcion_post == "4":
                    mostrar_texto("¡Gracias por jugar! Hasta la próxima.")
                    exit()
                else:
                    print("Opción inválida. Intenta de nuevo.")
                    
        elif opcion == "2":
            mostrar_texto("¡Gracias por jugar! Hasta la próxima.")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()
