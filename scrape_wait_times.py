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

        sy_wait_times = driver.execute_script("""
            let times = [];
            let tickerItems = document.querySelectorAll("div.ticker__item:nth-of-type(2) span");
            tickerItems.forEach(function(item) {
                times.push(item.innerText);
            });
            return times;
        """)

        otay_wait_times = driver.execute_script("""
            let times = [];
            let tickerItems = document.querySelectorAll("div.ticker__item:nth-of-type(3) span");
            tickerItems.forEach(function(item) {
                times.push(item.innerText);
            });
            return times;
        """)

        lanes = ['All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
        count = 0
        filtered_wait_times = ['SAN YSIDRO:','All Traffic >>']

        for wait_time in sy_wait_times:
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

        lanes_otay = ['All Traffic >>', 'Ready Lanes >>', 'Sentri >>']
        count_otay = 0
        filtered_wait_times_otay = ['\n-\n-\nOTAY:','All Traffic >>']

        for wait_time in otay_wait_times:
            if wait_time[-1] == ":" or wait_time[0] == "N":
                continue
            else:
                if 'No Delay' in wait_time:
                    filtered_wait_times_otay.append(wait_time)                 
                elif 'Status' in wait_time:
                    wait_time = 'Vehicles: 0.05'
                    filtered_wait_times_otay.append(wait_time)                   
                    continue
                else:
                    filtered_wait_times_otay.append(wait_time)                  
                if 'Pedestrians' in wait_time:
                    count_otay += 1
                    filtered_wait_times_otay.append("\n" + lanes_otay[count_otay])

        filtered_wait_times_otay = filtered_wait_times_otay[:-2]


        wait_times_combined = filtered_wait_times + filtered_wait_times_otay

        for i in wait_times_combined:
            print(i)

        return wait_times_combined
    
    except Exception as e:
        print(f'An error occurred: {e}')
    
    finally:
        driver.quit()

if __name__ == '__main__':
    scrape_wait_times()