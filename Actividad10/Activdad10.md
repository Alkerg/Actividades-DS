# Actividad 10: Ejecutar pruebas con pytest

## Paso 1: Instalando pytest y pytest-cov

```
python3 -m pip install pytest pytest-cov
```
## Paso 2: Escribiendo y ejecutando pruebas con pytest

Ejecutamos todas las pruebas del proyecto con el comando ```pytest -v```

```
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-10
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 11 items

test_triangle.py::TestAreaOfTriangle::test_float_values PASSED                                                                                                      [  9%] 
test_triangle.py::TestAreaOfTriangle::test_integer_values PASSED                                                                                                    [ 18%] 
test_triangle.py::TestAreaOfTriangle::test_negative_base PASSED                                                                                                     [ 27%] 
test_triangle.py::TestAreaOfTriangle::test_negative_height PASSED                                                                                                   [ 36%] 
test_triangle.py::TestAreaOfTriangle::test_negative_values PASSED                                                                                                   [ 45%] 
test_triangle.py::TestAreaOfTriangle::test_with_boolean PASSED                                                                                                      [ 54%] 
test_triangle.py::TestAreaOfTriangle::test_with_nulls PASSED                                                                                                        [ 63%] 
test_triangle.py::TestAreaOfTriangle::test_with_string PASSED                                                                                                       [ 72%] 
test_triangle.py::TestAreaOfTriangle::test_zero_base PASSED                                                                                                         [ 81%] 
test_triangle.py::TestAreaOfTriangle::test_zero_height PASSED                                                                                                       [ 90%] 
test_triangle.py::TestAreaOfTriangle::test_zero_values PASSED                                                                                                       [100%] 

```
## Paso 3: Añadiendo cobertura de pruebas con pytest-cov

Medimos la covertura de todo el proyecto con el comando ```pytest --cov=pruebas_pytest ```

```
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-10
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 11 items

test_triangle.py ...........                                                                                                                                        [100%]C:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\site-packages\coverage\inorout.py:519: CoverageWarning: Module actividad-10 was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")
C:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\site-packages\coverage\control.py:793: CoverageWarning: No data was collected. (no-data-collected)
  self._warn("No data was collected.", slug="no-data-collected")
WARNING: Failed to generate report: No data to report.

C:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\site-packages\pytest_cov\plugin.py:308: CovReportWarning: Failed to generate report: No data to report.        

  warnings.warn(CovReportWarning(message))




=========================================================================== 11 passed in 0.29s =========================================================================== 
```
Medimos la covertura de un modulo específico con ```pytest -v --cov-triangle.py```

```
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-10
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 11 items

test_triangle.py::TestAreaOfTriangle::test_float_values PASSED                                                                                                      [  9%]
test_triangle.py::TestAreaOfTriangle::test_integer_values PASSED                                                                                                    [ 18%]
test_triangle.py::TestAreaOfTriangle::test_negative_base PASSED                                                                                                     [ 27%] 
test_triangle.py::TestAreaOfTriangle::test_negative_height PASSED                                                                                                   [ 36%]
test_triangle.py::TestAreaOfTriangle::test_negative_values PASSED                                                                                                   [ 45%] 
test_triangle.py::TestAreaOfTriangle::test_with_boolean PASSED                                                                                                      [ 54%] 
test_triangle.py::TestAreaOfTriangle::test_with_nulls PASSED                                                                                                        [ 63%] 
test_triangle.py::TestAreaOfTriangle::test_with_string PASSED                                                                                                       [ 72%] 
test_triangle.py::TestAreaOfTriangle::test_zero_base PASSED                                                                                                         [ 81%]
test_triangle.py::TestAreaOfTriangle::test_zero_height PASSED                                                                                                       [ 90%] 
test_triangle.py::TestAreaOfTriangle::test_zero_values PASSED                                                                                                       [100%] C
:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\site-packages\coverage\inorout.py:519: CoverageWarning: Module triangle.py was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")
C:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\site-packages\coverage\control.py:793: CoverageWarning: No data was collected. (no-data-collected)
  self._warn("No data was collected.", slug="no-data-collected")
WARNING: Failed to generate report: No data to report.

C:\Users\Albert\AppData\Local\Programs\Python\Python310\lib\site-packages\pytest_cov\plugin.py:308: CovReportWarning: Failed to generate report: No data to report.        

  warnings.warn(CovReportWarning(message))


---------- coverage: platform win32, python 3.10.5-final-0 -----------


=========================================================================== 11 passed in 0.24s =========================================================================== 
```

Para un informe más detallado ejecutamos el comando ```pytest --cov=triangle --cov-report=term-missing```

```
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-10
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 11 items

test_triangle.py ...........                                                                                                                                        [100%]

---------- coverage: platform win32, python 3.10.5-final-0 -----------
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
triangle.py      10      0   100%
-------------------------------------------
TOTAL            10      0   100%


=========================================================================== 11 passed in 0.24s =========================================================================== 
```


Si queremos agregar un informe HTML, ejecutamos el siguiente comando ```pytest --cov=triangle --cov-report=term-missing --cov-report=html```

```
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0
rootdir: D:\Varios\DS\actividad-10
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 11 items

test_triangle.py ...........                                                                                                                                        [100%]

---------- coverage: platform win32, python 3.10.5-final-0 -----------
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
triangle.py      10      0   100%
-------------------------------------------
TOTAL            10      0   100%
Coverage HTML written to dir htmlcov


=========================================================================== 11 passed in 0.57s =========================================================================== 
```
## Paso 4: Añadiendo colores automáticamente
Si por alguna razón los colores en la terminarl no se muestran, podemos forzarlos con la opción ```--color=yes```
## Paso 5: Automatizando la configuración de pytest 
Setup.cfg es un archivo de configuración general de todo el paquete o proyecto. Se puede usar para configurar varias herramientas relacionadas con el proyecto, como pytest, flake8, mypy, y otras herramientas que utilicen secciones específicas dentro del archivo. 
```
[tool:pytest]
addopts = -v --tb=short --cov=. --cov-report=term-missing

[coverage:run]
branch = True

[coverage:report]
show_missing = True
```
Por otro lado el archivo pytest.ini es un archivo de configuración específico para pytest
## Paso 6: Ejecutando pruebas con la configuración automatizada
Ya con el archivo setup.cfg, podemos configurar la herramienta de pytest para escribir los comandos que necesitemos sin la necesidad de escribir parámetros adicionales para obtener los datos que necesitamos de las pruebas. Para este archivo la estructura es más simple y directa.
```
[pytest]
addopts = -v --tb=short --cov=. --cov-report=term-missing

[coverage:run]
branch = True

[coverage:report]
show_missing = True
```
```
PS D:\Varios\DS\actividad-10> pytest
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.5.0 -- C:\Users\Albert\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: D:\Varios\DS\actividad-10, configfile: setup.cfg
plugins: anyio-3.6.2, Faker-37.1.0, cov-3.0.0
collected 11 items

test_triangle.py::TestAreaOfTriangle::test_float_values PASSED                                                                                                      [  9%]
test_triangle.py::TestAreaOfTriangle::test_integer_values PASSED                                                                                                    [ 18%] 
test_triangle.py::TestAreaOfTriangle::test_negative_base PASSED                                                                                                     [ 27%] 
test_triangle.py::TestAreaOfTriangle::test_negative_height PASSED                                                                                                   [ 36%] 
test_triangle.py::TestAreaOfTriangle::test_negative_values PASSED                                                                                                   [ 45%] 
test_triangle.py::TestAreaOfTriangle::test_with_boolean PASSED                                                                                                      [ 54%] 
test_triangle.py::TestAreaOfTriangle::test_with_nulls PASSED                                                                                                        [ 63%] 
test_triangle.py::TestAreaOfTriangle::test_with_string PASSED                                                                                                       [ 72%] 
test_triangle.py::TestAreaOfTriangle::test_zero_base PASSED                                                                                                         [ 81%] 
test_triangle.py::TestAreaOfTriangle::test_zero_height PASSED                                                                                                       [ 90%] 
test_triangle.py::TestAreaOfTriangle::test_zero_values PASSED                                                                                                       [100%]

---------- coverage: platform win32, python 3.10.5-final-0 -----------
Name               Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------
test_triangle.py      30      0      2      0   100%
triangle.py           10      0      8      0   100%
--------------------------------------------------------------
TOTAL                 40      0     10      0   100%


=========================================================================== 11 passed in 0.29s =========================================================================== 
```