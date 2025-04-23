# Actividad 8

### Ejercicio 1: Método para vaciar el carrito
Objetivo: Implementa en la clase Carrito un método llamado vaciar() que elimine todos los items del carrito. Luego, escribe pruebas siguiendo el patrón AAA para verificar que, al vaciar el carrito, la lista de items quede vacía y el total sea 0.

```
    def vaciar(self):
        """
        Vacía el carrito.
        """
        self.items = []
```
```
def test_vaciar_carrito():

    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Laptop", precio=1000.00)
    producto2 = ProductoFactory(nombre="Mouse", precio=50.00)
    producto3 = ProductoFactory(nombre="Teclado", precio=75.00)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=2) 
    carrito.agregar_producto(producto3, cantidad=3)

    # Act
    carrito.vaciar_carrito()

    
    # Assert
    lista = carrito.obtener_items()
    assert lista == []
    assert len(lista) == 0
```

### Ejercicio 2: Descuento por compra mínima
Objetivo: Amplía la lógica del carrito para aplicar un descuento solo si el total supera un monto determinado. Por ejemplo, si el total es mayor a $500, se aplica un 15% de descuento.

```
    def aplicar_descuento_condicional(self, porcentaje, minimo):
        """
        Aplica un descuento condicional al total del carrito.
        """
        if self.calcular_total() >= minimo:
            return self.aplicar_descuento(porcentaje)
        return self.calcular_total()
```
```
def test_descuento_condicional():
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Laptop", precio=1000.00)
    producto2 = ProductoFactory(nombre="Mouse", precio=50.00)
    producto3 = ProductoFactory(nombre="Teclado", precio=75.00)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=2) 
    carrito.agregar_producto(producto3, cantidad=3)

    # Act
    carrito.aplicar_descuento_condicional(0.15, 500)

    # Assert
    assert carrito.calcular_total() == 0.85 * (1000 + 2 * 50 + 3 * 75)
```
### Ejercicio 3: Manejo de stock en producto
Objetivo: Modifica la clase Producto para que incluya un atributo stock (cantidad disponible). Luego, actualiza el método agregar_producto en Carrito para que verifique que no se agregue una cantidad mayor a la disponible en stock. Si se intenta agregar más, se debe lanzar una excepción.

```
def agregar_producto(self, producto, cantidad=1):
        """
        Agrega un producto al carrito. Si el producto ya existe, incrementa la cantidad.
        """
        if cantidad > producto.stock:
            raise ValueError("No hay suficiente stock disponible")
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                if cantidad + item.cantidad > producto.stock:
                    item.cantidad += cantidad
                    return
                else:
                    raise ValueError("No hay suficiente stock disponible")

        self.items.append(ItemCarrito(producto, cantidad))
```
```
def test_agregar_producto_en_stock():

    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Laptop", precio=250.00)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto1, cantidad=5)

```

### Actividad 4: Ordenar items del carrito
Objetivo: Agrega un método en Carrito que devuelva la lista de items ordenados por un criterio (por ejemplo, por precio unitario o por nombre del producto).

```

```

```
def test_ordenar_lista_de_producto_criterio_definido():
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Laptop", precio=1000.00)
    producto2 = ProductoFactory(nombre="Mouse", precio=50.00)
    producto3 = ProductoFactory(nombre="Teclado", precio=75.00)

    # Act
    listByPrice = carrito.obtener_items_ordenados('precio')
    listByName = carrito.obtener_items_ordenados('nombre')

    # Assert
    assert [items.producto.price for items in listByName] == [50, 75, 1000]
    assert [items.producto.nombre for items in listByName] == ['Laptop', 'Mouse', 'Teclado']
```