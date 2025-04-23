# Actividad 7

## Ejercicio 1: Añadir soporte para minutos y segundos en tiempos de espera

##### belly_steps.py
```
def convertir_palabra_a_numero(palabra):
    try:
        return int(palabra)
    except ValueError:
        numeros = {
            "cero": 0, "uno": 1, "una":1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
            "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11,
            "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16,
            "diecisiete":17, "dieciocho":18, "diecinueve":19, "veinte":20,
            "treinta": 30, "cuarenta":40, "cuarenta y cinco":45 , "cincuenta":50, "sesenta":60, "setenta":70,
            "ochenta":80, "noventa":90, "media": 0.5, "tres mil seiscientos": 3600,
        }
        return numeros.get(palabra.lower(), 0)

@given('que he comido {cukes:d} pepinos')
def step_given_eaten_cukes(context, cukes):
    context.belly.comer(cukes)

@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    time_description = re.sub(r'y|,', ' ', time_description)
    time_description = time_description.strip()

    # Expresión regular para capturar horas, minutos y segundos
    pattern = re.compile(
        r'(?:(\w+)\s*horas?)?\s*'
        r'(?:(\w+)\s*minutos?)?\s*'
        r'(?:(\w+)\s*segundos?)?'
    )
    match = pattern.match(time_description)

    if match:
        hours_word = match.group(1) or "0"
        minutes_word = match.group(2) or "0"
        seconds_word = match.group(3) or "0"

        hours = convertir_palabra_a_numero(hours_word)
        minutes = convertir_palabra_a_numero(minutes_word)
        seconds = convertir_palabra_a_numero(seconds_word)

        total_time_in_hours = hours + (minutes / 60) + (seconds / 3600)
    else:
        num_pattern = re.match(r'(\d+)\s*(segundos|minutos)', time_description)
        if num_pattern:
            valor = int(num_pattern.group(1))
            unidad = num_pattern.group(2)
            if unidad.startswith("minuto"):
                total_time_in_hours = valor / 60
            elif unidad.startswith("segundo"):
                total_time_in_hours = valor / 3600
            else:
                raise ValueError(f"Unidad de tiempo no reconocida: {unidad}")
        else:
            raise ValueError(f"No se pudo interpretar la descripción del tiempo: {time_description}")

    context.belly.esperar(total_time_in_hours)


```
##### Pruebas con behave
```
Albert@DESKTOP-F43V0VL MINGW64 /d/Varios/DS/belly_project (main)
$ behave
Caracter▒stica: Caracter▒stica del est▒mago # features/belly.feature:3

  Escenario: comer muchos pepinos y gru▒ir  # features/belly.feature:5
    Dado que he comido 42 pepinos           # features/steps/belly_steps.py:19
    Cuando espero 2 horas                   # features/steps/belly_steps.py:23
    Entonces mi est▒mago deber▒a gru▒ir     # features/steps/belly_steps.py:63

  Escenario: comer pocos pepinos y no gru▒ir  # features/belly.feature:10
    Dado que he comido 10 pepinos             # features/steps/belly_steps.py:19
    Cuando espero 2 horas                     # features/steps/belly_steps.py:23
    Entonces mi est▒mago no deber▒a gru▒ir    # features/steps/belly_steps.py:67

  Escenario: comer muchos pepinos y esperar menos de una hora  # features/belly.feature:15
    Dado que he comido 50 pepinos                              # features/steps/belly_steps.py:19
    Cuando espero media hora                                   # features/steps/belly_steps.py:23
    Entonces mi est▒mago no deber▒a gru▒ir                     # features/steps/belly_steps.py:67

  Escenario: comer pepinos y esperar en minutos  # features/belly.feature:20
    Dado que he comido 30 pepinos                # features/steps/belly_steps.py:19
    Cuando espero 90 minutos                     # features/steps/belly_steps.py:23
    Entonces mi est▒mago deber▒a gru▒ir          # features/steps/belly_steps.py:63

  Escenario: comer pepinos y esperar en diferentes formatos  # features/belly.feature:25
    Dado que he comido 25 pepinos                            # features/steps/belly_steps.py:19
    Cuando espero "dos horas y treinta minutos"              # features/steps/belly_steps.py:23
    Entonces mi est▒mago deber▒a gru▒ir                      # features/steps/belly_steps.py:63

  Escenario: Comer pepinos y esperar en minutos y segundos  # features/belly.feature:30
    Dado que he comido 35 pepinos                           # features/steps/belly_steps.py:19
    Cuando espero "1 hora y 30 minutos y 45 segundos"       # features/steps/belly_steps.py:23
    Entonces mi est▒mago deber▒a gru▒ir                     # features/steps/belly_steps.py:63

1 feature passed, 0 failed, 0 skipped
6 scenarios passed, 0 failed, 0 skipped
18 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.010s
```
##### Pruebas con pytest

```
Albert@DESKTOP-F43V0VL MINGW64 /d/Varios/DS/belly_project (main)
$ pytest test_parser.py
============================= test session starts =============================
platform win32 -- Python 3.10.9, pytest-8.3.5, pluggy-1.5.0
rootdir: D:/Varios/DS/belly_project
collected 4 items

test_parser.py ....                                                      [100%]

============================== 4 passed in 0.04s ==============================
```

## Ejercicio 2: Manejo de cantidades fraccionarias de pepinos


