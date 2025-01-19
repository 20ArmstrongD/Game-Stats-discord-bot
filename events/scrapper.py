import logging
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# api_url = 'https://r6.tracker.network/r6siege/profile/ubi/r1bone/overview'

def get_playerdata(api_url):
    # Configure Firefox option for headless browsing (non-ui)
    options = Options()
    options.headless = True  # headless mode ON
    options.log.level = "trace"
    options.set_preference("gfx.webrender.enabled", False)
    options.set_preference("layers.acceleration.disabled", True)

    driver = None  # Initialize driver outside the try block
    elements = {}  # Initialize elements dictionary

    try:
        # Init the Firefox WebDriver using pointing to path for geckodriver
        service = Service('/home/DiscordPi/.wdm/drivers/geckodriver/linux64/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)

        # Navigate to the URL
        driver.get(api_url)

        # Wait for the page to load, in case of dynamic content
        driver.implicitly_wait(10)

        # Find the elements containing the player data
        try:
            logging.info(f"Looking For Player Data...")

            kd_element = driver.find_element(By.XPATH, "//span[contains(text(),'KD')]/following-sibling::span/span")
            level_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Level')]/span[@class='text-primary']")
            playtime_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Playtime')]/span[@class='text-primary']")
            # rank_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-20') and contains(@class, 'text-secondary')]")
            # ranked_kd_element = driver.find_element(By.XPATH, "//section[1]//div[3]//div[1]//div[2]//div[5]//span[2]/span")

            kd = kd_element.text if kd_element else None
            level = level_element.text if level_element else None
            playtime = playtime_element.text if playtime_element else None
            try:
                rank_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-20') and contains(@class, 'text-secondary')]")
                ranked_kd_element = driver.find_element(By.XPATH, "//section[1]//div[3]//div[1]//div[2]//div[5]//span[2]/span")
                # rank = rank_element.text if rank_element else None
                # ranked_kd = ranked_kd_element.text if ranked_kd_element else None
                rank = rank_element.text if rank_element else None
                ranked_kd = ranked_kd_element.text if ranked_kd_element else None
            except Exception as e:
                logging.warning("Ranked elements not found.")
                rank = None
                ranked_kd = None

            # Extract text from elements


            elements = {
                'KD': kd,
                'Level': level,
                'Playtime': playtime,
                'Rank': rank,
                'Ranked KD': ranked_kd
            }

            logging.info("Player Data Successfully Found!")
            for key, value in elements.items():
                if value is not None:
                    logging.info(f"    *    {key}: {value}")

        except Exception as e:
            logging.error(f"Error extracting player data: {e}")

    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")

    finally:
        if driver:
            driver.quit()  # driver.quit() is called only if driver was initialized

    # Filter elements to return only non-None and None elements separately
    non_none_elements = {key: value for key, value in elements.items() if value is not None}
    none_elements = {key: value for key, value in elements.items() if value is None}

    return kd, level, playtime, rank, ranked_kd

    # return non_none_elements, none_elements

# Example usage
# non_none_data, none_data = get_playerdata(api_url)
# logging.info(f"Non-None Elements: {non_none_data}")
# logging.info(f"None Elements: {none_data}")
