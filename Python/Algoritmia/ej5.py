print("Ingresa tres notas para dar el promedio: ")
nota1= int(input("Ingresa nota_1"))
nota2= int(input("Ingresa nota_2"))
nota3= int(input("Ingresa nota_3"))
promedio= (nota1 + nota2 + nota3) / 3
print("El promedio es: ", promedio)
if promedio >=3:
    print("Pasa :)", promedio)
else:
    print("No pasa :(")
    