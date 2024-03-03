from selenium import webdriver

def scrape_wait_times():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # Recommended for Docker environment
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--disable-gpu')  # GPU not used in headless mode
    options.add_argument('--window-size=1920,1080')  # Specify window size
    
    # Directly use ChromeDriver without webdriver_manager
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.smartbordercoalition.com/border-wait-times")
        driver.implicitly_wait(10)

        wait_times = driver.execute_script("""
            let times = [];
            let tickerItems = document.querySelectorAll("div.ticker__item:nth-of-type(2) span");
            tickerItems.forEach(function(item) {
                times.push(item.innerText);
            });
            return times;
        """)

        lanes = ['All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
        count = 0
        filtered_wait_times = ['Normal Lanes >>']

        for wait_time in wait_times:
            if wait_time[-1] == ":" or wait_time[0] == "N":
                continue
            else:
                if 'No Delay' in wait_time:
                    filtered_wait_times.append(wait_time)                 
                elif 'Status' in wait_time:
                    wait_time = 'Vehicles: 0.05'
                    filtered_wait_times.append(wait_time)                   
                    continue
                else:
                    filtered_wait_times.append(wait_time)                  
                if 'Pedestrians' in wait_time:
                    count += 1
                    filtered_wait_times.append("\n" + lanes[count])

        print(filtered_wait_times)
        return filtered_wait_times

    except Exception as e:
        print(f'An error occurred: {e}')
    
    finally:
        driver.quit()

if __name__ == '__main__':
    scrape_wait_times()
