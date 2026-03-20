async def SUCCESS_ALT(screenObj):
    import asyncio
    from animations import _colors as colors

    for _ in range(2):
        screenObj.clearAll()
        screenObj.setAll(colors.YELLOW)
        await asyncio.sleep_ms(200)
        screenObj.clearAll()
        await asyncio.sleep_ms(200)