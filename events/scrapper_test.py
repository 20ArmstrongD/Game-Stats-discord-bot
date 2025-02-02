import logging
import asyncio
from pyppeteer import launch

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_url = 'https://r6.tracker.network/r6siege/profile/ubi/BigMcD0n/overview'

async def get_playerdata(api_url):
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

        # Wait for the specific element to be present (with a different method for text matching)
        await page.waitForSelector("span", {'timeout': 60000})  # Wait for any span tag to be loaded

        # Use JavaScript evaluation to find the text content
        kd = await page.evaluate('''() => {
            const element = [...document.querySelectorAll("span")]
                .find(el => el.innerText.includes("KD"));
            return element ? element.innerText : null;
        }''')

        level = await page.evaluate('''() => {
            const element = [...document.querySelectorAll("span")]
                .find(el => el.innerText.includes("Level"));
            return element ? element.innerText : null;
        }''')

        playtime = await page.evaluate('''() => {
            const element = [...document.querySelectorAll("span")]
                .find(el => el.innerText.includes("Playtime"));
            return element ? element.innerText : null;
        }''')

        player_profile_img = await page.evaluate('''() => {
            const element = document.querySelector("img");
            return element ? element.src : null;
        }''')

        # Try to find ranked elements (if available)
        try:
            rank = await page.evaluate('''() => {
                const element = [...document.querySelectorAll("span")]
                    .find(el => el.innerText.includes("Rank"));
                return element ? element.innerText : null;
            }''')

            ranked_kd = await page.evaluate('''() => {
                const element = [...document.querySelectorAll("span")]
                    .find(el => el.innerText.includes("Ranked KD"));
                return element ? element.innerText : null;
            }''')

            ranked_img = await page.evaluate('''() => {
                const element = document.querySelector("img.ranked-img-class");
                return element ? element.src : null;
            }''')

            unknown_rank_elements= [rank, ranked_kd, ranked_img]
            
        except Exception as e:
            logging.warning("Ranked elements not found or not applicable.")
            for element in unknown_rank_elements:
                if element is None:
                    logging.info(f"{element} is not found")

        # Log the results
        elements = {
            'KD': kd,
            'Level': level,
            'Playtime': playtime,
            'Player Profile Pic': player_profile_img,
            'Rank': rank,
            'Ranked KD': ranked_kd,
            'Ranked Image': ranked_img,
        }

        logging.info("Player Data Successfully Found!")
        for key, value in elements.items():
            if value:
                logging.info(f"    *    {key}: {value}")

        # Close the browser
        await browser.close()

    except Exception as e:
        logging.error(f"Error in Pyppeteer: {e}")
    
    finally:
        # Ensure that the browser closes no matter what
        if browser:
            await browser.close()  # Close the browser session
            logging.info("Chromium browser process terminated.")
        
    return kd, level, rank, ranked_img, ranked_kd, player_profile_img

# # Run the async function
# asyncio.get_event_loop().run_until_complete(get_playerdata(api_url))
