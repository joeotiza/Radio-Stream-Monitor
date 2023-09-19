import pywhatkit
from datetime import datetime
import time
import requests

# Variables
phone_number = "+254711223344"
group_id = "Jp8a8ZH2D1AJHYEYTnkddM"
#Allow the program to call on WhatsApp web the first time it is run
first_time = True

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

streaming_site_url = 'https://stream-13.zeno.fm/ud2u96xst5quv'  # Replace with the streaming site URL

def check_site_status():
    try:
        okay = True
        
        stations = "The following streams are not working:\n"
        
        radios = {
            "radio_taifa" :     "https://stream-13.zeno.fm/ud2u96xst5quv",
            "english_service" : "https://stream-48.zeno.fm/mhmwnyyst5quv",
            "pwani_fm" :        "https://stream-22.zeno.fm/smhmfr1a94zuv",
            "coro_fm " :        "https://stream-38.zeno.fm/65sw1gyst5quv",
            "iftin   " :        "https://stream-10.zeno.fm/1v7yr8499yzuv",
            "mayienga" :        "https://stream-69.zeno.fm/ayw9hk0st5quv",
            "minto   " :        "https://stream-61.zeno.fm/u3dw22zst5quv",
            "kitwek_fm" :       "https://stream-23.zeno.fm/gh67mvp8f2zuv",
            "mwatu_fm" :        "https://stream-26.zeno.fm/kawduafexa0uv",
            "ingo_fm " :        "https://stream-37.zeno.fm/sxr6fxkgymzuv",
            "mwago_fm" :        "https://stream.zeno.fm/3bp7c3sfx98uv",
            "nosim_fm" :        "https://stream-23.zeno.fm/nw5wm356998uv",
            "ngemi_fm" :        "https://stream-160.zeno.fm/bq8gnvsso0xuv?zs"
        }
        print("\nKBC RADIOS STREAMING STATUS\n")
        print("Station Name\tStatus Code\tStream Link")
        print("----------------------------------------------")
        for r in radios:
            with requests.get(radios[r], stream = True) as l:
                print(r +"\t"+ str(l.status_code) +"\t\t"+ l.url)
                if (l.status_code != 200):
                    okay = False
                    stations += r + "\n"
        
        print("\nOperation Complete!\n\n")
        
        if (okay):
            message = "All streams are working well."
        else:
            message = stations
        
        #message = 'Write the message here'
        time_hour = datetime.now().hour
        time_minute = datetime.now().minute + 2
        
        #handling spillover time values
        if time_minute >= 60:
            time_hour += 1
            time_minute %= 60
        if time_hour >= 24:
            time_hour = 0

        morning = time_hour == 8 and time_minute >= 0 and time_minute <= 4
        noon = time_hour == 12 and time_minute >= 0 and time_minute <= 4
        evening = time_hour == 16 and time_minute >= 0 and time_minute <= 4

        #send a message at 8AM, noon, and 4PM regardless to ensure system is still online
        global first_time
        alert_time = morning or noon or evening or first_time
        
        waiting_time_to_send = 20
        close_tab = True
        waiting_time_to_close = 5
        
        mode = "group"
        
        #only send a message if one or more stations are down
        if not okay or alert_time:
            first_time = False

            if mode == "contact":
                # Send a WhastApp message to an specific contact
                pywhatkit.sendwhatmsg(phone_number, message, time_hour, time_minute, waiting_time_to_send, close_tab, waiting_time_to_close)
            elif mode == "group":
                # Send a WhastApp message to an specific group
                pywhatkit.sendwhatmsg_to_group(group_id, message, time_hour, time_minute, waiting_time_to_send, close_tab, waiting_time_to_close)
            else:
                print("Error code: 97654")
                print("Error Message: Please select a mode to send your message.")

            #if a station is down, send alerts in 10 minute intervals
            if not okay:
                time.sleep(10*60)
    except requests.exceptions.RequestException as e:
        print(f'Error: Unable to access the streaming site.\n{str(e)}')

def monitor_site():
    while True:
        try:
            # Set up the headless Chrome browser
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(streaming_site_url)

            # Check if the streaming site is accessible
            if 'error-page' in driver.page_source:
                print('The streaming site is down!')

            # Close the browser
            driver.quit()
        except Exception as e:
            print(f'Error: {str(e)}')

        # Check the site status using requests (without browser automation)
        check_site_status()

        # Wait for a specific interval before checking again (e.g., 5 seconds)
        time.sleep(5)

if __name__ == '__main__':
    try:
        monitor_site()
    except KeyboardInterrupt:
        print('Monitoring stopped by user.')
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
