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