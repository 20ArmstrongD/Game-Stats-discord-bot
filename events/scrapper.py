import discord
from discord import app_commands
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging

# api_url = f'https://r6.tracker.network/r6siege/profile/xbl/SeamedRhombus62/overview'

def get_playerdata(api_url):
    # Setup Chrome options for headless browsing
    options = Options()
    options.headless = True  # Don't open a window, just fetch the page

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to the URL
        driver.get(api_url)

        # Wait for the page to load (in case of dynamic content)
        driver.implicitly_wait(10)

        # Find the element containing the "KD" label and the next sibling span
        kd_element = driver.find_element(By.XPATH, "//span[contains(text(),'KD')]/following-sibling::span/span")
        level_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Level')]/span[@class='text-primary']")
        playtime_element = driver.find_element(By.XPATH, "//span[@class='text-14 text-secondary font-sans font-medium leading-3/4' and contains(., 'Playtime')]/span[@class='text-primary']")
        rank_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-20') and contains(@class, 'text-secondary')]")
        ranked_kd_element = driver.find_element(By.XPATH,"//section[1]//div[3]//div[1]//div[2]//div[5]//span[2]/span")

        # Extract text from elements
        kd = kd_element.text if kd_element else None
        level = level_element.text if level_element else None
        playtime = playtime_element.text if playtime_element else None
        rank = rank_element.text if rank_element else None
        ranked_kd = ranked_kd_element.text if ranked_kd_element else None

        if kd and level and playtime and rank and ranked_kd:
                logging.info("found all elements")
                # print(f"Playtime: {playtime} hrs")
                # print(f"K/D Ratio: {kd}")
                # print(f"Level: {level}")
                # print(f"Rank: {rank}")
                # print(f"Ranked KD: {ranked_kd}")
        else:
            print("Some elements were not found.")        
        # if kd_element and level_element and playtime_element and rank_element and ranked_kd_element:
        #     print(f"Playtime: {playtime_element.text}rs")
        #     print(f"K/D Ratio: {kd_element.text}")
        #     print(f"level: {level_element.text}")
        #     print(f"rank: {rank_element.text}")
        #     print(f"ranked KD: {ranked_kd_element.text}")
        # else:
        #     print("elements.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return kd, level, playtime, rank, ranked_kd

# Replace with the URL you want to pull data from



