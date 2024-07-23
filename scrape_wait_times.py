import requests
from bs4 import BeautifulSoup
import logging

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

def scrape_wait_times():
    url = "https://www.smartbordercoalition.com/border-wait-times"
    lanes_sy = ['SAN YSIDRO:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
    lanes_otay = ['OTAY:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>']

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        sy_wait_times = soup.select("div.ticker__item:nth-of-type(2) span")
        sy_wait_times = [span.text for span in sy_wait_times]
        
        otay_wait_times = soup.select("div.ticker__item:nth-of-type(3) span")
        otay_wait_times = [span.text for span in otay_wait_times]

        filtered_wait_times_sy = process_wait_times(sy_wait_times, lanes_sy)
        filtered_wait_times_otay = process_wait_times(otay_wait_times, lanes_otay)
        combined_wait_times = [filtered_wait_times_sy, filtered_wait_times_otay[:-2]]
        
        logger.info("Data processed successfully")
        return combined_wait_times

    except Exception as e:
        logger.error(f'An error occurred: {e}', exc_info=True)
        return None

def get_wait_times():
    return scrape_wait_times()

if __name__ == "__main__":
    result = get_wait_times()
    print(result)