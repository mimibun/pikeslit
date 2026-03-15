from _env import SSID, PASSWORD, HOSTNAME
from microdot import Microdot
from screen import Screen
import network, asyncio

screen = Screen()
screen.setBrightness(0.05)
app = Microdot()

async def connectToWifi():
    async def setupWifi():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        print(f"Connecting as '{HOSTNAME}' to '{SSID}'...")
        wlan.connect(SSID, PASSWORD) if PASSWORD != "" else wlan.connect(SSID)
        
        while not wlan.isconnected():
            await asyncio.sleep(15)

        print(f"Connected! My IP is: {wlan.ipconfig('addr4')[0]}")

    loading = asyncio.create_task(screen.animate(screen.LOADING))
    await setupWifi()
    loading.cancel()
    await screen.animate(screen.SUCCESS)

async def main():
    await connectToWifi()

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