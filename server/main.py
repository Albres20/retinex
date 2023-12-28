from fastapi import FastAPI
from typing import Union
from Clas1 import MiClase     
import renitex
from pydantic import BaseModel

app = FastAPI()

class HexDataInput(BaseModel):
    hex_data: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = "Hello there"):
    objeto = MiClase("David")
    salida=objeto.saludar()
    return {"item_id": item_id, "q": salida}

@app.post("/receiveImg/")
async def convert_to_bytes(input_data: HexDataInput):
    # Convertir la data hexadecimal a bytes
    print("Debuging")
    hex_data=input_data.hex_data
    try:
        byte_data = bytes.fromhex(hex_data)
        renitex.starConversion(byte_data)
        print("Good conversion")

    except ValueError as e:
        print("fail")
        return {"Error": "Formato hexadecimal inválido"}
    
    # Guardar los bytes en un archivo
    file_path = "data_file.bin"
    with open(file_path, "wb") as output_file:
        output_file.write(byte_data)
    
    return {"message": "Data convertida y guardada como archivo binario", "saved_path": file_path}
