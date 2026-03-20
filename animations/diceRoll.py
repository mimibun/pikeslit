async def DICE_ROLL(screenObj):
    import random, asyncio

    result = random.randint(0,5)

    screenObj.clearAll()
    EYES = [
        tuple([4]),
        (2,6),
        (0,4,8),
        (0,2,6,8),
        (0,2,4,6,8),
        (0,2,3,5,6,8)
    ]

    for _ in range(12):
        screenObj.setMultiple(EYES[random.randint(0,5)], screenObj.COLOUR("red"))
        await asyncio.sleep_ms(150)

    screenObj.clearAll()
    await asyncio.sleep_ms(300)
    for pixel in EYES[result]:
        screenObj.np[pixel] = screenObj.COLOUR("red")

    screenObj.write()