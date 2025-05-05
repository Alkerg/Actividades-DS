# Actividad: Escribir aserciones en pruebas con pytest


## Paso 1: Instalación de pytest y pytest-cov

Instalamos las herramientas necesarias mediante el siguiente comando: ```python3 -m pip install pytest pytest-cov```

## Paso 3: Escribiendo aserciones para el método is_empty()

```
def test_is_empty():
    stack = Stack()
    assert stack.is_empty() == True  # La pila recién creada debe estar vacía
    stack.push(5)
    assert stack.is_empty() == False  # Después de agregar un elemento, la pila no debe estar vacía
```
```
def test_pop(self):
    self.stack.push(3)
    self.stack.push(5)
    self.assertEqual(self.stack.pop(), 5)
    self.assertEqual(self.stack.peek(), 3)
    self.stack.pop()
    self.assertTrue(self.stack.is_empty())
```

## Paso 4: Ejecuta pytest para verificar is_empty()

```
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-11
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_stack.py::TestStack::test_is_empty PASSED                                                                                       [100%]

============================================================ 1 passed in 0.16s ============================================================ 
```

## Paso 5: Escribiendo aserciones para el método peek()

Ahora escribimos el test para el método peek() , test_peek() en test_stack.py de la siguiente manera:

```
def test_peek(self):
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.peek() == 2  # El valor superior debe ser el último agregado (2)
    assert stack.peek() == 2  # La pila no debe cambiar después de peek()
```
```
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-11
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 2 items

test_stack.py::TestStack::test_is_empty PASSED                                                                                       [ 50%]
test_stack.py::TestStack::test_peek PASSED                                                                                           [100%] 

============================================================ 2 passed in 0.15s ============================================================ 
```

## Paso 6: Escribiendo aserciones para el método pop()
Ahora escribimos el test para el método pop() en test_stack.py

```
def test_pop(self):
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2  # El valor superior (2) debe eliminarse y devolverse
    assert stack.peek() == 1  # Después de pop(), el valor superior debe ser 1
```

```
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-11
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 3 items

test_stack.py::TestStack::test_is_empty PASSED                                                                                       [ 33%]
test_stack.py::TestStack::test_peek PASSED                                                                                           [ 66%] 
test_stack.py::TestStack::test_pop PASSED                                                                                            [100%] 

============================================================ 3 passed in 0.17s ============================================================ 
```

## Paso 7: Escribiendo aserciones para el método push()

```
def test_push():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1  # El valor recién agregado debe estar en la parte superior
    stack.push(2)
    assert stack.peek() == 2  # Después de otro push, el valor superior debe ser el último agregado
```



## Paso 8: Ejecuta pytest para verificar todas las pruebas

```
=========================================================== test session starts =========================================================== 
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-11
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 4 items

test_stack.py::TestStack::test_is_empty PASSED                                                                                       [ 25%]
test_stack.py::TestStack::test_peek PASSED                                                                                           [ 50%]
test_stack.py::TestStack::test_pop PASSED                                                                                            [ 75%]
test_stack.py::TestStack::test_push PASSED                                                                                           [100%]

============================================================ 4 passed in 0.32s ============================================================
```

## Paso 9: Agregando cobertura de pruebas con pytest-cov
Ejecutamos el siguiente comando para generar un informe de cobertura: ```pytest --cov=stack --cov-report term-missing```

```
PS D:\Varios\DS\actividad-11> pytest --cov=stack --cov-report term-missing
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-11
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 4 items

test_stack.py ....                                                                                                                   [100%]

---------- coverage: platform win32, python 3.10.5-final-0 -----------
Name       Stmts   Miss  Cover   Missing
----------------------------------------
stack.py      12      0   100%
----------------------------------------
TOTAL         12      0   100%


============================================================ 4 passed in 0.24s ============================================================ 
```


Ahora ejecutamos el comando ```pytest``` con el archivo de configuración ```setup.cfg```
```
[tool:pytest]
addopts = -v --tb=short --cov=stack --cov-report=term-missing

[coverage:run]
branch = True
omit =
    */tests/*
    */test_*

[coverage:report]
show_missing = True
```


```
PS D:\Varios\DS\actividad-11> pytest
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-11, configfile: setup.cfg
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 4 items

test_stack.py::TestStack::test_is_empty PASSED                                                                                       [ 25%]
test_stack.py::TestStack::test_peek PASSED                                                                                           [ 50%] 
test_stack.py::TestStack::test_pop PASSED                                                                                            [ 75%] 
test_stack.py::TestStack::test_push PASSED                                                                                           [100%] 

---------- coverage: platform win32, python 3.10.5-final-0 -----------
Name       Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------
stack.py      12      0      2      0   100%
------------------------------------------------------
TOTAL         12      0      2      0   100%


============================================================ 4 passed in 0.28s ============================================================ 
```
