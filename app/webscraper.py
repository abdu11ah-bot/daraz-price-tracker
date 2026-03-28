from playwright.sync_api import sync_playwright
import logging


def Webscraper(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ))
        try:
            page.goto(url, timeout=20000)
            page.wait_for_selector(".pdp-mod-product-badge-title", timeout=15000)

            name = page.locator(".pdp-mod-product-badge-title").first.inner_text()
            price = (
                page.locator(".pdp-price").first.inner_text()
                .replace("৳", "")
                .replace(",", "")
                .strip()
            )

            logging.info(f"Scraped — Name: {name} | Price: {price}")
            return [name, price]

        except Exception as e:
            logging.error(f"Webscraper error for {url}: {e}")
            return None

        finally:
            browser.close()