# system
from selenium import webdriver
import time
import random
import sys
#
from f24_access_file import f24_read_write_file


class Flightradar24:

    #
    def __init__(self):
        # start read write file object
        self.file = f24_read_write_file()

    def time_sleep(self, second):
        """
            Random time stop

            :Args:
            - second(int): second.

               :Usage:
                   Flightradar24.time_sleep(second)
        """
        value = random.randint(int(second), int(second) * 2)
        time.sleep(value)

    def webdriver_chrome(self, url):
        """
        Use Chrome Browser.

        :Args:
         - url(String): URL.

        :Usage:
            Flightradar24.webdriver_chrome(
            url)

        :Returns:
            driver is Object.
            Object is web content
            The content of the webpage contains html, css, js
        """
        try:

            options = webdriver.ChromeOptions()

            options.add_argument('--headless')
            options.add_argument('disable-infobars')
            options.add_argument("--no-sandbox")
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url)

            return driver

        except:
            driver.quit()
            exit()

    def flight_record(self, flight_id, data_timestamp, data_flight):

        flight_url = 'https://api.flightradar24.com/common/v1/' \
                     'flight-playback.json?flightId=%s&timestamp=%s&token=' % (
                         data_flight, data_timestamp)

        driver = self.webdriver_chrome(flight_url)
        self.time_sleep(5)
        try:
            # data is Flight GPS record
            flight_data = driver.find_element_by_tag_name('pre').text
            flight_time = time.strftime("%Y-%m-%d", time.localtime(int(data_timestamp)))
            file_name = flight_time + "_" + flight_id + "_" + data_flight
            # Data write file
            self.file.write_json(file_name, flight_data)
        except:
            pass
        finally:
            driver.quit()

    def main(self, flight_id):
        """
        Search the flight path of the query flight
        :Args:
        - flight_id(String): Airplane flight.

        :Usage:
            Flightradar24.main(flight_id)

         Note: 'flight_id' CI501 is China Airlines flights from Taipei  (TPE) to Shanghai Pudong (PVG)
        """

        _url = "https://www.flightradar24.com/data/flights/%s" % flight_id

        driver = self.webdriver_chrome(_url)
        try:
            # search CSV_button css name
            CSV_button = driver.find_elements_by_css_selector(
                '.btn-sm.btn-white.btn-table-action.fs-10.csvButton.notranslate.downloadCsv')

            for i, t in enumerate(CSV_button):
                # Deduct the flight record on the day 扣除當天飛行中紀錄
                if t.get_attribute('data-flight') != "" and i != 0:
                    self.time_sleep(5)
                    # Check if this flight record is available for this machine
                    search_result = self.file.search_f24_file_id(t.get_attribute('data-flight'))
                    # -1 is no data
                    if search_result < 0:
                        # Record the flight time of the day
                        data_flight = t.get_attribute('data-flight')
                        data_timestamp = t.get_attribute('data-timestamp')
                        self.flight_record(flight_id, data_timestamp, data_flight)
            #
        except:
            pass
        finally:
            driver.quit()
            print("program_end")



if __name__ == "__main__":

    Flightradar24().main(sys.argv[1])
