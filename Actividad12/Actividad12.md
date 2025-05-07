# Actividad 12: Revisión de fixtures en pruebas


### Paso 1: Inicializar la base de datos
Creamos un fixture que ejecute las acciones de creación de tablas y el cierre de conexión a la base de datos a nivel de módulo.

```
db.create_all()
db.session.close()
```

```
import json
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import db, app  
from models.account import Account

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

```
```
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-12, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 0 items

========================================================== no tests ran in 0.43s ========================================================== 
```

### Paso 2: Cargar datos de prueba

Cargamos los datos de prueba de ```account._data.json``` en la variable ```ACCOUNT_DATA``` para que en el método ```setup_class``` se carguen los datos antes de cada prueba
```
class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        print("Finalizó TestAccountModel")
```

### Paso 3: Escribir un caso de prueba para crear una cuenta
Utilizando el diccionario ```ACCOUNT_DATA``` creamos un primer caso de prueba que consiste en la creación de un usuario y luego lo comprobamos mediante el método de clase ```Account.all()```

```
    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]
        with app.app_context():
            account = Account(**data)
            account.create()
            assert len(Account.all()) == 1
```

```
PS D:\Varios\Actividad12> pytest
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\Actividad12, configfile: setup.cfg      
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

tests\test_account.py .                                                                                                              [100%]

============================================================ 1 passed in 0.67s ============================================================
```

### Paso 4: Escribir un caso de prueba para crear todas las cuentas
Ahora escribimos una prueba que consista en crear todas las cuentas del diccionario ```ACCOUNT_DATA```.Con el método de clase ```Account.all()``` comprobamos que el número de usuarios devuelto es el mismo que el del diccionario.

```
    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        with app.app_context():
            for data in ACCOUNT_DATA:
                account = Account(**data)
                account.create()
            assert len(Account.all()) == len(ACCOUNT_DATA)
```

```
PS D:\Varios\Actividad12> pytest
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\Actividad12, configfile: setup.cfg      
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 2 items

tests\test_account.py ..                                                                                                             [100%]

============================================================ 2 passed in 0.68s ============================================================ 
```

### Paso 5: Limpiar las tablas antes y después de cada prueba
Creamos los métodos ```setup_method``` y ```teardown_method``` para limpiar la base de datos antes y después de cada prueba

```
    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        with app.app_context():
            db.session.remove()
```

```
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\Actividad12, configfile: setup.cfg
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 2 items

tests\test_account.py ..                                                                                                             [100%]

============================================================ 2 passed in 0.61s ============================================================ 
```