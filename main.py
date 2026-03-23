from _env import SSID, PASSWORD, HOSTNAME, ACCESS_POINT_SSID
from microdot import Microdot
from screen import Screen
import network, asyncio
from animations._colors import * 

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
    
    attempts = 1
    while not wifi.isconnected() and attempts < 5:
        attempts += 1
        await asyncio.sleep(3)

    if wifi.isconnected():
        print(f"Connected to '{SSID}' successfully! My IP is: {wifi.ipconfig('addr4')[0]}")
        loading.cancel()
        await SUCCESS(screen)
    else: 
        print(f"Could not reach '{SSID}', creating access-point...")
        ap = network.WLAN(network.WLAN.IF_AP)
        ap.active(True)
        ap.config(ssid=ACCESS_POINT_SSID)

        print(f"Successfully created access-point! My SSID is: '{ACCESS_POINT_SSID}'")
        loading.cancel()
        del wifi
        await SUCCESS_ALT(screen)


async def main():
    from animations.testingAllColors import TESTING_ALL_COLORS
    from animations.diceRoll import DICE_ROLL

    await setupWifi()

    @app.get("/")
    async def index(response):
        from animations.colorNoise import COLOR_NOISE
        await screen.animate(COLOR_NOISE, screen)
        return "hi", 200
    
    

    @app.route("/brightness", methods=["GET"])
    def getBrightness(request):
        return { "value": screen.brightness }, 200

    @app.route("/brightness", methods=["POST"])
    def setBrightness(request):
        data = request.json

        if not data or "value" not in data:
            return { "error": "Invalid request" }, 400
        
        if not isinstance(data["value"], float) or data["value"] < 0.0 or data["value"] > 1.0:
            return { "error" : "value must be float and between >0.1 and <1.0" }, 400
        
        screen.brightness = data["value"] 
        
        return { "status": "success" }, 200
    


    @app.route("/animation", methods=["GET"])
    def getAnimaton(request):
        return { "animation": screen.animation }

    @app.route("/animation", methods=["POST"])
    async def setAnimaton(request):
        from animations._animations import animations

        data = request.json

        if not data or "animation" not in data:
            return { "error": "Invalid request" }, 400
        
        if not isinstance(data["animation"], str) or data["animation"] not in animations:
            return { "error": "Animation not found" }, 400
        
        for animation in animations:
            if str(animation) == data["animation"]:
                await screen.animate(animation, screen) 
        
        return { "status": "success" }, 200
        

    
    @app.get("/test")
    async def test(response):
        await screen.animate(TESTING_ALL_COLORS, screen)
        return "quarter brightness", 200

    @app.get("/uwu")
    def uwu(response):
        actual = screen.normalise(screen.test, hflip=True)
        for i in range(len(actual)):
            screen.np[i] = screen.dim(BLANK if actual[i] == 0 else WHITE)
        screen.write()
        return "uwu", 200
    

    @app.get("/rtd")
    async def rollTheDice(response):
        await screen.animate(DICE_ROLL, screen)
        return "wow it works??", 200

            
    await app.start_server(port=80)


asyncio.run(main())