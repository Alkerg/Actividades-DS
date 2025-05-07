import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory


@pytest.fixture
def carrito():
    return Carrito()


@pytest.fixture
def producto_generico():
    return ProductoFactory(nombre="Genérico", precio=100.0)