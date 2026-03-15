import asyncio

class Screen:
    def __init__(self, pin=4, amountLeds=9) -> None:
        import neopixel, machine

        self.n = amountLeds
        self.np = neopixel.NeoPixel(machine.Pin(pin), amountLeds)

        self.brightness = 0.5

        self.animation = None

    def setBrightness(self, brightness: float):
        self.brightness = brightness if brightness >= 0 and brightness <= 1 else self.brightness

    def toGRB(self, color: tuple):
        return ((color[1], color[0], color[2]))
    
    def write(self):
        self.np.write()
    

    
    def clearAll(self):
        self.np.fill(self.toGRB((0,0,0)))
        self.write()

    def setAll(self, color: tuple):
        self.np.fill(self.toGRB(tuple(int(c * self.brightness) for c in color)))
        self.write()

    def setSingle(self, position: int, color: tuple):
        self.np[position] = self.toGRB(tuple(int(c * self.brightness) for c in color))
        self.write()



    async def animate(self, animation):
        self.clearAll()
        if self.animation != None:
            self.animation.cancel()
        self.animation = asyncio.create_task(animation())


    async def COLOR_NOISE(self):
        import random, asyncio

        while True:
            self.setSingle(random.randint(0, self.n - 1), tuple(random.randint(2,255) for i in range(3)))
            await asyncio.sleep_ms(100)

    async def LOADING(self):
        import asyncio

        while True:
            for i in [0,1]:
                for led in range(self.n) if i % 2 == 0 else reversed(range(self.n)):
                    self.clearAll()
                    self.setSingle(led, (20,20,20))
                    await asyncio.sleep(0.1)

    async def SUCCESS(self):
        import asyncio

        for _ in range(2):
            self.clearAll()
            self.setAll((0,255,0))
            await asyncio.sleep_ms(200)
            self.clearAll()
            await asyncio.sleep_ms(200)

    async def DICE_ROLL(self):
        import random

        result = random.randint(0,5)

        self.clearAll()
        EYES = [
            (4),
            (2,6),
            (0,4,8),
            (0,2,6,8),
            (0,2,4,6,8),
            (0,2,3,5,6,8)
        ]

        print(result)
        if result != 0:
            for pixel in EYES[result]:
                self.np[pixel] = self.toGRB((20,0,0))
        else: self.np[4] = self.toGRB((20,0,0))
        

        self.write()