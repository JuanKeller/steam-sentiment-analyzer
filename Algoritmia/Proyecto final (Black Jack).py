import random

print("=================================")
print("  Bienvenido al Blackjack! (21)  ")
print("=================================")

# --- Reparto inicial de cartas ---
# El jugador empieza con 2 cartas aleatorias entre 1 y 11
carta1_jugador = random.randint(1, 11)
carta2_jugador = random.randint(1, 11)
puntos_jugador = carta1_jugador + carta2_jugador

# La casa tambien empieza con 2 cartas
carta1_casa = random.randint(1, 11)
carta2_casa = random.randint(1, 11)
puntos_casa = carta1_casa + carta2_casa

# Mostrar las cartas iniciales del jugador
print("\nTus cartas iniciales son:", carta1_jugador, "y", carta2_jugador)
print("Tu puntuacion es:", puntos_jugador)

# Solo le mostramos UNA carta de la casa (como en el juego real)
print("\nLa casa tiene una carta visible:", carta1_casa)

# =============================================
# TURNO DEL JUGADOR
# El jugador puede pedir cartas o plantarse
# =============================================

# Esta variable controla si el jugador sigue jugando
jugador_activo = True

while jugador_activo:

    # Si el jugador ya tiene 21, no necesita pedir mas
    if puntos_jugador == 21:
        print("\n¡Tienes exactamente 21! No puedes pedir mas.")
        jugador_activo = False

    else:
        # Le preguntamos que quiere hacer
        print("\n¿Que quieres hacer?")
        print("  1 - Pedir carta")
        print("  2 - Plantarse")

        # Usamos try/except para que no explote si el usuario escribe algo raro
        try:
            opcion = int(input("Elige una opcion (1 o 2): "))

            if opcion == 1:
                # El jugador pide una carta nueva
                carta_nueva = random.randint(1, 11)
                puntos_jugador = puntos_jugador + carta_nueva
                print("\nTe dieron un:", carta_nueva)
                print("Tu puntuacion ahora es:", puntos_jugador)

                # Revisamos si el jugador se paso de 21
                if puntos_jugador > 21:
                    print("\n¡Te pasaste de 21! Perdiste esta mano.")
                    jugador_activo = False

            elif opcion == 2:
                # El jugador se planta, termina su turno
                print("\nDecidiste plantarte con", puntos_jugador, "puntos.")
                jugador_activo = False

            else:
                # Si escribe un numero pero no es 1 ni 2
                print("Eso no es valido, escribe 1 o 2 nomas.")

        except:
            # Si escribe letras o algo que no sea numero
            print("Oops! Eso no es un numero. Intenta de nuevo.")

# =============================================
# TURNO DE LA CASA (solo si el jugador no se paso)
# La casa pide cartas hasta llegar a 17 o mas
# =============================================

# Solo juega la casa si el jugador no perdio
if puntos_jugador <= 21:
    print("\n--- Turno de la Casa ---")
    print("La casa tenia:", carta1_casa, "y", carta2_casa)
    print("Puntuacion de la casa:", puntos_casa)

    # La casa sigue pidiendo mientras tenga menos de 17
    while puntos_casa < 17:
        carta_casa_nueva = random.randint(1, 11)
        puntos_casa = puntos_casa + carta_casa_nueva
        print("La casa pide una carta:", carta_casa_nueva)
        print("Puntuacion de la casa ahora:", puntos_casa)

    # Avisamos si la casa se paso
    if puntos_casa > 21:
        print("\nLa casa se paso de 21!")

# =============================================
# RESULTADO FINAL
# Comparamos puntuaciones con if/elif/else
# =============================================

print("\n=================================")
print("         RESULTADO FINAL         ")
print("=================================")
print("Tu puntuacion:       ", puntos_jugador)
print("Puntuacion de la casa:", puntos_casa)
print("---------------------------------")

# Primero revisamos si el jugador ya perdio por pasarse
if puntos_jugador > 21:
    print("Resultado: PERDISTE (te pasaste de 21)")

# Si la casa se paso, el jugador gana automatico
elif puntos_casa > 21:
    print("Resultado: GANASTE (la casa se paso de 21!)")

# Si ninguno se paso, comparamos puntos normalmente
elif puntos_jugador > puntos_casa:
    print("Resultado: GANASTE! Felicidades :)")

elif puntos_jugador < puntos_casa:
    print("Resultado: PERDISTE, la casa gano esta vez.")

else:
    # Los dos tienen la misma puntuacion
    print("Resultado: EMPATE! Que casualidad.")

print("=================================")
print("       Gracias por jugar!        ")
print("=================================")