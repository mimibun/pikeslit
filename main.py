from _env import SSID, PASSWORD, HOSTNAME, ACCESS_POINT_SSID
from microdot import Microdot
from screen import Screen
import network, asyncio

screen = Screen()
screen.setBrightness(0.05)
app = Microdot()

async def setupWifi():
    from animations.loading import LOADING
    from animations.success import SUCCESS
    from animations.success_alt import SUCCESS_ALT

    loading = asyncio.create_task(LOADING(screen))

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    print(f"Attempting to connect as '{HOSTNAME}' to '{SSID}'...")
    wifi.connect(SSID, PASSWORD) if PASSWORD != "" else wifi.connect(SSID)
    
    attempts = 0
    while not wifi.isconnected() or attempts < 30:
        attempt += 1
        await asyncio.sleep(3)

    if wifi.isconnected():
        print(f"Connected to '{SSID}' successfully! My IP is: {wifi.ipconfig('addr4')[0]}")
        loading.cancel()
        await screen.animate(SUCCESS(screen))
    else: 
        wifi.active(False)
        print(f"Could not reach '{SSID}', creating access-point...")
        ap = network.WLAN(network.WLAN.IF_AP)
        ap.active(True)
        ap.config(ssid=ACCESS_POINT_SSID)

        if ap.isconnected():
            print(f"Successfully created access-point! My SSID is: '{ACCESS_POINT_SSID}'")
            loading.cancel()
            await screen.animate(SUCCESS(screen))
        else:
            print(f"Could not create access-point! Check your '_env.py' file :)")
            loading.cancel()
            await screen.animate(SUCCESS_ALT(screen))


async def main():
    from animations.loading import LOADING
    from animations.success import SUCCESS
    from animations.testingAllColors import TESTING_ALL_COLORS
    from animations.diceRoll import DICE_ROLL

    await setupWifi()

    @app.get("/")
    async def index(response):
        from animations.colorNoise import COLOR_NOISE
        await screen.animate(COLOR_NOISE(screen))
        return "hi", 200
    
    @app.get("/full")
    def full(response):
        screen.setBrightness(1.0)
        return "full brightness", 200
    
    @app.get("/half")
    def half(response):
        screen.setBrightness(0.5)
        return "half brightness", 200
    
    @app.get("/quarter")
    def quarter(response):
        screen.setBrightness(0.25)
        return "quarter brightness", 200
    
    @app.get("/test")
    async def test(response):
        await screen.animate(TESTING_ALL_COLORS(screen))
        return "quarter brightness", 200
    

    @app.get("/rtd")
    async def rollTheDice(response):
        await screen.animate(DICE_ROLL(screen))
        return "wow it works??", 200

            
    await app.start_server(port=80)


asyncio.run(main())