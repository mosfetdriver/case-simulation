import asyncio
import websockets
import json

async def on_connect(websocket, path):
    print("Conexión establecida con el servidor OCPP")

    # Simulación de eventos de carga
    while True:
        try:
            # Generar datos de carga simulados
            charging_data = {
                "charging_state": "Charging",
                "current": round(random.uniform(5, 20), 2),
                "voltage": 230,
                "soc": round(random.uniform(10, 90), 2),
            }

            # Enviar datos al servidor OCPP
            await websocket.send(json.dumps(charging_data))

            # Simular intervalo de tiempo entre eventos
            await asyncio.sleep(5)
        except websockets.exceptions.ConnectionClosed:
            print("Conexión cerrada")
            break

# URL del servidor OCPP
ocpp_server_url = "ws://localhost:9000/ocpp/2.0"

# Iniciar el simulador y conectar al servidor OCPP
async def main():
    async with websockets.connect(ocpp_server_url) as websocket:
        await on_connect(websocket, "")

# Ejecutar el simulador
if __name__ == "__main__":
    asyncio.run(main())
