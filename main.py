from _env import SSID, PASSWORD, HOSTNAME
from microdot import Microdot
from screen import Screen
import network, asyncio

screen = Screen()
screen.setBrightness(0.05)
app = Microdot()

async def connectToWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print(f"Connecting as '{HOSTNAME}' to '{SSID}'...")
    wlan.connect(SSID, PASSWORD) if PASSWORD != "" else wlan.connect(SSID)
    
    while not wlan.isconnected():
        await asyncio.sleep(3)

    print(f"Connected! My IP is: {wlan.ipconfig('addr4')[0]}")

async def main():
    loading = asyncio.create_task(screen.LOADING())
    await connectToWifi()
    loading.cancel()
    await screen.animate(screen.SUCCESS)

    @app.get("/")
    async def index(response):
        await screen.animate(screen.COLOR_NOISE)
        return "hi", 200
    

    @app.get("/rtd")
    async def rollTheDice(response):
        await screen.animate(screen.DICE_ROLL)
        return "wow it works??", 200

            
    await app.start_server(port=80)


asyncio.run(main())