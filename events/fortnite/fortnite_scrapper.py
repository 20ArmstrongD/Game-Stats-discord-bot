import logging
import asyncio
from pyppeteer import launch

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%I:%M:%S %p'  # 12-hour clock with AM/PM
)


url = 'https://fortnitetracker.com/profile/all/Budg3taryChunk5'
async def get_fortnite_player_data(url):
    try:
        # Launch a headless browser
        browser = await launch(
            headless=True,
            executablePath='/usr/bin/chromium-browser',  # Path to the Chromium browser installed on your system
            args=['--no-sandbox']
        )
        page = await browser.newPage()

        # Set a longer timeout if needed
        await page.goto(url, {'timeout': 60000})  # Wait for the page to load for 60 seconds

        await page.waitForSelector("span", {'timeout': 60000})  # Wait for any span tag to be loaded

        # Use JavaScript evaluation to find the text content
        # Use CSS selector or XPATH to find values 
        try:
            kd = await page.evaluate('''() => {
                const xpath = "//*[@id="overview"]/div[2]/div/div[1]/div/div[1]/div[3]/div[2]/div[2]/div";
                const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                const element = result.singleNodeValue;
                return element ? element.innerText : null;
            }''')
            # logging.info(f"KD found")
            
            level = await page.evaluate('''() => {
                const xpath = "//*[@id="overview"]/div[2]/div/div[1]/header/div/div[2]/text()";
                const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                const element = result.singleNodeValue;
                return element ? element.innerText : null;
            }''')
            # logging.info(f"Level found")

            playtime = await page.evaluate('''() => {
            const xpath = "//*[@id='overview']/div[2]/div/div[1]/header/div/div[1]/text()";
            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            const element = result.singleNodeValue;
            return element ? element.textContent.trim() : null;
            }''')
            # logging.info(f"Playtime found")
            
            elements = {
                    'playtime': playtime,
                    'kd': kd,
                    'level': level
                    }
                 
        except Exception as e:
            logging.warning(f'These unable to be pulled')
            for key, value in elements.items():
                if value is None:
                    logging.warning(f"{key}: {value}")
        
        try:
            user_profile_img = await page.evaluate('''() => {
                const element = document.querySelector(".profile-header-avatar");
                return element ? element.src : null;
            }''')
            # logging.info(f"Player Profile Pic found")
            
            img_elements = {
                'user_profile_img':user_profile_img
                }
        except Exception as e:
            logging.warning(f" Image element(s) not found")
            for key,value in img_elements.items():
                logging.warning(f"{key}: {value}")
                
                
        logging.info(f"Player Data Sucessfully found!")
        for key, value in elements.items():
            if value:
                logging.info(f"    *    {key}: {value}")
        for key, value in img_elements.items():
            if value and len(value) > 10:
                logging.info(f"    *    {key}: url has been grabbed")      

        
    except Exception as e:
        logging.error(f"Error in Pyppeteer: {e}")
        
    finally:
            # Ensure that the browser closes
            if browser:
                await browser.close()  # Close the browser session


        
    return kd, level, playtime, user_profile_img


# scrapper.py script testing

asyncio.run(get_fortnite_player_data(url))
