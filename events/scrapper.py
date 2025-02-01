import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_playerdata(api_url):

    # Configure Firefox option for headless browsing (non-ui)
    options = Options()
    options.headless = True  
    options.log.level = "trace"
    options.set_preference("gfx.webrender.enabled", False)
    options.set_preference("layers.acceleration.disabled", True)

    # Initialize driver outside the try block
    driver = None  

    try:
        # Init the Firefox WebDriver using pointing to path for geckodriver
        service = Service('/home/DiscordPi/.wdm/drivers/geckodriver/linux64/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)

        # Navigate to the URL
        driver.get(api_url)

        # Wait for the page to load, in case of dynamic content
        driver.implicitly_wait(10)

        # Find the elements containing the player data (assuming everyplayer has these)
        try:
            logging.info(f"Looking For Player Data...")

            kd_element = driver.find_element(By.XPATH, "//span[contains(text(),'KD')]/following-sibling::span/span")
            level_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Level')]/span[@class='text-primary']")
            playtime_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Playtime')]/span[@class='text-primary']")
            player_profile_img_element = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div/main/div[3]/div[1]/div[2]/header/div[3]/div[1]/div[1]/div/img")

            kd = kd_element.text if kd_element else None
            level = level_element.text if level_element else None
            playtime = playtime_element.text if playtime_element else None
            player_profile_img = player_profile_img_element.get_attribute("src") if player_profile_img_element else None

            
            # try to find Ranked elements (not every player has these)
            try:
                rank_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-20') and contains(@class, 'text-secondary')]")
                ranked_kd_element = driver.find_element(By.XPATH, "//section[1]//div[3]//div[1]//div[2]//div[5]//span[2]/span")
                ranked_img_element = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div/main/div[3]/div[2]/div[2]/div[2]/section[2]/div[2]/div[1]/div[2]/div[1]/img")
                
                
                rank = rank_element.text if rank_element else None
                ranked_kd = ranked_kd_element.text if ranked_kd_element else None
                ranked_img = ranked_img_element.get_attribute("src") if ranked_img_element else None
                
                player_profile_img = player_profile_img_element.get_attribute("src") if player_profile_img_element else None
                
                unknown_elements = [rank, ranked_kd, ranked_img]
            except Exception as e:
                logging.warning("the following Ranked elements were not found.")
                for unknown_element in unknown_elements:
                    logging.warning("* ",unknown_element)

            elements = {
                'KD': kd,
                'Level': level,
                'Playtime': playtime,
                'Rank': rank,
                'Ranked KD': ranked_kd,
                'Ranked Image': ranked_img,
                'Player Profile Pic': player_profile_img}

            logging.info("Player Data Successfully Found!")
            for key, value in elements.items():
                if value is not None:
                    logging.info(f"    *    {key}: {value}")

        except Exception as e:
            logging.error(f"Error extracting player data: {e}")
            for key, value in elements.items():
                if value is None:
                    logging.info(f"    *    {key}: {value}")

    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")

    finally:
        if driver:
            driver.quit()  

    # elements to return only non-None and None elements separately (for testing function)
    # non_none_elements = {key: value for key, value in elements.items() if value is not None}
    # none_elements = {key: value for key, value in elements.items() if value is None}

    return kd, level, playtime, rank, ranked_kd, ranked_img, player_profile_img

    # return non_none_elements, none_elements

# For testing
# get_playerdata(api_url)
