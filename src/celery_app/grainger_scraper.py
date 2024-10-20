from playwright.async_api import async_playwright, Route, Request

async def save_resources(route: Route, request: Request):
    if request.resource_type in ["image", "media", "font"]:
        await route.abort()
    else:
        await route.continue_()
    

async def run_scrape(url, zipcode):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, proxy={
            "server": "geo.iproyal.com:12321",
            "username": "RAD5VCH0WnT6glQG",
            "password": "uJUnzLRMv5c5Ap0Z"
        })
        ctx = await browser.new_context()
        await ctx.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        page = await ctx.new_page()

        # await page.route("*/**", save_resources)

        res = await page.goto(url)

        if res.status == 404:
            return await page.content(), "", 404

        await page.get_by_test_id("rta-options-list").locator("span").nth(2).click()
        await page.get_by_text("Ship", exact=True).click()

        await page.locator("label").filter(has_text="Ship").click()
        await page.get_by_test_id("rta-zip-input").click()
        await page.get_by_test_id("rta-zip-input").fill(str(zipcode))
        await page.get_by_test_id("button-zip-code-form").click()
        main_page_content = await page.content()

        await page.get_by_test_id("button-add-to-cart-2082676").click()
        await page.get_by_text("View Cart").click()
        await page.get_by_text("Order Summary").nth(1).hover()
        shipping_content = await page.content()

        return main_page_content, shipping_content, 200
    
