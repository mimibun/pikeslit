async def LOADING(screenObj):
    import asyncio
    from animations._colors import WHITE

    while True:
        for i in [0,1]:
            for led in range(screenObj.n) if i % 2 == 0 else reversed(range(screenObj.n)):
                screenObj.clearAll()
                screenObj.setSingle(led, WHITE)
                await asyncio.sleep_ms(100)