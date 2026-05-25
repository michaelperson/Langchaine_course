#!/usr/bin/env bash
# ===================================================================
# lock.sh - Genere un requirements.lock.txt deterministe
# ===================================================================
# A executer UNE FOIS apres un build qui fonctionne, pour figer la
# version exacte de TOUTES les dependances (directes + transitives :
# numpy, torch, transformers, etc.).
#
# Usage :
#   bash infrastructure/lock.sh
#
# Le Dockerfile detecte automatiquement requirements.lock.txt
# et l'utilise en priorite si present.
# ===================================================================

set -euo pipefail

CONTAINER="formation-langchain-app"
OUTFILE="$(dirname "$0")/requirements.lock.txt"

# Verifier que le conteneur tourne
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "ERREUR : conteneur '${CONTAINER}' non demarre." >&2
  echo "Lance d'abord : docker compose -f infrastructure/docker-compose.yml up -d" >&2
  exit 1
fi

echo "[lock.sh] Generation du lock depuis ${CONTAINER}..."

# pip freeze --exclude-editable : evite les chemins locaux non portables
# Header informatif en tete du fichier
{
  echo "# ============================================================"
  echo "# requirements.lock.txt - GENERE AUTOMATIQUEMENT par lock.sh"
  echo "# Date  : $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "# Source: pip freeze dans ${CONTAINER}"
  echo "# NE PAS EDITER A LA MAIN - regenerer via : bash infrastructure/lock.sh"
  echo "# ============================================================"
  docker exec "${CONTAINER}" pip freeze --exclude-editable
} > "${OUTFILE}"

LINES=$(grep -cv '^#' "${OUTFILE}" || true)
echo "[lock.sh] OK - ${LINES} paquets pinnes dans ${OUTFILE}"
echo "[lock.sh] Pense a commiter ce fichier dans git."
