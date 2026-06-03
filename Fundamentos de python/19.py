sensor = {
    "Id": "5.01",
    "Tipo": "Temperatura",
    "Valor": 28.5,
    "Unidad": "C"
}
print("sensor:", sensor["Id"], ",", sensor["Tipo"])
sensor["Valor"] = 29.1
print("Lectura actualizada: ", sensor["Valor"], sensor["Unidad"])
