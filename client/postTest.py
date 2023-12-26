import requests

def byteToArray(ruta:str):
    with open("dogLow.png", "rb") as image:
        f = image.read()
        b = bytearray(f)
        #print("arraybytes: "+str(b))
        return b
        


bytes=byteToArray("dogLow.PNG")
hexadecimal=bytes.hex()
#print("Hexadecimal: "+str(hexadecimal))


# Datos hexadecimales que quieres enviar
hex_data = hexadecimal

# URL del endpoint al que quieres enviar los datos
url = "http://127.0.0.1:8000/receiveImg/"

# Payload con los datos hexadecimales
payload = {"hex_data": hex_data}

# Realizar la solicitud POST
response = requests.post(url, json=payload)
print("Response"+str(response))


