from fastapi import FastAPI
from typing import Union
from Clas1 import MiClase     

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = "Hello there"):
    objeto = MiClase("David")
    salida=objeto.saludar()
    return {"item_id": item_id, "q": salida}

@app.post("/receiveImg/")
async def convert_to_bytes(hex_data: str):
    # Convertir la data hexadecimal a bytes
    try:
        byte_data = bytes.fromhex(hex_data)
    except ValueError as e:
        return {"Error": "Formato hexadecimal inválido"}
    
    # Guardar los bytes en un archivo
    file_path = "uploads/data_file.bin"
    with open(file_path, "wb") as output_file:
        output_file.write(byte_data)
    
    return {"message": "Data convertida y guardada como archivo binario", "saved_path": file_path}
