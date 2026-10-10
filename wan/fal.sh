#!/usr/bin/env bash
# Genera un video con Wan 2.2 en fal (se cobra en tu cuenta de fal, no en VEED).
# Usa el CLI de open-edit, que sube imágenes locales, descarga el resultado y
# no compra dos veces el mismo pedido.
#
#   wan/fal.sh "prompt" [--imagen foto.png] [--modelo 5b|a14b] [--aspecto 9:16|16:9|1:1]
#              [--frames N] [--resolucion 720p|580p|480p] [--seed N] [--key nombre] [--dry]
set -euo pipefail

uso() {
  sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

prompt=""
imagen=""
modelo="5b"
aspecto=""
frames=""
resolucion="720p"
seed=""
key="wan"
dry=0

while (($#)); do
  case "$1" in
    --imagen) imagen="$2"; shift 2 ;;
    --modelo) modelo="$2"; shift 2 ;;
    --aspecto) aspecto="$2"; shift 2 ;;
    --frames) frames="$2"; shift 2 ;;
    --resolucion) resolucion="$2"; shift 2 ;;
    --seed) seed="$2"; shift 2 ;;
    --key) key="$2"; shift 2 ;;
    --dry) dry=1; shift ;;
    -h|--help) uso ;;
    -*) echo "Opción desconocida: $1" >&2; uso 1 ;;
    *) prompt="$1"; shift ;;
  esac
done

[[ -n "$prompt" ]] || { echo "Falta el prompt." >&2; uso 1; }

case "$modelo" in
  5b) frames="${frames:-121}" ;;   # 121 cuadros a 24 fps = 5 s
  a14b) frames="${frames:-81}" ;;  # 81 cuadros a 16 fps = 5 s
  *) echo "--modelo tiene que ser 5b o a14b" >&2; exit 1 ;;
esac

if [[ -n "$imagen" ]]; then
  tarea="image-to-video"
  aspecto="${aspecto:-auto}"
  # Una ruta local se pasa absoluta; open-edit la sube a fal.
  [[ "$imagen" =~ ^https?:// ]] || imagen="$(realpath "$imagen")"
else
  tarea="text-to-video"
  aspecto="${aspecto:-9:16}"
fi

if ((!dry)) && [[ -z "${FAL_KEY:-}" && -z "${OPEN_EDIT_FAL_KEY_FILE:-}" ]]; then
  echo "Falta FAL_KEY. Cargala como variable de entorno (o OPEN_EDIT_FAL_KEY_FILE con la ruta a un archivo que la tenga)." >&2
  exit 1
fi

cd "$(dirname "$0")/.."
run="runs/$key"
mkdir -p "$run"
entrada="$run/wan-$(date +%Y%m%d-%H%M%S).json"

PROMPT="$prompt" IMAGEN="$imagen" ASPECTO="$aspecto" FRAMES="$frames" \
RESOLUCION="$resolucion" SEED="$seed" node -e '
  const e = process.env;
  const input = {
    prompt: e.PROMPT,
    aspect_ratio: e.ASPECTO,
    num_frames: Number(e.FRAMES),
    resolution: e.RESOLUCION,
  };
  if (e.IMAGEN) input.image_url = e.IMAGEN;
  if (e.SEED) input.seed = Number(e.SEED);
  console.log(JSON.stringify(input, null, 2));
' > "$entrada"

cmd=(npx --yes @veedstudio/openedit-cli fal run "fal-ai/wan/v2.2-$modelo/$tarea" --input "@$entrada" --run "$run")

if ((dry)); then
  cat "$entrada"
  printf '%q ' "${cmd[@]}"; echo
  rm -f "$entrada"
  exit 0
fi

"${cmd[@]}"
