from unittest import TestCase
from stack import Stack


class TestStack(TestCase):
    """Casos de prueba para la Pila"""
    def test_is_empty(self):
        stack = Stack()
        assert stack.is_empty() == True  # La pila recién creada debe estar vacía
        stack.push(5)
        assert stack.is_empty() == False  # Después de agregar un elemento, la pila no debe estar vacía
    
    def test_peek(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.peek() == 2  # El valor superior debe ser el último agregado (2)
        assert stack.peek() == 2  # La pila no debe cambiar después de peek()
    
    def test_pop(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2  # El valor superior (2) debe eliminarse y devolverse
        assert stack.peek() == 1  # Después de pop(), el valor superior debe ser 1
    
    def test_push(self):
        stack = Stack()
        stack.push(1)
        assert stack.peek() == 1  # El valor recién agregado debe estar en la parte superior
        stack.push(2)
        assert stack.peek() == 2  # Después de otro push, el valor superior debe ser el último agregado