import asyncio

class Screen:
    def __init__(self, pin=4, amountLeds=256) -> None:
        import neopixel, machine

        self.n = amountLeds
        self.np = neopixel.NeoPixel(machine.Pin(pin), amountLeds)

        self.brightness = 0.5

        self.buffer = []
        self.animation = None
        
        self.test = [
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
        ]

    def setBrightness(self, brightness: float):
        self.brightness = brightness if brightness >= 0 and brightness <= 1 else self.brightness

    def dim(self, color):
        return tuple(int(c * self.brightness) for c in color)

    def write(self):
        self.np.write()
    
    def clearAll(self):
        from animations._colors import BLANK
        self.np.fill(BLANK)
        self.write()
    
    def clearBuffer(self):
        from animations._colors import BLANK
        self.np.fill(BLANK)

    def setAll(self, color: tuple):
        self.np.fill(tuple(int(c * self.brightness) for c in color))
        self.write()

    def setSingle(self, position: int, color: tuple):
        self.np[position] = tuple(int(c * self.brightness) for c in color)
        self.write()

    def setMultiple(self, pixels: tuple, color: tuple):
        self.clearBuffer()
        for pixel in tuple(pixels):
            self.np[pixel] = color
        self.np.write()

    async def animate(self, animation, screenObj):
        self.clearAll()
        if self.animation != None:
            self.animation.cancel()
        self.animation = asyncio.create_task(animation(screenObj))

    def normalise(self, goodArray, hflip=False, yflip=False):
        normal = []

        for line in range(len(self.test[0])) if not hflip else reversed(range(len(self.test[0]))):
            for pixel in range(len(self.test)) if line % 2 == 0 else reversed(range(len(self.test))) if not yflip else range(len(self.test)) if line % 2 != 0 else reversed(range(len(self.test))):
                normal.append(goodArray[pixel][line])

        return normal