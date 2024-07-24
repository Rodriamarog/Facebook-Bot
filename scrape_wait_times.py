import requests
from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def process_wait_times(wait_times, lanes):
    # Filter the list to keep only the entries we want
    filtered_times = [time for time in wait_times if time.startswith(('Vehicles:', 'Pedestrians:')) and not time.endswith(':')]
    
    result = [lanes[0]]
    for i, lane in enumerate(lanes[1:], 1):
        result.append(f"\n{lane}")
        if 2*i-2 < len(filtered_times):
            result.append(filtered_times[2*i-2])  # Vehicle time
        if 2*i-1 < len(filtered_times):
            result.append(filtered_times[2*i-1])  # Pedestrian time
    
    return result

def scrape_wait_times():
    url = "https://www.smartbordercoalition.com/border-wait-times"
    lanes_sy = ['SAN YSIDRO:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
    lanes_otay = ['OTAY:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        sy_wait_times = soup.select("div.ticker__item:nth-of-type(2) span")
        sy_wait_times = [clean_text(span.text) for span in sy_wait_times if clean_text(span.text)]
        
        otay_wait_times = soup.select("div.ticker__item:nth-of-type(3) span")
        otay_wait_times = [clean_text(span.text) for span in otay_wait_times if clean_text(span.text)]

        logger.info(f"Raw SY wait times: {sy_wait_times}")
        logger.info(f"Raw OTAY wait times: {otay_wait_times}")

        filtered_wait_times_sy = process_wait_times(sy_wait_times, lanes_sy)
        filtered_wait_times_otay = process_wait_times(otay_wait_times, lanes_otay)
        combined_wait_times = [filtered_wait_times_sy, filtered_wait_times_otay]
        
        logger.info("Data processed successfully")
        logger.info(f"Processed data: {combined_wait_times}")
        return combined_wait_times

    except Exception as e:
        logger.error(f'An error occurred: {e}', exc_info=True)
        return None

def get_wait_times():
    return scrape_wait_times()

if __name__ == "__main__":
    result = get_wait_times()
    print(result)