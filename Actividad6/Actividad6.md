# Actividad 6

### Ejercicios teóricos
**1.Diferencias entre git merge y git rebase**
**Pregunta:** Explica la diferencia entre git merge y git rebase y describe en qué escenarios sería más adecuado utilizar cada uno en un equipo de desarrollo ágil que sigue las prácticas de Scrum.
**Respuesta:** Git merge crea un nuevo commit de fusión conservando el historial de cambios de todas las ramas, mientras que git rebase reescribe el historial y mueve una rama como si hubiera partido del cambio más reciente de la otra rama.

**Relación entre git rebase y DevOps**
**Pregunta:** ¿Cómo crees que el uso de git rebase ayuda a mejorar las prácticas de DevOps, especialmente en la implementación continua (CI/CD)? Discute los beneficios de mantener un historial lineal en el contexto de una entrega continua de código y la automatización de pipelines.
**Respuesta:** Ya que git rebase nos permite mantener un historial lineal, se reduce la complejidad en la integración continua. Por otro lado se asegura que el código sea probado con los cambios más actuales.


**Impacto del git cherry-pick en un equipo Scrum**
**Pregunta:** Un equipo Scrum ha finalizado un sprint, pero durante la integración final a la rama principal (main) descubren que solo algunos commits específicos de la rama de una funcionalidad deben aplicarse a producción. ¿Cómo podría ayudar git cherry-pick en este caso? Explica los beneficios y posibles complicaciones
**Respuesta:** Ya que cherry-pick permite aplicar cambios de commits específicos, en este caso, el equipo podrá aplicar los cambios de los commits que se necesitan en la rama producción. En cuanto a las posibles complicaciones, si algunos commit dependen de otros que no se esten aplicando, entonces habrán conflictos.

### Ejercicios prácticos

**1.Simulación de un flujo de trabajo Scrum con git rebase y git merge**

**Pregunta: ¿Qué sucede con el historial de commits después del rebase?**
**Respuesta:** El historial de commits se mezcla, es decir, ahora aparece el commit que hice en feature junto con los commits que hice en main.
**Pregunta: ¿En qué situación aplicarías una fusión fast-forward en un proyecto ágil?**
**Respuesta:** Cuando estoy trabajando en archivos o características distintas de una aplicación, lo cual me asegura que no habrán conflictos al hacer merge.

**2.Cherry-pick para integración selectiva en un pipeline CI/CD**

**Pregunta: ¿Cómo utilizarías cherry-pick en un pipeline de CI/CD para mover solo ciertos cambios listos a producción?**
**Respuesta:** Utilizaría cherry-pick para seleccionar los commits de ramas que contengan cambios listos para ser añadidos a producción

**Pregunta: ¿Qué ventajas ofrece cherry-pick en un flujo de trabajo de DevOps?**
**Respuesta:** Podemos aplicar cambios específicos a producción sin tener que hacer merge de una rama entera y evitar conflictos con ciertos commits.


#### Git, Scrum y Sprints
##### Ejercicio 1: Crear ramas de funcionalidades (feature branches)

**Pregunta: ¿Por qué es importante trabajar en ramas de funcionalidades separadas durante un sprint?**
**Respuesta:** Es importante para mantener los conflictos al mínimo y que podamos trabajar en las funcionalidades de manera más aislada de forma que podamos hacer pruebas unitarias de manera más sencilla y ordenada

##### Ejercicio 2: Integración continua con git rebase
**Pregunta: ¿Qué ventajas proporciona el rebase durante el desarrollo de un sprint en términos de integración continua?**
**Respuesta:** El rebase nos permite mantener un historial limpio y detectar errores antes de integrar 

##### Ejercicio 3: Integración selectiva con git cherry-pick

**Pregunta: ¿Cómo ayuda git cherry-pick a mostrar avances de forma selectiva en un sprint review?**
**Respuesta:** Cherry-pick nos ayuda a mostrar solo las funcionalidades terminadas, es decir, tenemos mayor control sobre lo que se muestra en demos y reviews, reduciendo errores y malentendidos al presentar la version estable del producto que se desarrolla

##### Ejercicio 4: Revisión de conflictos y resolución
**Pregunta: ¿Cómo manejas los conflictos de fusión al final de un sprint? ¿Cómo puede el equipo mejorar la comunicación para evitar conflictos grandes?**
**Respuesta:** Los conflictos se manejan evitando trabajar sobre las mismas características y en caso de haberlos es necesario comunicarse con los autores de los cambios para llegar a un acuerdo

##### Ejercicio 5: Automatización de rebase con hooks de Git

**Pregunta: ¿Qué ventajas y desventajas observas al automatizar el rebase en un entorno de CI/CD?**
**Respuesta:** Una gran ventaja es mantener la rama en la que trabajo actualizada con respecto a la rama principal de forma inmediata, por otro lado también pueden ocurrir conflictos al ejecutarse el rebase.

### Navegando conflictos y versionado en un entorno devOps

#### Preguntas

##### Ejercicio para git checkout --ours y git checkout --theirs

**Contexto:** En un sprint ágil, dos equipos están trabajando en diferentes ramas. Se produce un conflicto de fusión en un archivo de configuración crucial. El equipo A quiere mantener sus cambios mientras el equipo B solo quiere conservar los suyos. El proceso de entrega continua está detenido debido a este conflicto.

**Pregunta:**
¿Cómo utilizarías los comandos git checkout --ours y git checkout --theirs para resolver este conflicto de manera rápida y eficiente? Explica cuándo preferirías usar cada uno de estos comandos y cómo impacta en la pipeline de CI/CD. ¿Cómo te asegurarías de que la resolución elegida no comprometa la calidad del código?
**Respuesta:**
Usaría el comando git checkout --ours para conservar los cambios del equipo A y de igual forma el equipo B.

##### Ejercicio para git diff

**Contexto:** Durante una revisión de código en un entorno ágil, se observa que un pull request tiene una gran cantidad de cambios, muchos de los cuales no están relacionados con la funcionalidad principal. Estos cambios podrían generar conflictos con otras ramas en la pipeline de CI/CD.

**Pregunta:**
Utilizando el comando git diff, ¿cómo compararías los cambios entre ramas para identificar diferencias específicas en archivos críticos? Explica cómo podrías utilizar git diff feature-branch..main para detectar posibles conflictos antes de realizar una fusión y cómo esto contribuye a mantener la estabilidad en un entorno ágil con CI/CD.
**Repuesta:**

##### Ejercicio para git merge --no-commit --no-ff

**Contexto:** En un proyecto ágil con CI/CD, tu equipo quiere simular una fusión entre una rama de desarrollo y la rama principal para ver cómo se comporta el código sin comprometerlo inmediatamente en el repositorio. Esto es útil para identificar posibles problemas antes de completar la fusión.

**Pregunta:**
Describe cómo usarías el comando git merge --no-commit --no-ff para simular una fusión en tu rama local. ¿Qué ventajas tiene esta práctica en un flujo de trabajo ágil con CI/CD, y cómo ayuda a minimizar errores antes de hacer commits definitivos? ¿Cómo automatizarías este paso dentro de una pipeline CI/CD?
**Respuesta:**
La principal ventaja de este comando es que nos permite ejecutar pruebas y validaciones antes de hacer el commit final de merge, de este modo se evita que lleguen a producción merges rotos o con conflictos no resueltos.
Automatizaría este paso de la siguiente manera:

```
 name: Fetch PR branch
        run: |
          git fetch origin ${{ github.head_ref }}:${{ github.head_ref }}

      - name: Merge PR branch (simulate)
        run: |
          git merge --no-commit --no-ff ${{ github.head_ref }}
```

##### Ejercicio para git mergetool

**Contexto:** Tu equipo de desarrollo utiliza herramientas gráficas para resolver conflictos de manera colaborativa. Algunos desarrolladores prefieren herramientas como vimdiff o Visual Studio Code. En medio de un sprint, varios archivos están en conflicto y los desarrolladores prefieren trabajar en un entorno visual para resolverlos.

**Pregunta:**
Explica cómo configurarías y utilizarías git mergetool en tu equipo para integrar herramientas gráficas que faciliten la resolución de conflictos. ¿Qué impacto tiene el uso de git mergetool en un entorno de trabajo ágil con CI/CD, y cómo aseguras que todos los miembros del equipo mantengan consistencia en las resoluciones?

**Respuesta:**

##### Ejercicio para git reset

**Contexto:** En un proyecto ágil, un desarrollador ha hecho un commit que rompe la pipeline de CI/CD. Se debe revertir el commit, pero se necesita hacerlo de manera que se mantenga el código en el directorio de trabajo sin deshacer los cambios.

**Pregunta:**
Explica las diferencias entre git reset --soft, git reset --mixed y git reset --hard. ¿En qué escenarios dentro de un flujo de trabajo ágil con CI/CD utilizarías cada uno? Describe un caso en el que usarías git reset --mixed para corregir un commit sin perder los cambios no commiteados y cómo afecta esto a la pipeline.

**Respuesta:**

##### Ejercicio para git revert

**Contexto:** En un entorno de CI/CD, tu equipo ha desplegado una característica a producción, pero se ha detectado un bug crítico. La rama principal debe revertirse para restaurar la estabilidad, pero no puedes modificar el historial de commits debido a las políticas del equipo.

**Pregunta:**
Explica cómo utilizarías git revert para deshacer los cambios sin modificar el historial de commits. ¿Cómo te aseguras de que esta acción no afecte la pipeline de CI/CD y permita una rápida recuperación del sistema? Proporciona un ejemplo detallado de cómo revertirías varios commits consecutivos.

**Respuesta:**
Para asegurarnos de que esta acción no afecte el pipeline de CI/CD, es conveniente ejecutar pruebas de forma local o hacer el revert en una rama temporal para comprobar que todo siga funcionando. Para revertir varios commits consecutivos podemos hacer lo siguiente:
```
git log --oneline
ccc333 (HEAD -> main) Agregar lógica de facturación
bbb222 Corrección de errores en validación
aaa111 Cambios en el formulario de checkout

git revert --no-commit abc1234^..a1b2c3d
git commit -m "Revertir cambios de checkout, validación y facturación por errores detectados en QA"

```

##### Ejercicio para git stash

**Contexto:** En un entorno ágil, tu equipo está trabajando en una corrección de errores urgente mientras tienes cambios no guardados en tu directorio de trabajo que aún no están listos para ser committeados. Sin embargo, necesitas cambiar rápidamente a una rama de hotfix para trabajar en la corrección.

**Pregunta:**
Explica cómo utilizarías git stash para guardar temporalmente tus cambios y volver a ellos después de haber terminado el hotfix. ¿Qué impacto tiene el uso de git stash en un flujo de trabajo ágil con CI/CD cuando trabajas en múltiples tareas? ¿Cómo podrías automatizar el proceso de stashing dentro de una pipeline CI/CD?
**Respuesta:**

##### Ejercicio para .gitignore

**Contexto:** Tu equipo de desarrollo ágil está trabajando en varios entornos locales con configuraciones diferentes (archivos de logs, configuraciones personales). Estos archivos no deberían ser parte del control de versiones para evitar confusiones en la pipeline de CI/CD.

**Pregunta:**
Diseña un archivo .gitignore que excluya archivos innecesarios en un entorno ágil de desarrollo. Explica por qué es importante mantener este archivo actualizado en un equipo colaborativo que utiliza CI/CD y cómo afecta la calidad y limpieza del código compartido en el repositorio.

**Respuesta:**
El archivo *.gitignore* sería el siguiente:

```
# Archivos del sistema
.DS_Store
Thumbs.db

# Archivos de entorno
.env
*.env.*
*.local

# Dependencias
node_modules/
vendor/

# Compilación / build
dist/
build/
*.log
*.out
*.class
*.pyc
__pycache__/
*.o
*.exe
*.dll

# IDEs y editores
.vscode/
.idea/
*.swp
*.sublime-workspace
*.sublime-project

# Cobertura y pruebas
coverage/
*.lcov
test-results/
junit-report.xml

# CI/CD
*.pid
*.lock
*.bak

# Archivos temporales y otros
*.tmp
*.bak
*.old
*.orig

# Docker
docker-compose.override.yml

# Sistema de control de versiones propio
.git/
```
Es importante mantener este archivo actualizado porque los desarrolladores podrían filtrarse archivos innecesarios en las ramas de desarrollo o de producción y además de ocupar espacio innecesario, se pueden colar variables sensibles o archivos de caché locales y en general, provocaría un caos entre los desarrolladores y multiples problemas de merge. Con un *.gitignore* completo y actualizado los commits y las fusiones serían limpios y se evitarían los problemas anteriormente mencionados. 








