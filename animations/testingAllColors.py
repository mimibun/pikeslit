from animations._colors import *
async def TESTING_ALL_COLORS(screenObj):
    import asyncio

    while True:
        for color in [
            RED,
            GREEN,
            BLUE,
            VIOLET,
            YELLOW,
            WHITE,
            CYAN
        ]:
            screenObj.setAll(color)
            await asyncio.sleep(3)