from playwright.async_api import async_playwright, Route, Request
from random import randint
import traceback

async def save_resources(route: Route, request: Request):
    if request.resource_type in ["image", "media", "font"]:
        await route.abort()
    else:
        await route.continue_()
    

async def run_scrape(url, zipcode):
    pid = url.split('?')[0].split('/')[-1].split('-')[-1]
    async with async_playwright() as p:
        try:
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

            res = await page.goto(url, wait_until="domcontentloaded")

            if res.status == 404:
                return await page.content(), "", 404

            try:
                await page.wait_for_selector("button:has-text('Change')",timeout=10000)
                await page.locator("button:has-text('Change')").click()
            except Exception as ex:
                pass

            await page.wait_for_selector("label:has-text('Ship')")
            await page.locator("label").filter(has_text="Ship").first.click()            
            await page.wait_for_selector('input[name="zipCode"]')
            await page.locator('input[name="zipCode"]').first.fill(str(zipcode))
            await page.locator('button[aria-label="Save ZIP Code"]').first.click()
            main_page_content = await page.content()

            await page.locator(f'form[data-testid="add-to-cart-form-{pid}"] button').click()
            await page.wait_for_selector('button.add-to-cart__view-cart')
            await page.locator('button.add-to-cart__view-cart').first.click()

            await page.get_by_text("Order Summary").nth(1).hover()
            shipping_content = await page.content()

            return main_page_content, shipping_content, 200
        except Exception as ex:
            traceback.print_exc()
            await page.screenshot(path=f"htmls/{randint(0, 10000)}.jpeg", type="jpeg", full_page=True)
        
    
