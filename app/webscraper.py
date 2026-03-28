from playwright.sync_api import sync_playwright
import logging


def Webscraper(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )
        page = context.new_page()
        try:
            # Use domcontentloaded instead of full load — much faster, doesn't wait for ads/trackers
            page.goto(url, timeout=40000, wait_until="domcontentloaded")
            page.wait_for_selector(".pdp-mod-product-badge-title", timeout=20000)

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