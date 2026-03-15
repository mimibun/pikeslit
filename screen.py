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
    
    def clearBuffer(self):
        self.np.fill(self.toGRB((0,0,0)))

    def setAll(self, color: tuple):
        self.np.fill(self.toGRB(tuple(int(c * self.brightness) for c in color)))
        self.write()

    def setSingle(self, position: int, color: tuple):
        self.np[position] = self.toGRB(tuple(int(c * self.brightness) for c in color))
        self.write()

    def setMultiple(self, pixels: tuple, color: tuple):
        self.clearBuffer()
        for pixel in tuple(pixels):
            self.np[pixel] = color
        self.np.write()


    def COLOUR(self, colorString: str):
        colorString = colorString.lower()
        color = (0,0,0)

        if colorString == "red": color = (255,0,0)
        elif colorString == "green": color = (0,255,0)
        elif colorString == "blue": color = (0,0,255)
        elif colorString == "violet": color = (255,0,255)
        elif colorString == "cyan": color = (0,255,255)
        elif colorString == "yellow": color = (255,255,0)
        elif colorString == "white": color = (255,255,255)
        else: color = (255,255,255)

        return self.toGRB(color)




    async def animate(self, animation):
        self.clearAll()
        if self.animation != None:
            self.animation.cancel()
        self.animation = asyncio.create_task(animation())

    async def COLOR_NOISE(self):
        import random

        while True:
            self.setSingle(random.randint(0, self.n - 1), tuple(random.randint(2,255) for i in range(3)))
            await asyncio.sleep_ms(100)

    async def LOADING(self):
        while True:
            for i in [0,1]:
                for led in range(self.n) if i % 2 == 0 else reversed(range(self.n)):
                    self.clearAll()
                    self.setSingle(led, (20,20,20))
                    await asyncio.sleep_ms(100)

    async def SUCCESS(self):
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
            tuple([4]),
            (2,6),
            (0,4,8),
            (0,2,6,8),
            (0,2,4,6,8),
            (0,2,3,5,6,8)
        ]

        for _ in range(12):
            self.setMultiple(EYES[random.randint(0,5)], self.COLOUR("red"))
            await asyncio.sleep_ms(150)

        self.clearAll()
        await asyncio.sleep_ms(300)
        for pixel in EYES[result]:
            self.np[pixel] = self.COLOUR("red")

        self.write()