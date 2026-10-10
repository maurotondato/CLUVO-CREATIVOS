#!/usr/bin/env bash
# Instala Wan2.2 (modelo TI2V-5B) para generar videos gratis en tu propia PC.
# Necesita: GPU NVIDIA de 24 GB o más, Linux (o Windows con WSL2), Python 3.10–3.12,
# git y unos 45 GB libres. Todo queda en $WAN_HOME (por defecto ~/wan2.2), fuera de este repo.
#
#   wan/instalar-local.sh              código + dependencias + modelo (34 GB)
#   wan/instalar-local.sh --sin-modelo código + dependencias; el modelo se baja después
#
# Se puede volver a correr: lo que ya está instalado se saltea y la descarga se retoma.
set -euo pipefail

WAN_HOME="${WAN_HOME:-$HOME/wan2.2}"
WAN_COMMIT=1ea34ff48f87168174e12956e200b1d908b1c5ff   # Wan2.2, 21/09/2026
REPO="$WAN_HOME/Wan2.2"
VENV="$WAN_HOME/venv"
MODELO="$WAN_HOME/Wan2.2-TI2V-5B"

con_modelo=1
case "${1:-}" in
  "") ;;
  --sin-modelo) con_modelo=0 ;;
  -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) echo "Opción desconocida: $1 (usá --sin-modelo o --help)" >&2; exit 1 ;;
esac

paso() { printf '\n==> %s\n' "$*"; }
falla() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

paso "GPU"
command -v nvidia-smi >/dev/null || falla "no se encontró nvidia-smi. Wan2.2 necesita una GPU NVIDIA con los drivers instalados (en WSL2, los drivers de Windows alcanzan)."
gpu="$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | head -1)"
vram="${gpu##*, }"
echo "$gpu MiB"
if ((vram < 23000)); then
  echo "AVISO: el modelo TI2V-5B pide 24 GB de VRAM y esta placa tiene ${vram} MiB. Puede quedarse sin memoria."
fi

paso "Disco"
mkdir -p "$WAN_HOME"
libre_gb=$(df -Pk "$WAN_HOME" | awk 'NR==2 {print int($4 / 1024 / 1024)}')
ya_gb=$(du -sk "$WAN_HOME" | awk '{print int($1 / 1024 / 1024)}')   # lo que ya se bajó en una corrida anterior
necesario_gb=$(((con_modelo ? 45 : 12) - ya_gb))
echo "${libre_gb} GB libres en $WAN_HOME"
((libre_gb >= necesario_gb)) || falla "hacen falta unos ${necesario_gb} GB libres."

paso "Python"
PY=""
for p in python3.12 python3.11 python3.10; do
  if command -v "$p" >/dev/null; then PY="$p"; break; fi
done
[[ -n "$PY" ]] || falla "hace falta Python 3.10, 3.11 o 3.12 (con 3.13 no hay binarios de numpy<2). En Ubuntu: sudo apt install python3.12 python3.12-venv"
echo "$($PY --version)"

paso "Código de Wan2.2"
if [[ ! -d "$REPO/.git" ]]; then
  git clone https://github.com/Wan-Video/Wan2.2.git "$REPO"
fi
git -C "$REPO" fetch --quiet origin "$WAN_COMMIT" 2>/dev/null || true
git -C "$REPO" checkout --quiet "$WAN_COMMIT"
echo "$REPO @ ${WAN_COMMIT:0:7}"

paso "Entorno virtual y dependencias"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$PY" -m venv "$VENV" || falla "no se pudo crear el venv. En Ubuntu: sudo apt install ${PY}-venv"
fi
"$VENV/bin/python" -m pip install --upgrade pip wheel setuptools
# torch 2.8 trae CUDA 12.8 y tiene flash-attn precompilado: no hace falta compilar nada.
# Las restricciones evitan que el resto de las dependencias suba torch a otra versión.
printf '%s\n' torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 > "$WAN_HOME/restricciones.txt"
pip=("$VENV/bin/python" -m pip install -c "$WAN_HOME/restricciones.txt")
"${pip[@]}" torch torchvision torchaudio
cp="cp$("$VENV/bin/python" -c 'import sys; print(f"{sys.version_info[0]}{sys.version_info[1]}")')"
"${pip[@]}" "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiTRUE-${cp}-${cp}-linux_x86_64.whl"
grep -v '^flash_attn' "$REPO/requirements.txt" > "$WAN_HOME/requirements-sin-flash.txt"
"${pip[@]}" -r "$WAN_HOME/requirements-sin-flash.txt" "huggingface_hub[cli]"
"$VENV/bin/python" -c 'import torch, flash_attn; print("torch", torch.__version__, "| CUDA disponible:", torch.cuda.is_available(), "| flash_attn", flash_attn.__version__)'

if ((con_modelo)); then
  paso "Modelo Wan2.2-TI2V-5B (34 GB)"
  if [[ -f "$MODELO/.descarga-completa" ]]; then
    echo "ya descargado"
  else
    if [[ -x "$VENV/bin/hf" ]]; then
      "$VENV/bin/hf" download Wan-AI/Wan2.2-TI2V-5B --local-dir "$MODELO"
    else
      "$VENV/bin/huggingface-cli" download Wan-AI/Wan2.2-TI2V-5B --local-dir "$MODELO"
    fi
    touch "$MODELO/.descarga-completa"
  fi
else
  echo
  echo "Modelo salteado. Para bajarlo después: wan/instalar-local.sh"
fi

paso "Listo"
echo "Generá con: wan/generar-local.sh \"tu prompt\""
