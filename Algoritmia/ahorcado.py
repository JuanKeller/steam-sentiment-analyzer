
palabra_secreta = "computador"

progreso = []
for letra in palabra_secreta:
    progreso.append("_")

vidas = 6
letras_usadas = []

print("=============================")
print("   BIENVENIDO AL AHORCADO    ")
print("=============================")
print("La palabra tiene", len(palabra_secreta), "letras.")
print("Tienes", vidas, "vidas. ¡Buena suerte!")
print()


while vidas > 0:

    print("Palabra:", " ".join(progreso))
    print("Vidas restantes:", vidas)
    print("Letras usadas:", letras_usadas)
    print()

    letra_valida = False
    while letra_valida == False:
        try:
            entrada = input("Ingresa una letra: ")

            if len(entrada) != 1:
                print("⚠️  Por favor ingresa solo UNA letra.")
            elif entrada.isdigit():
                print("⚠️  Eso es un numero, no una letra.")
            elif entrada in letras_usadas:
                print("⚠️  Ya usaste esa letra, intenta con otra.")
            else:
                letra_valida = True

        except:
            print("⚠️  Algo raro paso, intenta de nuevo.")

    entrada = entrada.lower()
    letras_usadas.append(entrada)

    if entrada in palabra_secreta:
        print("✅ ¡Bien! La letra '", entrada, "' esta en la palabra.")

        posicion = 0
        while posicion < len(palabra_secreta):
            if palabra_secreta[posicion] == entrada:
                progreso[posicion] = entrada
            posicion = posicion + 1

    else:
        vidas = vidas - 1
        print("❌ La letra '", entrada, "' NO esta en la palabra.")
        print("Perdiste una vida. Te quedan:", vidas)

    print("-----------------------------")

    if "_" not in progreso:
        print()
        print("🎉 ¡¡GANASTE!!")
        print("La palabra era:", palabra_secreta)
        print("La adivinaste con", vidas, "vidas de sobra. ¡Excelente!")
        vidas = -1  

if vidas == 0:
    print()
    print("💀 ¡PERDISTE! Se acabaron tus vidas.")
    print("La palabra secreta era:", palabra_secreta)
    print("¡La proxima vez lo lograras!")