# Actividad: Red-Green-Refactor

## Paso 1 (Red): Escribimos la primera prueba
### Iteración 1: Agregar usuario (Básico)

```
import pytest
from user_manager import UserManager, UserAlreadyExistsError

def test_agregar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "kapu"
    password = "securepassword"

    # Act
    manager.add_user(username, password)

    # Assert
    assert manager.user_exists(username), "El usuario debería existir después de ser agregado."
```
```
================================================================= ERRORS =================================================================
______________________________________________ ERROR collecting tests/test_user_manager.py _______________________________________________ 
ImportError while importing test module 'D:\Varios\DS\actividad-9b\tests\test_user_manager.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
test_user_manager.py:2: in <module>
    from user_manager import UserManager, UserAlreadyExistsError
E   ModuleNotFoundError: No module named 'user_manager'
======================================================== short test summary info ========================================================= 
ERROR test_user_manager.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
============================================================ 1 error in 0.15s ============================================================
```

## Paso 2 (Green): Implementamos lo mínimo para que pase la prueba

```
class UserAlreadyExistsError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        self.users[username] = password

    def user_exists(self, username):
        return username in self.users
```


```
========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-9b, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_user_manager.py .                                                                                                              [100%]

=========================================================== 1 passed in 0.15s ============================================================ 
```

## Paso 3 (Refactor)

### Iteración 2: Autenticación de usuario (Introducción de una dependencia para Hashing)

### Paso 1 (Red): Escribimos la prueba


```
import pytest
from user_manager import UserManager, UserNotFoundError, UserAlreadyExistsError

class FakeHashService:
    """
    Servicio de hashing 'falso' (Fake) que simplemente simula el hashing
    devolviendo la cadena con un prefijo "fakehash:" para fines de prueba.
    """
    def hash(self, plain_text: str) -> str:
        return f"fakehash:{plain_text}"

    def verify(self, plain_text: str, hashed_text: str) -> bool:
        return hashed_text == f"fakehash:{plain_text}"

def test_autenticar_usuario_exitoso_con_hash():
    # Arrange
    hash_service = FakeHashService()
    manager = UserManager(hash_service=hash_service)

    username = "usuario1"
    password = "mypassword123"
    manager.add_user(username, password)

    # Act
    autenticado = manager.authenticate_user(username, password)

    # Assert
    assert autenticado, "El usuario debería autenticarse correctamente con la contraseña correcta."
```
### Paso 2 (Green): Implementamos la funcionalidad y la DI
```
class UserNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UserManager:
    def __init__(self, hash_service=None):
        """
        Si no se provee un servicio de hashing, se asume un hash trivial por defecto
        (simplemente para no romper el código).
        """
        self.users = {}
        self.hash_service = hash_service
        if not self.hash_service:
            # Si no pasamos un hash_service, usamos uno fake por defecto.
            # En producción, podríamos usar bcrypt o hashlib.
            class DefaultHashService:
                def hash(self, plain_text: str) -> str:
                    return plain_text  # Pésimo, pero sirve de ejemplo.

                def verify(self, plain_text: str, hashed_text: str) -> bool:
                    return plain_text == hashed_text

            self.hash_service = DefaultHashService()

    def add_user(self, username, password):
        if username in self.users:
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed_pw = self.hash_service.hash(password)
        self.users[username] = hashed_pw

    def user_exists(self, username):
        return username in self.users

    def authenticate_user(self, username, password):
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        stored_hash = self.users[username]
        return self.hash_service.verify(password, stored_hash)
```
Ejecutamos pytest y la prueba debería pasar. Nuestra inyección de dependencias nos permite cambiar la lógica de hashing sin modificar UserManager.




```
========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-9b, configfile: pytest.ini 
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 1 item

test_user_manager.py .                                                                                                              [100%]

=========================================================== 1 passed in 0.13s ============================================================
```

Podemos refactorizar si lo consideramos necesario, pero por ahora la estructura cumple el propósito.

### Iteración 3: Uso de un Mock para verificar llamadas (Spy / Mock)
```
def test_hash_service_es_llamado_al_agregar_usuario():
    # Arrange
    mock_hash_service = MagicMock()
    manager = UserManager(hash_service=mock_hash_service)
    username = "spyUser"
    password = "spyPass"

    # Act
    manager.add_user(username, password)

    # Assert
    mock_hash_service.hash.assert_called_once_with(password)
```

### Paso 1 (Red): Escribimos la prueba de "espionaje"
```
from unittest.mock import MagicMock

def test_hash_service_es_llamado_al_agregar_usuario():
    # Arrange
    mock_hash_service = MagicMock()
    manager = UserManager(hash_service=mock_hash_service)
    username = "spyUser"
    password = "spyPass"

    # Act
    manager.add_user(username, password)

    # Assert
    mock_hash_service.hash.assert_called_once_with(password)
```
### Paso 2 (Green): Probar que todo pasa
```
========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-9b, configfile: pytest.ini 
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 2 items

test_user_manager.py ..                                                                                                             [100%]

=========================================================== 2 passed in 0.21s ============================================================
```

### Iteración 4: Excepción al agregar usuario existente (Stubs/más pruebas negativas)
```
def test_no_se_puede_agregar_usuario_existente_stub():
    # Este stub forzará que user_exists devuelva True
    class StubUserManager(UserManager):
        def user_exists(self, username):
            return True

    stub_manager = StubUserManager()
    with pytest.raises(UserAlreadyExistsError) as exc:
        stub_manager.add_user("cualquier", "1234")

    assert "ya existe" in str(exc.value)
```

### Iteración 5: Agregar un "Fake" repositorio de datos (Inyección de Dependencias)

### Paso 1 (Red): Nueva prueba
Creamos una prueba que verifique que podemos inyectar un repositorio y que UserManager lo use.

```
class InMemoryUserRepository:
    """Fake de un repositorio de usuarios en memoria."""
    def __init__(self):
        self.data = {}

    def save_user(self, username, hashed_password):
        if username in self.data:
            raise UserAlreadyExistsError(f"'{username}' ya existe.")
        self.data[username] = hashed_password

    def get_user(self, username):
        return self.data.get(username)

    def exists(self, username):
        return username in self.data

def test_inyectar_repositorio_inmemory():
    repo = InMemoryUserRepository()
    manager = UserManager(repo=repo)  # inyectamos repo
    username = "fakeUser"
    password = "fakePass"

    manager.add_user(username, password)
    assert manager.user_exists(username)
```

### Paso 2 (Green): Implementación

Modificamos UserManager para recibir un repo:
```
class UserManager:
    def __init__(self, hash_service=None, repo=None):
        self.hash_service = hash_service or self._default_hash_service()
        self.repo = repo
        if not self.repo:
            # Si no se inyecta repositorio, usamos uno interno por defecto
            self.repo = self._default_repo()
    
    def _default_hash_service(self):
        class DefaultHashService:
            def hash(self, plain_text: str) -> str:
                return plain_text
            def verify(self, plain_text: str, hashed_text: str) -> bool:
                return plain_text == hashed_text
        return DefaultHashService()

    def _default_repo(self):
        # Un repositorio en memoria muy básico
        class InternalRepo:
            def __init__(self):
                self.data = {}
            def save_user(self, username, hashed_password):
                if username in self.data:
                    raise UserAlreadyExistsError(f"'{username}' ya existe.")
                self.data[username] = hashed_password
            def get_user(self, username):
                return self.data.get(username)
            def exists(self, username):
                return username in self.data
        return InternalRepo()

    def add_user(self, username, password):
        hashed = self.hash_service.hash(password)
        self.repo.save_user(username, hashed)

    def user_exists(self, username):
        return self.repo.exists(username)

    def authenticate_user(self, username, password):
        stored_hash = self.repo.get_user(username)
        if stored_hash is None:
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        return self.hash_service.verify(password, stored_hash)

```

## Paso 3 (Refactor)
### Iteración 6: Introducir un “Spy” de notificaciones (Envío de correo)

### Paso 1 (Red): Prueba
```
from unittest.mock import MagicMock

def test_envio_correo_bienvenida_al_agregar_usuario():
    # Arrange
    mock_email_service = MagicMock()
    manager = UserManager(email_service=mock_email_service)
    username = "nuevoUsuario"
    password = "NuevaPass123!"

    # Act
    manager.add_user(username, password)

    # Assert
    mock_email_service.send_welcome_email.assert_called_once_with(username)
```
### Paso 2 (Green): Implementamos la llamada al servicio de correo
```
class UserManager:
    def __init__(self, hash_service=None, repo=None, email_service=None):
        self.hash_service = hash_service or self._default_hash_service()
        self.repo = repo or self._default_repo()
        self.email_service = email_service 

    def add_user(self, username, password):
        hashed = self.hash_service.hash(password)
        self.repo.save_user(username, hashed)
        if self.email_service:
            self.email_service.send_welcome_email(username)
```
```
========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-9b, configfile: pytest.ini
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 4 items

test_user_manager.py ....                                                                                                           [100%]

=========================================================== 4 passed in 0.17s ============================================================
```

## Ejercicio integral





