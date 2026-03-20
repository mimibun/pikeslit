async def COLOR_NOISE(screenObj):
    import random, asyncio

    while True:
        screenObj.setSingle(random.randint(0, screenObj.n - 1), tuple(random.randint(2,255) for i in range(3)))
        await asyncio.sleep_ms(50)