import logging
import asyncio
from pyppeteer import launch

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%I:%M:%S %p'  # 12-hour clock with AM/PM
)

# api_url = 'https://r6.tracker.network/r6siege/profile/ubi/BigMcD0n/overview'

async def get_r6siege_player_data(api_url):
    try:
        # Launch a headless browser
        browser = await launch(
            headless=True,
            executablePath='/usr/bin/chromium-browser',  # Path to the Chromium browser installed on your system
            args=['--no-sandbox']
        )
        page = await browser.newPage()

        # Set a longer timeout if needed
        await page.goto(api_url, {'timeout': 60000})  # Wait for the page to load for 60 seconds

        await page.waitForSelector("span", {'timeout': 60000})  # Wait for any span tag to be loaded

        # Use JavaScript evaluation to find the text content
        # Use CSS selector or XPATH to find values 
        kd = await page.evaluate('''() => {
            const xpath = "//span[contains(text(), 'KD')]/following-sibling::span/span";
            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            const element = result.singleNodeValue;
            return element ? element.innerText : null;
        }''')
        # logging.info(f"KD found")
        
        level = await page.evaluate('''() => {
            const xpath = "/html/body/div[1]/div/div[2]/div[3]/div/main/div[3]/div[2]/div[2]/div[2]/section[1]/div/div[1]/span[1]/span";
            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            const element = result.singleNodeValue;
            return element ? element.innerText : null;
        }''')
        # logging.info(f"Level found")

        playtime = await page.evaluate('''() => {
            const element = document.querySelector("span.text-secondary:nth-child(3) > span:nth-child(1)");
            return element ? element.innerText : null;
        }''')
        # logging.info(f"Playtime found")

        user_profile_img = await page.evaluate('''() => {
            const element = document.querySelector(".user-avatar__image");
            return element ? element.src : null;
        }''')
        # logging.info(f"Player Profile Pic found")

        # Try to find ranked elements (if available)
        try:
            
            rank = await page.evaluate('''() => {
                const element = document.querySelector(".flex-1 > div:nth-child(1) > span:nth-child(1)");
                return element ? element.innerText : null;
            }''')
            # logging.info(f"Rank found")
            
            ranked_kd = await page.evaluate('''() => {
                const element = document.querySelector("div.playlist:nth-child(1) > div:nth-child(2) > div:nth-child(5) > span:nth-child(2) > span:nth-child(1)");
                return element ? element.innerText : null;
            }''')
            # logging.info(f"Ranked_KD found")
            
            rank_img = await page.evaluate('''() => {
                const element = document.querySelector("header.rounded-t-4 > div:nth-child(1) > img:nth-child(1)");
                return element ? element.src : null;
            }''')

            # # Log the Ranked Image
            # logging.info(f"Ranked Image found")

        except Exception as e:
            ranked_elements = {"Rank": rank,
                               "Ranked_KD": ranked_kd,
                               "Ranked_img": rank_img}
            logging.warning(f'These unable to be pulled')
            for key, value in ranked_elements.items():
                if value is None:
                    print(f"{key}: {value}")

        # Log the results
        elements = {
            'KD': kd,
            'Level': level,
            'Playtime': playtime,
            'Rank': rank,
            'Ranked KD': ranked_kd
        }
        img_elements = {
            'Player Profile Pic': user_profile_img,
            'Ranked Image': rank_img}

        logging.info("Player Data Successfully Found!")
        for key, value in elements.items():
            if value:
                logging.info(f"    *    {key}: {value}")
        for key, value in img_elements.items():
            if value is not None and len(value) > 10:
                logging.info(f"    *    {key}: url has been grabbed")

    except Exception as e:
        logging.error(f"Error in Pyppeteer: {e}")
        
    finally:
            # Ensure that the browser closes
            if browser:
                await browser.close()  # Close the browser session


        
    return kd, level, playtime, rank, ranked_kd, user_profile_img, rank_img


# scrapper.py script testing
# get_playerdata(api_url)
