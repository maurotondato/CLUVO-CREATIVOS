import certifi, json
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import asyncio, edge_tts
lines = [
 "¿Tu club todavía se maneja con planillas y mensajes?",
 "Con Cluvo, tus socios reservan canchas en segundos,",
 "se anotan a clases y a torneos.",
 "Y vos controlás todo: caja, stock, pagos y reportes.",
 "Tenis, pádel, fútbol... se adapta a tu deporte.",
 "Cluvo. By Mok Lab.",
]
async def main():
    out = {}
    for i, t in enumerate(lines, 1):
        c = edge_tts.Communicate(t, "es-AR-TomasNeural", rate="+6%", pitch="-2Hz", boundary="WordBoundary")
        words = []
        with open(f"f{i}.mp3", "wb") as f:
            async for ch in c.stream():
                if ch["type"] == "audio": f.write(ch["data"])
                elif ch["type"] == "WordBoundary":
                    words.append([round(ch["offset"]/1e7,3), round((ch["offset"]+ch["duration"])/1e7,3), ch["text"]])
        out[f"f{i}"] = words
    json.dump(out, open("words.json","w"), ensure_ascii=False, indent=1)
asyncio.run(main())
