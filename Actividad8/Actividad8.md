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
```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_carrito.py::test_vaciar_carrito
======================================================= test session starts ========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini  
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_carrito.py .                                                                                                             [100%]

======================================================== 1 passed in 0.55s =========================================================
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
```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_carrito.py::test_descuento_condicional
======================================================= test session starts ========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_carrito.py .                                                                                                             [100%]

======================================================== 1 passed in 0.61s ========================================================= 
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
        carrito.agregar_producto(producto1, cantidad=100)

```
```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_carrito.py::test_agregar_producto_en_stock
======================================================= test session starts ======================================================== 
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_carrito.py .                                                                                                             [100%] 

======================================================== 1 passed in 0.30s ========================================================= 
```

### Actividad 4: Ordenar items del carrito
Objetivo: Agrega un método en Carrito que devuelva la lista de items ordenados por un criterio (por ejemplo, por precio unitario o por nombre del producto).

```
def obtener_items_ordenados(self,criterio:str):
    if criterio not in ['precio', 'nombre']:
        raise ValueError("Criterio inválido. Use 'precio' o 'nombre'")
    if criterio == 'precio':
        return sorted(self.items, key=lambda item: item.producto.precio)
    elif criterio == 'nombre':
        return sorted(self.items, key=lambda item: item.producto.nombre)

```

```
def test_ordenar_lista_de_producto_criterio_definido():
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Laptop", precio=1000.00)
    producto2 = ProductoFactory(nombre="Mouse", precio=50.00)
    producto3 = ProductoFactory(nombre="Teclado", precio=75.00)

    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=1)
    carrito.agregar_producto(producto3, cantidad=1)

    # Act
    listByPrice = carrito.obtener_items_ordenados('precio')
    listByName = carrito.obtener_items_ordenados('nombre')

    # Assert
    assert [items.producto.precio for items in listByPrice] == [50, 75, 1000]
    assert [items.producto.nombre for items in listByName] == ['Laptop', 'Mouse', 'Teclado']
```

```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_carrito.py::test_ordenar_lista_de_producto_criterio_definido
======================================================= test session starts ========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_carrito.py .                                                                                                             [100%]

======================================================== 1 passed in 0.28s ========================================================= 
```

### Ejercicio 5: Uso de Pytest Fixtures
Objetivo: Refactoriza las pruebas para que utilicen fixtures de Pytest, de modo que se reutilicen instancias comunes de Carrito o de productos.
```
def test_vaciar_carrito(carrito,producto_generico):

    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=1)
    carrito.agregar_producto(producto_generico, cantidad=2) 
    carrito.agregar_producto(producto_generico, cantidad=3)

    # Act
    carrito.vaciar_carrito()
    
    # Assert
    lista = carrito.obtener_items()
    assert lista == []
    assert len(lista) == 0


def test_descuento_condicional(carrito,producto_generico):
    
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=1)
    carrito.agregar_producto(producto_generico, cantidad=2) 
    carrito.agregar_producto(producto_generico, cantidad=3)

    # Act
    nueva_cantidad = carrito.aplicar_descuento_condicional(15, 200)
    # Assert
    assert nueva_cantidad == 0.85 * (1000 + 2 * 50 + 3 * 75)

def test_agregar_producto_en_stock(carrito, producto_generico):

    # Arrange
    producto1 = producto_generico
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto1, cantidad=100)

```

### Ejercicio 6: Pruebas parametrizadas
Objetivo: Utiliza la marca @pytest.mark.parametrize para crear pruebas que verifiquen múltiples escenarios de descuento o actualización de cantidades.
```
@pytest.mark.parametrize(
    "porcentaje, total_esperado",
    [
        (0, 100.0),
        (10, 90.0),
        (50, 50.0),
        (100, 0.0),
    ]
)
def test_aplicar_descuento(carrito,producto_generico, porcentaje, total_esperado):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con una cantidad determinada.
    Act: Se aplica un descuento del 10% al total.
    Assert: Se verifica que el total con descuento sea el correcto.
    """
    # Arrange
    producto = producto_generico
    carrito.agregar_producto(producto, cantidad=1) 
    
    # Act
    total_con_descuento = carrito.aplicar_descuento(porcentaje)
    
    # Assert
    assert total_con_descuento == total_esperado   

@pytest.mark.parametrize(
    "precio_total, porcentaje_descuento, minimo, hay_descuento",
    [
        (600, 10, 500, True),   
        (400, 20, 500, False),  
        (500, 15, 500, True), 
    ]
)
def test_descuento_condicional(carrito,precio_total,porcentaje_descuento,minimo,hay_descuento):
    # Arrange
    producto = ProductoFactory(nombre="Laptop", precio=precio_total)
    carrito.agregar_producto(producto, cantidad=1)

    # Act
    nuevo_total = carrito.aplicar_descuento_condicional(porcentaje_descuento, minimo)

    # Assert
    if(hay_descuento):
        total_esperado =  precio_total * (1 - porcentaje_descuento / 100)
    else:
        total_esperado = precio_total

    assert  nuevo_total == total_esperado 
```
```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_carrito.py::test_descuento_condicional
=================================================== test session starts ==================================================== 
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 3 items

test_carrito.py ...                                                                                                   [100%] 

==================================================== 3 passed in 0.14s =====================================================
```


### Ejercicio 7: Calcular impuestos en el carrito
Objetivo: Implementar un método calcular_impuestos(porcentaje) que retorne el valor del impuesto calculado sobre el total del carrito.

#### Red

```
def test_calcular_impuestos():
    """
    Red: Se espera que calcular_impuestos retorne el valor del impuesto.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto", precio=250.00)
    carrito.agregar_producto(producto, cantidad=4)  # Total = 1000

    # Act
    impuesto = carrito.calcular_impuestos(10)  # 10% de 1000 = 100

    # Assert
    assert impuesto == 100.00
```
#### Green
```
    def calcular_impuestos(self, porcentaje):
        total = self.calcular_total()
        return total * (porcentaje / 100)
```

```
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_carrito.py .                                                                                                     [100%] 

==================================================== 1 passed in 0.11s =====================================================
```
#### Refactor
```
    def calcular_impuestos(self, porcentaje):
        """
        Calcula el valor de los impuestos basados en el porcentaje indicado.
        
        Args:
            porcentaje (float): Porcentaje de impuesto a aplicar (entre 0 y 100).
        
        Returns:
            float: Monto del impuesto.
        
        Raises:
            ValueError: Si el porcentaje no está entre 0 y 100.
        """
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        total = self.calcular_total()
        return total * (porcentaje / 100)
```

### Ejercicio 8: Aplicar cupón de descuento con límite máximo
Objetivo: Implementar un método aplicar_cupon(descuento_porcentaje, descuento_maximo) que aplique un cupón de descuento al total del carrito, pero asegurándose de que el descuento no supere un valor máximo.
#### Red
```
import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

def test_aplicar_cupon_con_limite():
    """
    Red: Se espera que al aplicar un cupón, el descuento no supere el límite máximo.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto", precio=200.00)
    carrito.agregar_producto(producto, cantidad=2)  # Total = 400

    # Act
    total_con_cupon = carrito.aplicar_cupon(20, 50)  # 20% de 400 = 80, pero límite es 50

    # Assert
    assert total_con_cupon == 350.00
```

#### Green
```
def aplicar_cupon(self, descuento_porcentaje, descuento_maximo):
    total = self.calcular_total()
    descuento_calculado = total * (descuento_porcentaje / 100)
    descuento_final = min(descuento_calculado, descuento_maximo)
    return total - descuento_final
```
```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_cupon.py
=================================================== test session starts ==================================================== 
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_cupon.py .                                                                                                       [100%] 

==================================================== 1 passed in 0.12s ===================================================== 
```
#### Refactor
```
def aplicar_cupon(self, descuento_porcentaje, descuento_maximo):
        """
            Aplica un cupón de descuento al total del carrito, asegurando que el descuento no exceda el máximo permitido.
            
            Args:
                descuento_porcentaje (float): Porcentaje de descuento a aplicar.
                descuento_maximo (float): Valor máximo de descuento permitido.
            
            Returns:
                float: Total del carrito después de aplicar el cupón.
            
            Raises:
                ValueError: Si alguno de los valores es negativo.
        """
        if descuento_porcentaje < 0 or descuento_maximo < 0:
            raise ValueError("Los valores de descuento deben ser positivos")
        
        total = self.calcular_total()
        descuento_calculado = total * (descuento_porcentaje / 100)
        descuento_final = min(descuento_calculado, descuento_maximo)
        return total - descuento_final
```


### Ejercicio 9: Validación de stock al agregar productos (RGR)
Objetivo: Asegurarse de que al agregar un producto al carrito, no se exceda la cantidad disponible en stock.
#### Red
```
import pytest
from src.carrito import Carrito, Producto

def test_agregar_producto_excede_stock():
    """
    Red: Se espera que al intentar agregar una cantidad mayor a la disponible en stock se lance un ValueError.
    """
    # Arrange
    # Suponemos que el producto tiene 5 unidades en stock.
    producto = Producto("ProductoStock", 100.00)
    producto.stock = 1
    carrito = Carrito()

    # Act & Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto, cantidad=6)
```
#### Green
```
    def agregar_producto(self, producto, cantidad=1):
        # Verifica el stock disponible
        total_en_carrito = 0
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                total_en_carrito = item.cantidad
                break
        if total_en_carrito + cantidad > producto.stock:
            raise ValueError("Cantidad a agregar excede el stock disponible")
        
        # Si el producto ya existe, incrementa la cantidad
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                item.cantidad += cantidad
                return
        self.items.append(ItemCarrito(producto, cantidad))

```

#### Refactor
```
def _buscar_item(self, producto):
    for item in self.items:
        if item.producto.nombre == producto.nombre:
            return item
    return None

def agregar_producto(self, producto, cantidad=1):
    """
    Agrega un producto al carrito verificando que la cantidad no exceda el stock disponible.
    
    Args:
        producto (Producto): Producto a agregar.
        cantidad (int): Cantidad a agregar.
    
    Raises:
        ValueError: Si la cantidad total excede el stock del producto.
    """
    item = self._buscar_item(producto)
    cantidad_actual = item.cantidad if item else 0

    if cantidad_actual + cantidad > producto.stock:
        raise ValueError("Cantidad a agregar excede el stock disponible")
    
    if item:
        item.cantidad += cantidad
    else:
        self.items.append(ItemCarrito(producto, cantidad))

```
```
PS D:\Varios\DS\actividad-8\tests> pytest .\test_stock.py
=================================================== test session starts ====================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-8, configfile: pytest.ini  
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_stock.py .                                                                                                       [100%]

==================================================== 1 passed in 0.12s ===================================================== 
```
