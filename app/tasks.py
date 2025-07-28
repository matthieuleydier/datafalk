# app/tasks.py
from rembg import remove

def process_image(input_path: str, output_path: str):
    with open(input_path, "rb") as i:
        input_data = i.read()
    output_data = remove(input_data)
    with open(output_path, "wb") as o:
        o.write(output_data)

