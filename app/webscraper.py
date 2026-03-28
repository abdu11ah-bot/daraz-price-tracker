from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


def Webscraper(url):
    options = webdriver.ChromeOptions()  # type: ignore
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)  # type: ignore
    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "pdp-mod-product-badge-title")
            )
        )

        name = driver.find_element(
            By.CLASS_NAME, "pdp-mod-product-badge-title"
        ).text
        price = (
            driver.find_element(By.CLASS_NAME, "pdp-price")
            .text.replace("৳", "")
            .replace(",", "")
            .strip()
        )

        logging.info(f"Scraped — Name: {name} | Price: {price}")
        return [name, price]

    except Exception as e:
        logging.error(f"Webscraper error for {url}: {e}")
        return None

    finally:
        driver.quit()
