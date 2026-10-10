#!/usr/bin/env bash
# Genera un video con Wan2.2 TI2V-5B en tu GPU (gratis). Antes: wan/instalar-local.sh
#
#   wan/generar-local.sh "prompt" [--imagen foto.png] [--horizontal] [--frames N]
#                        [--pasos N] [--seed N] [--salida archivo.mp4]
#
# Por defecto: vertical 704x1280 (para reels), 121 cuadros = 5 s a 24 fps,
# y la salida va a runs/wan/ dentro de este repo.
set -euo pipefail

WAN_HOME="${WAN_HOME:-$HOME/wan2.2}"
REPO="$WAN_HOME/Wan2.2"
VENV="$WAN_HOME/venv"
MODELO="$WAN_HOME/Wan2.2-TI2V-5B"

uso() {
  sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

prompt=""
imagen=""
size="704*1280"
frames=121
pasos=""
seed=-1
salida=""

while (($#)); do
  case "$1" in
    --imagen) imagen="$(realpath "$2")"; shift 2 ;;
    --horizontal) size="1280*704"; shift ;;
    --frames) frames="$2"; shift 2 ;;
    --pasos) pasos="$2"; shift 2 ;;
    --seed) seed="$2"; shift 2 ;;
    --salida) salida="$(realpath -m "$2")"; shift 2 ;;
    -h|--help) uso ;;
    -*) echo "Opción desconocida: $1" >&2; uso 1 ;;
    *) prompt="$1"; shift ;;
  esac
done

[[ -n "$prompt" ]] || { echo "Falta el prompt." >&2; uso 1; }
((frames % 4 == 1)) || { echo "--frames tiene que ser 4n+1 (por ejemplo 81, 121)." >&2; exit 1; }
[[ -x "$VENV/bin/python" && -f "$MODELO/.descarga-completa" ]] || {
  echo "Wan2.2 no está instalado en $WAN_HOME. Corré primero: wan/instalar-local.sh" >&2
  exit 1
}

if [[ -z "$salida" ]]; then
  salida="$(cd "$(dirname "$0")/.." && pwd)/runs/wan/wan-local-$(date +%Y%m%d-%H%M%S).mp4"
fi
mkdir -p "$(dirname "$salida")"

args=(
  --task ti2v-5B
  --size "$size"
  --frame_num "$frames"
  --ckpt_dir "$MODELO"
  --offload_model True
  --convert_model_dtype
  --t5_cpu
  --base_seed "$seed"
  --prompt "$prompt"
  --save_file "$salida"
)
[[ -n "$imagen" ]] && args+=(--image "$imagen")
[[ -n "$pasos" ]] && args+=(--sample_steps "$pasos")

cd "$REPO"
"$VENV/bin/python" generate.py "${args[@]}"
echo "Video: $salida"
