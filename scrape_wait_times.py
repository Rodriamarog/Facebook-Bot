import asyncio
import logging
from pyppeteer import launch

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_wait_times(wait_times, lanes):
    count = 1
    filtered_wait_times = [lanes[0], lanes[1]]  # Starts with "SAN YSIDRO:" or "OTAY:"
    for wait_time in wait_times:
        if wait_time[-1] == ":" or wait_time[0] == "N":
            continue
        else:
            if 'No Delay' in wait_time:
                filtered_wait_times.append(wait_time)
            elif 'Status' in wait_time:
                wait_time = 'Vehicles: 0.05'
                filtered_wait_times.append(wait_time)
            else:
                filtered_wait_times.append(wait_time)
            if 'Pedestrians' in wait_time and count < len(lanes) - 1:
                count += 1
                filtered_wait_times.append("\n" + lanes[count])
    return filtered_wait_times

async def scrape_wait_times():
    browser = await launch(
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--single-process',
        ]
    )
    page = await browser.newPage()
    logger.info("Browser initialized")

    lanes_sy = ['SAN YSIDRO:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
    lanes_otay = ['OTAY:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']

    try:
        await page.goto("https://www.smartbordercoalition.com/border-wait-times")
        await page.waitForSelector("div.ticker__item")
        logger.info("Page loaded successfully")

        sy_wait_times = await page.evaluate("""
        () => Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(2) span")).map(span => span.innerText)
        """)
        
        otay_wait_times = await page.evaluate("""
        () => Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(3) span")).map(span => span.innerText)
        """)

        filtered_wait_times_sy = process_wait_times(sy_wait_times, lanes_sy)
        filtered_wait_times_otay = process_wait_times(otay_wait_times, lanes_otay)
        combined_wait_times = [filtered_wait_times_sy, filtered_wait_times_otay[:-2]]
        logger.info("Data processed successfully")

        return combined_wait_times
    except Exception as e:
        logger.error(f'An error occurred: {e}', exc_info=True)
        return None
    finally:
        await browser.close()
        logger.info("Browser session closed")

def get_wait_times():
    return asyncio.get_event_loop().run_until_complete(scrape_wait_times())

if __name__ == "__main__":
    result = get_wait_times()
    print(result)