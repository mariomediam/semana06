from faker import Faker
fake = Faker()

def fake_products(cantidad):
    UNIDADES_MEDIDA = ["UN", "DOC", "CI", "MI"]
    for id in range(0, cantidad):
        nombre = "Producto 0" + str(id)
        precio = float(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=1, max_value=150))
        unidad_medida = UNIDADES_MEDIDA[fake.random_int(min=0, max=3)]
        print("INSERT INTO productos (nombre, precio, unidad_medida, estado) VALUES ('%s', %s, '%s', true);"% (nombre, precio, unidad_medida))

fake_products(100)