# Reporte 2.0 - Actividad 19

## Setup Inicial

Lo primerpo que realizamos es terraform init para instalar los modulos y plugins necesarios para el proyecto actual:

````bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ terraform init
Initializing the backend...
Initializing modules...
- simulated_apps in modules/application_service
Initializing provider plugins...
- Finding latest version of hashicorp/template...
- Finding latest version of hashicorp/external...
- Finding hashicorp/local versions matching "~> 2.5"...
- Finding hashicorp/random versions matching "~> 3.6"...
- Finding latest version of hashicorp/null...
- Installing hashicorp/local v2.5.3...
- Installed hashicorp/local v2.5.3 (signed by HashiCorp)
- Installing hashicorp/random v3.7.2...
- Installed hashicorp/random v3.7.2 (signed by HashiCorp)
- Installing hashicorp/null v3.2.4...
- Installed hashicorp/null v3.2.4 (signed by HashiCorp)
- Installing hashicorp/template v2.2.0...
- Installed hashicorp/template v2.2.0 (signed by HashiCorp)
- Installing hashicorp/external v2.3.5...
- Installed hashicorp/external v2.3.5 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ 

````

Pero nosotros debemos realizar un par de cambios antes de continuar para poder realizar la aplicación de terraform con el comando `terraform apply`. 

El primer cambio lo encontramos en el archivo `main.tf` raíz (el que se encuentra en `/Proyecto_iac_local/`), pues la ruta del ejecutable de Python es diferente a la de Windows.

`which python` nos brinda la ruta: `/usr/bin/python`

Modificamos la dirección de Python en `main.tf` raiz:

`main.tf` antes:

```
resource "local_file" "bienvenida" {
  content  = "Bienvenido al proyecto IaC local! Hora: ${timestamp()}"
  filename = "${path.cwd}/generated_environment/bienvenida.txt"
}

resource "random_id" "entorno_id" {
  byte_length = 8
}

output "id_entorno" {
  value = random_id.entorno_id.hex
}

output "ruta_bienvenida" {
  value = local_file.bienvenida.filename
}

variable "python_executable" {
  description = "Ruta al ejecutable de Python (python o python3)."
  type        = string
  default     = "C:/Users/kapum/DS/bdd/Scripts/python.exe"
}

locals {
  common_app_config = {
    app1 = { version = "1.0.2", port = 8081 }
    app2 = { version = "0.5.0", port = 8082 }
    # Se pueden añadir más líneas fácilmente
    # app3 = { version = "2.1.0", port = 8083 }
    # app4 = { version = "1.0.0", port = 8084 }
  }
}

module "simulated_apps" {
  for_each = local.common_app_config

  source                   = "./modules/application_service"
  app_name                 = each.key
  app_version              = each.value.version
  app_port                 = each.value.port
  base_install_path        = "${path.cwd}/generated_environment/services"
  global_message_from_root = var.mensaje_global # Pasar la variable sensible
  python_exe               = var.python_executable
}

output "detalles_apps_simuladas" {
  value = {
    for k, app_instance in module.simulated_apps : k => {
      config_path  = app_instance.service_config_path
      install_path = app_instance.service_install_path
      # metadata    = app_instance.service_metadata_content # Puede ser muy verboso
      metadata_id = app_instance.service_metadata_content.uniqueId
    }
  }
  sensitive = true # Porque contiene mensaje_global (indirectamente)
}

resource "null_resource" "validate_all_configs" {
  depends_on = [module.simulated_apps] # Asegura que las apps se creen primero
  triggers = {
    # Re-validar si cualquier output de las apps cambia (muy general, pero para el ejemplo)
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  provisioner "local-exec" {
    command = "${var.python_executable} ${path.cwd}/scripts/python/validate_config.py ${path.cwd}/generated_environment/services"
    # Opcional: ¿qué hacer si falla?
    # on_failure = fail # o continue
  }
}

resource "null_resource" "check_all_healths" {
  depends_on = [null_resource.validate_all_configs] # Después de validar
  # Triggers similares o basados en los PIDs si los expusiéramos como output
  triggers = {
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  # Usar un bucle for para llamar al script de health check para cada servicio
  # Esto es un poco más avanzado con provisioners, una forma simple es invocar un script que lo haga internamente
  # O, si quisiéramos hacerlo directamente con N llamadas:
  # (Esto es solo ilustrativo, un script que itere sería mejor para muchos servicios)
  provisioner "local-exec" {
    when        = create # o always si se quiere
    command     = <<EOT
      for service_dir in $(ls -d ${path.cwd}/generated_environment/services/*/); do
        bash ${path.cwd}/scripts/bash/check_simulated_health.sh "$service_dir"
      done
    EOT
    interpreter = ["bash", "-c"]
  }
}

```

`main.tf` después de modificar la variable "python_executable":

```
resource "local_file" "bienvenida" {
  content  = "Bienvenido al proyecto IaC local! Hora: ${timestamp()}"
  filename = "${path.cwd}/generated_environment/bienvenida.txt"
}

resource "random_id" "entorno_id" {
  byte_length = 8
}

output "id_entorno" {
  value = random_id.entorno_id.hex
}

output "ruta_bienvenida" {
  value = local_file.bienvenida.filename
}

variable "python_executable" {
  description = "Ruta al ejecutable de Python (python o python3)."
  type        = string
  default     = "/usr/bin/python"
}

locals {
  common_app_config = {
    app1 = { version = "1.0.2", port = 8081 }
    app2 = { version = "0.5.0", port = 8082 }
    # Se pueden añadir más líneas fácilmente
    # app3 = { version = "2.1.0", port = 8083 }
    # app4 = { version = "1.0.0", port = 8084 }
  }
}

module "simulated_apps" {
  for_each = local.common_app_config

  source                   = "./modules/application_service"
  app_name                 = each.key
  app_version              = each.value.version
  app_port                 = each.value.port
  base_install_path        = "${path.cwd}/generated_environment/services"
  global_message_from_root = var.mensaje_global # Pasar la variable sensible
  python_exe               = var.python_executable
}

output "detalles_apps_simuladas" {
  value = {
    for k, app_instance in module.simulated_apps : k => {
      config_path  = app_instance.service_config_path
      install_path = app_instance.service_install_path
      # metadata    = app_instance.service_metadata_content # Puede ser muy verboso
      metadata_id = app_instance.service_metadata_content.uniqueId
    }
  }
  sensitive = true # Porque contiene mensaje_global (indirectamente)
}

resource "null_resource" "validate_all_configs" {
  depends_on = [module.simulated_apps] # Asegura que las apps se creen primero
  triggers = {
    # Re-validar si cualquier output de las apps cambia (muy general, pero para el ejemplo)
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  provisioner "local-exec" {
    command = "${var.python_executable} ${path.cwd}/scripts/python/validate_config.py ${path.cwd}/generated_environment/services"
    # Opcional: ¿qué hacer si falla?
    # on_failure = fail # o continue
  }
}

resource "null_resource" "check_all_healths" {
  depends_on = [null_resource.validate_all_configs] # Después de validar
  # Triggers similares o basados en los PIDs si los expusiéramos como output
  triggers = {
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  # Usar un bucle for para llamar al script de health check para cada servicio
  # Esto es un poco más avanzado con provisioners, una forma simple es invocar un script que lo haga internamente
  # O, si quisiéramos hacerlo directamente con N llamadas:
  # (Esto es solo ilustrativo, un script que itere sería mejor para muchos servicios)
  provisioner "local-exec" {
    when        = create # o always si se quiere
    command     = <<EOT
      for service_dir in $(ls -d ${path.cwd}/generated_environment/services/*/); do
        bash ${path.cwd}/scripts/bash/check_simulated_health.sh "$service_dir"
      done
    EOT
    interpreter = ["bash", "-c"]
  }
}

```

En este primer cambio, procedemos a realizar la validación de nuestro proyecto en Terraform:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ terraform validate
Success! The configuration is valid.


```

Así mismo, este es el árbol del directorio del proyecto, el cual nos permitirá conocer la estructura inicial del proyecto y analizar como evoluciona paso a paso:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ tree
.
├── Instrucciones.md
├── main.tf
├── modules
│   ├── application_service
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   ├── templates
│   │   │   └── config.json.tpl
│   │   └── variables.tf
│   └── environment_setup
│       ├── main.tf
│       ├── scripts
│       │   └── initial_setup.sh
│       └── variables.tf
├── outputs.tf
├── scripts
│   ├── bash
│   │   ├── check_simulated_health.sh
│   │   └── start_simulated_service.sh
│   └── python
│       ├── generate_app_metadata.py
│       └── validate_config.py
├── terraform.tfstate
├── terraform.tfvars.example
├── variables.tf
└── versions.tf

9 directories, 18 files
```



---

## Fases

### Fase 0: Preparación e introducción

### Fase 1: Fundamentos de terraform y primer recurso local

`versions.tf` en raíz:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat versions.tf 
terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

```

`main.tf` en raíz:

Notamos que el primer resource es la indicación de un recurso de bienvenida indicando cuyo contenido es una string de saludo junto a la hora de ejecución.

Notamos que el segundo resource, "random_id" "id_entorno" indica la longitud para un byte, y su nombre indica que será para la generación de una id aleatoria.

Notamos que el primer output "id_entorno" almacena el valor de una id aleatoria

Notamos que el segundo output "ruta_bienvenida almacena la ruta del archivo de bienvenida

```bash
resource "local_file" "bienvenida" {
  content  = "Bienvenido al proyecto IaC local! Hora: ${timestamp()}"
  filename = "${path.cwd}/generated_environment/bienvenida.txt"
}

resource "random_id" "entorno_id" {
  byte_length = 8
}

output "id_entorno" {
  value = random_id.entorno_id.hex
}

output "ruta_bienvenida" {
  value = local_file.bienvenida.filename
}

variable "python_executable" {
  description = "Ruta al ejecutable de Python (python o python3)."
  type        = string
  default     = "/usr/bin/python"
}

locals {
  common_app_config = {
    app1 = { version = "1.0.2", port = 8081 }
    app2 = { version = "0.5.0", port = 8082 }
    # Se pueden añadir más líneas fácilmente
    # app3 = { version = "2.1.0", port = 8083 }
    # app4 = { version = "1.0.0", port = 8084 }
  }
}

module "simulated_apps" {
  for_each = local.common_app_config

  source                   = "./modules/application_service"
  app_name                 = each.key
  app_version              = each.value.version
  app_port                 = each.value.port
  base_install_path        = "${path.cwd}/generated_environment/services"
  global_message_from_root = var.mensaje_global # Pasar la variable sensible
  python_exe               = var.python_executable
}

output "detalles_apps_simuladas" {
  value = {
    for k, app_instance in module.simulated_apps : k => {
      config_path  = app_instance.service_config_path
      install_path = app_instance.service_install_path
      # metadata    = app_instance.service_metadata_content # Puede ser muy verboso
      metadata_id = app_instance.service_metadata_content.uniqueId
    }
  }
  sensitive = true # Porque contiene mensaje_global (indirectamente)
}

resource "null_resource" "validate_all_configs" {
  depends_on = [module.simulated_apps] # Asegura que las apps se creen primero
  triggers = {
    # Re-validar si cualquier output de las apps cambia (muy general, pero para el ejemplo)
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  provisioner "local-exec" {
    command = "${var.python_executable} ${path.cwd}/scripts/python/validate_config.py ${path.cwd}/generated_environment/services"
    # Opcional: ¿qué hacer si falla?
    # on_failure = fail # o continue
  }
}

resource "null_resource" "check_all_healths" {
  depends_on = [null_resource.validate_all_configs] # Después de validar
  # Triggers similares o basados en los PIDs si los expusiéramos como output
  triggers = {
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  # Usar un bucle for para llamar al script de health check para cada servicio
  # Esto es un poco más avanzado con provisioners, una forma simple es invocar un script que lo haga internamente
  # O, si quisiéramos hacerlo directamente con N llamadas:
  # (Esto es solo ilustrativo, un script que itere sería mejor para muchos servicios)
  provisioner "local-exec" {
    when        = create # o always si se quiere
    command     = <<EOT
      for service_dir in $(ls -d ${path.cwd}/generated_environment/services/*/); do
        bash ${path.cwd}/scripts/bash/check_simulated_health.sh "$service_dir"
      done
    EOT
    interpreter = ["bash", "-c"]
  }
}

```



### Fase 2

`variables.tf` en raíz:

Notamos la creación de tres variables para nuestro proyecto en raíz, "nombre_entorno" establece que el nombre de la variable será "desarrollo". Mientras que la segunda variable "numero_instancias_app_simulada" será un contandor de instancias de la app simuladas que se crearán y está sujeto a un valor fijo _2_. Finalmente, la variable "mensaje_global" 

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat variables.tf 
variable "nombre_entorno" {
  description = "Nombre base para el entorno generado."
  type        = string
  default     = "desarrollo"
}

variable "numero_instancias_app_simulada" {
  description = "Cuántas instancias de la app simulada crear."
  type        = number
  default     = 2
}

variable "mensaje_global" {
  description = "Un mensaje para incluir en varios archivos."
  type        = string
  default     = "Configuración gestionada por Terraform."
  sensitive   = true # Para demostrar

```

`terraform.tfvars.example`:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat terraform.tfvars.example 
nombre_entorno = "mi_proyecto_local"
numero_instancias_app_simulada = 3
// mensaje_global se puede omitir para usar default, o definir aquí.
```

`modules/environment_setup/main.tf`:

Nos encontramos dentro del módulo environment_setup y este módulo se encarga de crear 

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/environment_setup/main.tf 
variable "base_path" {
  description = "Ruta base para el entorno."
  type        = string
}

variable "nombre_entorno_modulo" {
  description = "Nombre del entorno para este módulo."
  type        = string
}

resource "null_resource" "crear_directorio_base" {
  # Usar provisioner para crear el directorio si no existe
  # Esto asegura que el directorio existe antes de que otros recursos intenten usarlo
  provisioner "local-exec" {
    command = "mkdir -p ${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
  # Añadir un trigger para que se ejecute si cambia el nombre del entorno
  triggers = {
    dir_name = "${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
}

resource "local_file" "readme_entorno" {
  content    = "Este es el entorno ${var.nombre_entorno_modulo}. ID: ${random_id.entorno_id_modulo.hex}"
  filename   = "${var.base_path}/${var.nombre_entorno_modulo}_data/README.md"
  depends_on = [null_resource.crear_directorio_base]
}

resource "random_id" "entorno_id_modulo" {
  byte_length = 4
}

resource "null_resource" "ejecutar_setup_inicial" {
  depends_on = [local_file.readme_entorno]
  triggers = {
    readme_md5 = local_file.readme_entorno.content_md5 # Se reejecuta si el README cambia
  }
  provisioner "local-exec" {
    command     = "bash ${path.module}/scripts/initial_setup.sh '${var.nombre_entorno_modulo}' '${local_file.readme_entorno.filename}'"
    interpreter = ["bash", "-c"]
    working_dir = "${var.base_path}/${var.nombre_entorno_modulo}_data" # Ejecutar script desde aquí
  }
}

output "ruta_readme_modulo" {
  value = local_file.readme_entorno.filename
}
```

Vamos a separar sus variables al archivo `/modules/environment_setup/variables.tf`:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/environment_setup/variables.tf 
variable "base_path" {
  description = "Ruta base para el entorno."
  type        = string
}

variable "nombre_entorno_modulo" {
  description = "Nombre del entorno para este módulo."
  type        = string
}

```

Para ello debemos eliminar dichas variables de `/modules/environment_setup/main.tf`

```bash
resource "null_resource" "crear_directorio_base" {
  # Usar provisioner para crear el directorio si no existe
  # Esto asegura que el directorio existe antes de que otros recursos intenten usarlo
  provisioner "local-exec" {
    command = "mkdir -p ${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
  # Añadir un trigger para que se ejecute si cambia el nombre del entorno
  triggers = {
    dir_name = "${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
}

resource "local_file" "readme_entorno" {
  content    = "Este es el entorno ${var.nombre_entorno_modulo}. ID: ${random_id.entorno_id_modulo.hex}"
  filename   = "${var.base_path}/${var.nombre_entorno_modulo}_data/README.md"
  depends_on = [null_resource.crear_directorio_base]
}

resource "random_id" "entorno_id_modulo" {
  byte_length = 4
}

resource "null_resource" "ejecutar_setup_inicial" {
  depends_on = [local_file.readme_entorno]
  triggers = {
    readme_md5 = local_file.readme_entorno.content_md5 # Se reejecuta si el README cambia
  }
  provisioner "local-exec" {
    command     = "bash ${path.module}/scripts/initial_setup.sh '${var.nombre_entorno_modulo}' '${local_file.readme_entorno.filename}'"
    interpreter = ["bash", "-c"]
    working_dir = "${var.base_path}/${var.nombre_entorno_modulo}_data" # Ejecutar script desde aquí
  }
}

output "ruta_readme_modulo" {
  value = local_file.readme_entorno.filename
}
```

Vemos que `/modules/environment_setup/scripts/initial_setup.sh` ya estaba listo:

```bash
#!/bin/bash
# Script: initial_setup.sh
ENV_NAME=$1
README_PATH=$2
echo "Ejecutando setup inicial para el entorno: $ENV_NAME"
echo "Fecha de setup: $(date)" > setup_log.txt
echo "Readme se encuentra en: $README_PATH" >> setup_log.txt
echo "Creando archivo de placeholder..."
touch placeholder_$(date +%s).txt
echo "Setup inicial completado."
# Simular más líneas de código
for i in {1..20}; do
    echo "Paso de configuración simulado $i..." >> setup_log.txt
    # sleep 0.01 # Descomenta para simular trabajo
done

```

Debemos añadir el modulo y output a nuestro `main.tf` raíz:

```
module "config_entorno_principal" {
  source                = "./modules/environment_setup"
  base_path             = "${path.cwd}/generated_environment"
  nombre_entorno_modulo = var.nombre_entorno
}

output "readme_principal" {
  value = module.config_entorno_principal.ruta_readme_modulo
}
```



### Fase 3: Módulos, plantillas y scripts Python

Ya se encuentran los cambios implementados en `modules/application_service/main.tf`

````bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/application_service/main.tf 
variable "app_name"                 { type = string }
variable "app_version"              { type = string }
variable "app_port"                 { type = number }
variable "base_install_path"        { type = string }
variable "global_message_from_root" { type = string }
variable "python_exe"               { type = string }

locals {
  install_path = "${var.base_install_path}/${var.app_name}_v${var.app_version}"
}

resource "null_resource" "crear_directorio_app" {
  triggers = { dir_path = local.install_path }

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command     = "mkdir -p \"${local.install_path}/logs\""
  }
}

data "template_file" "app_config" {
  template = file("${path.module}/templates/config.json.tpl")
  vars = {
    app_name_tpl    = var.app_name
    app_version_tpl = var.app_version
    port_tpl        = var.app_port
    deployed_at_tpl = timestamp()
    message_tpl     = var.global_message_from_root
  }
}

resource "local_file" "config_json" {
  content    = data.template_file.app_config.rendered
  filename   = "${local.install_path}/config.json"
  depends_on = [null_resource.crear_directorio_app]
}

data "external" "app_metadata_py" {
  program = [var.python_exe, "${path.root}/scripts/python/generate_app_metadata.py"]

  query = merge(
    {
      app_name   = var.app_name
      version    = var.app_version
      input_data = "datos_adicionales_para_python"
    },
    {
      q1  = "v1",  q2  = "v2",  q3  = "v3",  q4  = "v4",  q5  = "v5",
      q6  = "v6",  q7  = "v7",  q8  = "v8",  q9  = "v9",  q10 = "v10",
      q11 = "v11", q12 = "v12", q13 = "v13", q14 = "v14", q15 = "v15",
      q16 = "v16", q17 = "v17", q18 = "v18", q19 = "v19", q20 = "v20"
    }
  )
}

resource "local_file" "metadata_json" {
  content    = data.external.app_metadata_py.result.metadata_json_string
  filename   = "${local.install_path}/metadata_generated.json"
  depends_on = [null_resource.crear_directorio_app]
}

resource "null_resource" "start_service_sh" {
  depends_on = [local_file.config_json, local_file.metadata_json]

  triggers = {
    config_md5   = local_file.config_json.content_md5
    metadata_md5 = local_file.metadata_json.content_md5
  }

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command     = "${path.root}/scripts/bash/start_simulated_service.sh '${var.app_name}' '${local.install_path}' '${local_file.config_json.filename}'"
  }
}

output "service_install_path"  { value = local.install_path }
output "service_config_path"   { value = local_file.config_json.filename }
output "service_metadata_content" {
  value = jsondecode(data.external.app_metadata_py.result.metadata_json_string)

````

`modules/application_service/variables.tf`:

separamos las variables en el archivo dedicado

````bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/application_service/variables.tf 
variable "app_name" { type = string }
variable "app_version" { type = string }
variable "app_port" { type = number }
variable "base_install_path" { type = string }
variable "global_message_from_root" { type = string }
variable "python_exe" { type = string } # Ruta al ejecutable de Python

````

`modules/application_service/templates/config.json.tpl`:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/application_service/templates/config.json.tpl 
{
    "applicationName": "${app_name_tpl}",
    "version": "${app_version_tpl}",
    "listenPort": ${port_tpl},
    "deploymentTime": "${deployed_at_tpl}",
    "notes": "Este es un archivo de configuración autogenerado. ${message_tpl}",
    "settings": {
        "featureA": true,
        "featureB": false,
        "maxConnections": 100,
        "logLevel": "INFO"
        // Líneas de settings simulados
        ,"s1": "val1", "s2": "val2", "s3": "val3", "s4": "val4", "s5": "val5"
        ,"s6": "val6", "s7": "val7", "s8": "val8", "s9": "val9", "s10": "val10"
        ,"s11": "val11", "s12": "val12", "s13": "val13", "s14": "val14", "s15": "val15"
        ,"s16": "val16", "s17": "val17", "s18": "val18", "s19": "val19", "s20": "val20"
        ,"s21": "val21", "s22": "val22", "s23": "val23", "s24": "val24", "s25": "val25"
        ,"s26": "val26", "s27": "val27", "s28": "val28", "s29": "val29", "s30": "val30"
    }
}

```

`scripts/python/generate_app_metada.py`:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat scripts/python/generate_app_metadata.py 
import json
import sys
import datetime
import uuid

# Función para simular lógica compleja
def complex_logic_simulation(app_name, version):
    # Simular múltiples operaciones y generación de datos
    data_points = []
    for i in range(15): # Generar 15 líneas de "lógica"
        data_points.append(f"Simulated data point {i} for {app_name} v{version} - {uuid.uuid4()}")

    dependencies = {} # Simular 10 líneas de dependencias
    for i in range(10):
        dependencies[f"dep_{i}"] = f"version_{i}.{i+1}"

    computed_values = {} # Simular 10 líneas de valores computados
    for i in range(10):
        computed_values[f"val_{i}"] = i * 100 / (i + 0.5)

    return {
        "generated_data_points": data_points,
        "simulated_dependencies": dependencies,
        "calculated_metrics": computed_values,
        "generation_details": [f"Detail line {j}" for j in range(15)] # 15 líneas más
    }

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test-lines": # Para contar líneas fácilmente
        print(f"Lee  líneas de código Python (incluyendo comentarios y espacios).")
        # Simulación de más líneas para conteo
        for i in range(60): # 60 print statements
            print(f"Línea de prueba {i}")
        return

    input_str = sys.stdin.read()
    input_json = json.loads(input_str)

    app_name = input_json.get("app_name", "unknown_app")
    app_version = input_json.get("version", "0.0.0")
    # input_data = input_json.get("input_data", "") # Usar si es necesario

    # Lógica de generación de metadatos 
    metadata = {
        "appName": app_name,
        "appVersion": app_version,
        "generationTimestamp": datetime.datetime.utcnow().isoformat(),
        "generator": "Python IaC Script",
        "uniqueId": str(uuid.uuid4()),
        "parametersReceived": input_json,
        "simulatedComplexity": complex_logic_simulation(app_name, app_version),
        "additional_info": [f"Linea info {k}" for k in range(10)], # 10 líneas
        "status_flags": {f"flag_{l}": (l % 2 == 0) for l in range(10)} # 10 líneas
    }
    # Simulación de más lógica de negocio 
    metadata["processing_log"] = []
    for i in range(30):
        metadata["processing_log"].append(f"Entrada log  {i}: Item procesado {uuid.uuid4()}")

    # El script DEBE imprimir un JSON válido a stdout para 'data "external"'
    print(json.dumps({"metadata_json_string": json.dumps(metadata, indent=2)}))

if __name__ == "__main__":

```

`scripts/bash/start_simulated_service.sh`:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat scripts/bash/start_simulated_service.sh
#!/bin/bash
APP_NAME=$1
INSTALL_PATH=$2
CONFIG_FILE=$3

echo "--- Iniciando servicio simulado: $APP_NAME ---"
echo "Ruta de instalación: $INSTALL_PATH"
echo "Archivo de configuración: $CONFIG_FILE"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: Archivo de configuración no encontrado: $CONFIG_FILE"
  exit 1
fi

# 1) Asegurarse de que exista el directorio de logs
LOG_DIR="$INSTALL_PATH/logs"
mkdir -p "$LOG_DIR"

PID_FILE="$INSTALL_PATH/${APP_NAME}.pid"
LOG_FILE="$LOG_DIR/${APP_NAME}_startup.log"

echo "Simulando inicio de $APP_NAME a las $(date)" >> "$LOG_FILE"
# Simular más líneas de logging y operaciones
for i in {1..25}; do
    echo "Paso de arranque $i: verificando sub-componente $i..." >> "$LOG_FILE"
    # sleep 0.01 # Descomenta para simular tiempo
done

# Crear un archivo PID simulado
echo $$ > "$PID_FILE"  # $$ es el PID del script actual
echo "Servicio $APP_NAME 'iniciado'. PID guardado en $PID_FILE" >> "$LOG_FILE"
echo "Servicio $APP_NAME 'iniciado'. PID: $(cat "$PID_FILE")"
echo "--- Fin inicio servicio $APP_NAME ---"

```

`main.tf` raiz:

Ya está listo.

### Fase 4: Validación y reportes (Python y Bash)

`scripts/python/validate_config.py`:

````python
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat scripts/python/validate_config.py 
import json
import sys
import os

# Función para simular validaciones complejas
def perform_complex_validations(config_data, file_path):
    errors = []
    warnings = []
    # Simular 20 líneas de validaciones
    if not isinstance(config_data.get("applicationName"), str):
        errors.append(f"[{file_path}] 'applicationName' debe ser un string.")
    if not isinstance(config_data.get("listenPort"), int):
        errors.append(f"[{file_path}] 'listenPort' debe ser un entero.")
    elif not (1024 < config_data.get("listenPort", 0) < 65535):
        warnings.append(f"[{file_path}] 'listenPort' {config_data.get('listenPort')} está fuera del rango común.")

    # Más validaciones simuladas
    for i in range(10):
        if f"setting_{i}" not in config_data.get("settings", {}):
             warnings.append(f"[{file_path}] Falta 'settings.setting_{i}'.")
    if len(config_data.get("notes", "")) < 10:
        warnings.append(f"[{file_path}] 'notes' es muy corto.")

    # Simulación de 15 chequeos adicionales
    for i in range(15):
        if config_data.get("settings",{}).get(f"s{i+1}") == None:
             errors.append(f"[{file_path}] Falta el setting s{i+1}")

    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No se proporcionó la ruta al directorio de configuración."}))
        sys.exit(1)

    config_dir_path = sys.argv[1]
    all_errors = []
    all_warnings = []
    files_processed = 0

    # Simulación de lógica de recorrido y validación 
    for root, _, files in os.walk(config_dir_path):
        for file in files:
            if file == "config.json": # Solo valida los config.json
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    errors, warnings = perform_complex_validations(data, file_path)
                    all_errors.extend(errors)
                    all_warnings.extend(warnings)
                    files_processed += 1
                except json.JSONDecodeError:
                    all_errors.append(f"[{file_path}] Error al decodificar JSON.")
                except Exception as e:
                    all_errors.append(f"[{file_path}] Error inesperado: {str(e)}")

    # Simulación de más líneas de código de reporte 
    report_summary = [f"Archivo de resumen de validación generado el {datetime.datetime.now()}"]
    for i in range(19):
        report_summary.append(f"Línea de sumario {i}")


    print(json.dumps({
        "validation_summary": f"Validados {files_processed} archivos de configuración.",
        "errors_found": all_errors,
        "warnings_found": all_warnings,
        "detailed_report_lines": report_summary # Más líneas
    }))

if __name__ == "__main__":
    # Añadir import datetime si no está
    import datetime
    main()

````

`scripts/bash/check_simulated_health.sh`:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat scripts/bash/check_simulated_health.sh 
#!/bin/bash
SERVICE_PATH=$1
SERVICE_NAME=$(basename "$SERVICE_PATH") # Asumir que el último componente es el nombre

echo "--- Comprobando salud de: $SERVICE_NAME en $SERVICE_PATH ---"

# Directorio y fichero de logs
LOG_DIR="$SERVICE_PATH/logs"
LOG_FILE="$LOG_DIR/${SERVICE_NAME}_health.log"

# Asegurarse de que exista el directorio de logs
mkdir -p "$LOG_DIR"

# Intentar extraer nombre base del servicio (app1 de app1_v1.0.2)
BASE_SERVICE_NAME=$(echo "$SERVICE_NAME" | cut -d'_' -f1)
PID_FILE_ACTUAL="$SERVICE_PATH/${BASE_SERVICE_NAME}.pid"

echo "Comprobación iniciada a $(date)" > "$LOG_FILE"
# Simular más líneas de operaciones y logging
for i in {1..20}; do
    echo "Paso de comprobación $i: verificando recurso $i..." >> "$LOG_FILE"
done

if [ -f "$PID_FILE_ACTUAL" ]; then
    PID=$(cat "$PID_FILE_ACTUAL")
    # En un sistema real, verificaríamos si el proceso con ese PID existe.
    # Aquí simulamos que está "corriendo" si el PID file existe.
    echo "Servicio $BASE_SERVICE_NAME (PID $PID) parece estar 'corriendo'." | tee -a "$LOG_FILE"
    echo "HEALTH_STATUS: OK" >> "$LOG_FILE"
    echo "--- Salud OK para $SERVICE_NAME ---"
    exit 0
else
    echo "ERROR: Archivo PID $PID_FILE_ACTUAL no encontrado. $BASE_SERVICE_NAME parece no estar 'corriendo'." | tee -a "$LOG_FILE"
    echo "HEALTH_STATUS: FAILED" >> "$LOG_FILE"
    echo "--- Salud FALLIDA para $SERVICE_NAME ---"
    exit 1
fi

```

`main.tf` notamos que ya se encuentra `null_resource` para ejecutar los scripts:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat main.tf 
resource "local_file" "bienvenida" {
  content  = "Bienvenido al proyecto IaC local! Hora: ${timestamp()}"
  filename = "${path.cwd}/generated_environment/bienvenida.txt"
}

resource "random_id" "entorno_id" {
  byte_length = 8
}

output "id_entorno" {
  value = random_id.entorno_id.hex
}

output "ruta_bienvenida" {
  value = local_file.bienvenida.filename
}

locals {
  common_app_config = {
    app1 = { version = "1.0.2", port = 8081 }
    app2 = { version = "0.5.0", port = 8082 }
    # Se pueden añadir más líneas fácilmente
    # app3 = { version = "2.1.0", port = 8083 }
    # app4 = { version = "1.0.0", port = 8084 }
  }
}

module "config_entorno_principal" {
  source                = "./modules/environment_setup"
  base_path             = "${path.cwd}/generated_environment"
  nombre_entorno_modulo = var.nombre_entorno
}

output "readme_principal" {
  value = module.config_entorno_principal.ruta_readme_modulo
}

module "simulated_apps" {
  for_each = local.common_app_config

  source                   = "./modules/application_service"
  app_name                 = each.key
  app_version              = each.value.version
  app_port                 = each.value.port
  base_install_path        = "${path.cwd}/generated_environment/services"
  global_message_from_root = var.mensaje_global # Pasar la variable sensible
  python_exe               = var.python_executable
}

output "detalles_apps_simuladas" {
  value = {
    for k, app_instance in module.simulated_apps : k => {
      config_path  = app_instance.service_config_path
      install_path = app_instance.service_install_path
      # metadata    = app_instance.service_metadata_content # Puede ser muy verboso
      metadata_id = app_instance.service_metadata_content.uniqueId
    }
  }
  sensitive = true # Porque contiene mensaje_global (indirectamente)
}

resource "null_resource" "validate_all_configs" {
  depends_on = [module.simulated_apps] # Asegura que las apps se creen primero
  triggers = {
    # Re-validar si cualquier output de las apps cambia (muy general, pero para el ejemplo)
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  provisioner "local-exec" {
    command = "${var.python_executable} ${path.cwd}/scripts/python/validate_config.py ${path.cwd}/generated_environment/services"
    # Opcional: ¿qué hacer si falla?
    # on_failure = fail # o continue
  }
}

resource "null_resource" "check_all_healths" {
  depends_on = [null_resource.validate_all_configs] # Después de validar
  # Triggers similares o basados en los PIDs si los expusiéramos como output
  triggers = {
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  # Usar un bucle for para llamar al script de health check para cada servicio
  # Esto es un poco más avanzado con provisioners, una forma simple es invocar un script que lo haga internamente
  # O, si quisiéramos hacerlo directamente con N llamadas:
  # (Esto es solo ilustrativo, un script que itere sería mejor para muchos servicios)
  provisioner "local-exec" {
    when        = create # o always si se quiere
    command     = <<EOT
      for service_dir in $(ls -d ${path.cwd}/generated_environment/services/*/); do
        bash ${path.cwd}/scripts/bash/check_simulated_health.sh "$service_dir"
      done
    EOT
    interpreter = ["bash", "-c"]
  }
}

```

Notamos que aparecen varios errores en el momento de realizar `terraform apply`, pues nos resultan errores de ejecución en algunos recursos. En varios de los recursos a ejecutarse los errores son unicamente en la ruta de estos. El error con mayor dificultad de corrección ha sido el corregir la lectura de `modules/environment_setup/scripts/initial_setup.sh`. Pues se estaba ejecutando desde el directorio `/generated_environment/`

```bash
Apply complete! Resources: 10 added, 0 changed, 10 destroyed.

Outputs:

detalles_apps_simuladas = <sensitive>
id_entorno = "a826b6ff938e2d23"
readme_principal = "/home/amirmiir/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local/generated_environment/desarrollo_data/README.md"
ruta_bienvenida = "/home/amirmiir/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local/generated_environment/bienvenida.txt"
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ 

```



---

## Ejercicios

### Ejercicio 1

### Ejercicio 2

### Ejercicio 3: **Ejercicio de idempotencia y scripts externos:**

Para esta tarea vamos a modificar la carpeta `modules/environment_setup/scripts/initial_setup.sh`, cuyo estado inicial es el siguiente:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/environment_setup/scripts/initial_setup.sh 
#!/bin/bash
# Script: initial_setup.sh
ENV_NAME=$1
README_PATH=$2
echo "Ejecutando setup inicial para el entorno: $ENV_NAME"
echo "Fecha de setup: $(date)" > setup_log.txt
echo "Readme se encuentra en: $README_PATH" >> setup_log.txt
echo "Creando archivo de placeholder..."
touch placeholder_$(date +%s).txt
echo "Setup inicial completado."
# Simular más líneas de código
for i in {1..20}; do
    echo "Paso de configuración simulado $i..." >> setup_log.txt
    # sleep 0.01 # Descomenta para simular trabajo
done

```

Entonces procedemos a implementar el algoritmo para contar:

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ cat modules/environment_setup/scripts/initial_setup.sh 
#!/bin/bash
# Script: initial_setup.sh
# Uso: initial_setup.sh <ENV_NAME> <README_PATH>

ENV_NAME=$1
README_PATH=$2

CONTROL_FILE="placeholder_control.txt"
COUNTER_FILE="setup_run_count.txt"

echo "Ejecutando setup inicial para entorno: $ENV_NAME"

# Si el control ya existe, salimos silenciosamente (idempotencia)
if [[ -f "$CONTROL_FILE" ]]; then
  echo "Encontrado $CONTROL_FILE → nada que hacer."
  exit 0
fi

echo "Control no encontrado; ejecutando acciones iniciales…"

# Acción real solo la primera vez
echo "Creando $CONTROL_FILE y placeholder_*.txt"
touch "$CONTROL_FILE"
touch "placeholder_$(date +%s).txt"

# Registrar en log estándar
echo "Fecha de setup: $(date)" > setup_log.txt
echo "README se encuentra en: $README_PATH"  >> setup_log.txt

# Algoritmo: incrementar contador de ejecuciones
if [[ -f "$COUNTER_FILE" ]]; then
  count=$(<"$COUNTER_FILE")
  ((count++))
else
  count=1
fi
echo "$count" > "$COUNTER_FILE"
echo "Ejecuciones acumuladas: $count" >> setup_log.txt

# Simular pasos extra
for i in {1..20}; do
  echo "Paso simulado $i…" >> setup_log.txt
done

echo "Setup inicial COMPLETADO."
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ 

```

Y añadimos una variable tal que de esta dependa la ejecución y podamos identificarla (y forzar un cambio de versión) `variables.tf`

```bash
variable "setup_revision" {
  description = "Revisión del setup inicial; cambia su valor para forzar la re-ejecución."
  type        = string
  default     = "v1"
}
```

Esta la implementamos en el main del modulo environment_setup:

```bash
resource "null_resource" "ejecutar_setup_inicial" {
  depends_on = [local_file.readme_entorno]

  triggers = {
    readme_md5     = local_file.readme_entorno.content_md5
    setup_revision = var.setup_revision # ← nuevo
    script_sha256  = filesha256("${path.module}/scripts/initial_setup.sh")
  }

  provisioner "local-exec" {
    command     = "bash ${abspath("${path.module}/scripts/initial_setup.sh")} '${var.nombre_entorno_modulo}' '${local_file.readme_entorno.filename}'"
    interpreter = ["bash", "-c"]
    working_dir = "${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
}

```

El resultado de idempotencia se ve en la ejecución de `terraform apply`, en la creación de `generated_environment/desarrollo_data/placeholder_1748971524.txt` , `generated_environment/desarrollo_data/placeholder_1748975553.txt` y `generated_environment/desarrollo_data/placeholder_control.txt`

```bash
amirmiir@zenbook14-aacg-EndOS:~/Escritorio/.UNI/CC3S2-SD-251/Actividad19/Proyecto_iac_local(main)$ tree generated_environment/
generated_environment/
├── bienvenida.txt
├── desarrollo_data
│   ├── placeholder_1748971524.txt
│   ├── placeholder_1748975553.txt
│   ├── placeholder_control.txt
│   ├── README.md
│   ├── setup_log.txt
│   └── setup_run_count.txt
└── services
    ├── app1_v1.0.2
    │   ├── app1.pid
    │   ├── config.json
    │   ├── logs
    │   │   ├── app1_startup.log
    │   │   └── app1_v1.0.2_health.log
    │   └── metadata_generated.json
    └── app2_v0.5.0
        ├── app2.pid
        ├── config.json
        ├── logs
        │   ├── app2_startup.log
        │   └── app2_v0.5.0_health.log
        └── metadata_generated.json

7 directories, 17 files

```



### Ejercicio 4
