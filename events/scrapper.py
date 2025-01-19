import logging
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_playerdata(api_url):

    # Configure Firefox option for headless browsing (non-ui)
    options = Options()
    options.headless = True  # headless mode ON
    options.log.level = "trace"  
    options.set_preference("gfx.webrender.enabled", False)
    options.set_preference("layers.acceleration.disabled", True)

    driver = None  # Initialize driver outside the try block
    try:
        # Init the Firefox WebDriver using pointing to path for geckodriver
        service = Service('/home/DiscordPi/.wdm/drivers/geckodriver/linux64/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)

        # Navigate to the URL
        driver.get(api_url)

        # Wait for the page to load , incase of dynamic content
        driver.implicitly_wait(10)

        # Find the elements containing the player data
        try:
            logging.info(f"Looking For Player Data...")

            kd_element = driver.find_element(By.XPATH, "//span[contains(text(),'KD')]/following-sibling::span/span")
            level_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Level')]/span[@class='text-primary']")
            playtime_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Playtime')]/span[@class='text-primary']")
            rank_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-20') and contains(@class, 'text-secondary')]")
            ranked_kd_element = driver.find_element(By.XPATH, "//section[1]//div[3]//div[1]//div[2]//div[5]//span[2]/span")

            # Extract text from elements
            kd = kd_element.text if kd_element else None
            level = level_element.text if level_element else None
            playtime = playtime_element.text if playtime_element else None
            rank = rank_element.text if rank_element else None
            ranked_kd = ranked_kd_element.text if ranked_kd_element else None

            # Log the data or handle missing data
            if kd and level and playtime and rank and ranked_kd:
                logging.info("Player Data Successfully Found!")
                time.sleep(1)

                elements = {
                    'KD': kd,
                    'Level': level, 
                    'Playtime': playtime, 
                    'Rank': rank, 
                    'Ranked KD': ranked_kd
                }

                logging.info(f"Elements Found:")
                for key, value in elements.items():
                    if value is not None:
                        time.sleep(0.2)
                        logging.info(f"    *    {key}: {value}")

            else:
                logging.warning("Player data not found.")

        except Exception as e:
            logging.error(f"Error extracting player data: {e}")

    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
    finally:
        if driver:
            driver.quit()  # driver.quit() is called only if driver was initialized

    return kd, level, playtime, rank, ranked_kd
