# Wan 2.2: video con IA

[Wan2.2](https://github.com/Wan-Video/Wan2.2) genera clips de video a partir de un texto o de una imagen. Hay dos formas de usarlo desde este repo:

| | En fal (pago) | En tu PC (gratis) |
|---|---|---|
| Script | `wan/fal.sh` | `wan/instalar-local.sh` y `wan/generar-local.sh` |
| Qué necesita | Una clave de fal en `FAL_KEY` | GPU NVIDIA de 24 GB o más (RTX 4090, 3090...), Linux o Windows con WSL2, unos 45 GB libres |
| Modelos | 5B (rápido, 24 fps) y A14B (mejor calidad) | 5B (TI2V-5B) |
| Dónde queda el video | `runs/<key>/assets/fal/` | `runs/wan/` |

`runs/` está ignorado en git, así que ningún video generado se sube solo al repo.

## En fal

```bash
npm install                                    # una vez: instala el CLI de open-edit
wan/fal.sh "pelota de pádel picando en el vidrio, cámara lenta, luz de atardecer"
wan/fal.sh "la jugadora saca y la cámara la sigue" --imagen assets/foto.png
wan/fal.sh "..." --modelo a14b --aspecto 16:9 --frames 81 --seed 3
wan/fal.sh "..." --dry                         # muestra el pedido sin gastar nada
```

- Por defecto: vertical 9:16, 720p, 5 segundos. Con `--imagen`, el formato sale de la imagen.
- Cada video se cobra en tu cuenta de fal. Al terminar, el CLI muestra el costo.
- El mismo pedido no se compra dos veces: si repetís exactamente el mismo prompt, te devuelve el video que ya tenías. Para otra variante, cambiá `--seed`.

## En tu PC (gratis)

```bash
wan/instalar-local.sh                          # una vez: código, dependencias y modelo (34 GB)
wan/generar-local.sh "pelota de pádel picando en el vidrio, cámara lenta"
wan/generar-local.sh "la jugadora saca" --imagen assets/foto.png
wan/generar-local.sh "..." --horizontal --frames 81 --seed 3
```

- Todo se instala en `~/wan2.2`, fuera del repo. Para usar otra carpeta, definí `WAN_HOME`.
- Por defecto el video sale vertical (704×1280), de 5 s a 24 fps. `--frames` tiene que ser 4n+1 (81, 121...).
- Usa las opciones de bajo consumo de memoria de Wan (`--offload_model`, `--t5_cpu`). Según Wan, un clip de 5 s en 720p tarda menos de 9 minutos en una placa de consumo como la 4090.
- En Windows, instalá [WSL2](https://learn.microsoft.com/es-es/windows/wsl/install) con Ubuntu y corré los scripts desde ahí. Con los drivers de NVIDIA de Windows alcanza.
- Si tu placa tiene menos de 24 GB, este modelo no entra.
