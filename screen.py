import asyncio

class Screen:
    def __init__(self, pin=4, amountLeds=256) -> None:
        import neopixel, machine

        self.n = amountLeds
        self.np = neopixel.NeoPixel(machine.Pin(pin), amountLeds)

        self.brightness = 0.5

        self.buffer = []
        self.animation = None

    def setBrightness(self, brightness: float):
        self.brightness = brightness if brightness >= 0 and brightness <= 1 else self.brightness






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

    async def animate(self, animation):
        self.clearAll()
        if self.animation != None:
            self.animation.cancel()
        self.animation = asyncio.create_task(animation())