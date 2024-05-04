import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def process_wait_times(wait_times, lanes):
    count = 0
    filtered_wait_times = [lanes[0]]  # Starts with "SAN YSIDRO:" or "OTAY:"
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

def scrape_wait_times():
    chrome_bin = os.getenv("CHROME_BIN", "/opt/chromium")  # Adjusted for Lambda environment
    chromedriver_bin = os.getenv("CHROMEDRIVER_BIN", "/opt/chromedriver")  # Adjusted for Lambda environment

    options = Options()
    options.binary_location = chrome_bin
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    service = Service(executable_path=chromedriver_bin)
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("WebDriver initialized")

    lanes_sy = ['SAN YSIDRO:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
    lanes_otay = ['OTAY:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']

    try:
        driver.get("https://www.smartbordercoalition.com/border-wait-times")
        driver.implicitly_wait(10)
        logger.info("Page loaded successfully")

        sy_wait_times = driver.execute_script("""
            return Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(2) span")).map(span => span.innerText);
        """)
        otay_wait_times = driver.execute_script("""
            return Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(3) span")).map(span => span.innerText);
        """)

        filtered_wait_times_sy = process_wait_times(sy_wait_times, lanes_sy)
        filtered_wait_times_otay = process_wait_times(otay_wait_times, lanes_otay)

        combined_wait_times = [filtered_wait_times_sy, filtered_wait_times_otay]
        logger.info("Data processed successfully")
        return combined_wait_times

    except Exception as e:
        logger.error(f'An error occurred: {e}', exc_info=True)
        return None

    finally:
        driver.quit()
        logger.info("WebDriver session closed")

def lambda_handler(event, context):
    logger.info("Handler started")
    results = scrape_wait_times()
    logger.info("Handler completed")
    return {
        'statusCode': 200,
        'body': results
    }

if __name__ == "__main__":
    handler_result = lambda_handler(None, None)
    print(handler_result)
