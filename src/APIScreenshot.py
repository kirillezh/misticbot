class APIScreenshot:
    def __init__(self,browser = None):
        if browser != None:
            self.browser = browser
        
        self.mode = False
        self.darkmode()
        self.browser = None
        
    async def start(self):
        from pyppeteer import launch
        import logging
        self.browser = await launch(defaultViewport={
                "width": 1600,
                "height": 1200,
                "isMobile": False,
                "hasTouch":False,
                "isLandscape":False}, 
                logLevel = logging.WARNING, 
            options={'args': ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process', '--no-zygote']})
        
    def darkmode(self):
        import datetime
        from src.locales import GMT
        time_h = getattr(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=GMT*3600))), 'hour')
        if time_h in range(8, 22):
            self.mode = False
        else:
            self.mode = True

    async def screenshot_alert(self):
        if self.browser == None:
            await self.start()
        import asyncio
        from src.locales import URL
        page = await self.browser.newPage()
        await page.goto(URL)
        await page.evaluate("document.querySelector('html').className = '"+ ('black-preset' if self.darkmode() else 'light') +" menu-hidden'")
        await asyncio.sleep(3)
        await page.screenshot({'path': 'screenshot.png'})
        await page.close()
        return 'screenshot.png'
    