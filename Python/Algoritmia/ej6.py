print("Descuento del 10% por compras mayores de $100.000 ")
valor_de_compra= int(input("Ingresa el valor de compra: "))
descuento= (valor_de_compra * 10) / 100
valor_con_descuento= valor_de_compra - descuento
if valor_de_compra > 100000:
    print("El valor a pagar con su descuento es:" , valor_con_descuento)
else:
    print("No aplica descuento: ", valor_de_compra)