# system
from selenium import webdriver
import time
import random
import sys
#
from f24_access_file import f24_read_write_file


class Flightradar24:
    __url = "https://www.flightradar24.com/data/flights/%s"
    # check button get parameter
    __playButton_className = '.btn.btn-sm.btn-playback.btn-table-action.text-white.bkg-blue.fs-10'
    # This is the attributes value of flightradar24 flight id
    __flightRadar24_flightId_attributes_name = 'data-flight-hex'
    # This is the attributes value of flightradar24 timestamp
    __flightRadar24_timestamp_attributes_name = 'data-timestamp'
    # get json
    __flight_json_url = 'https://api.flightradar24.com/common/v1/flight-playback.json?flightId=%s&timestamp=%s&token='

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

            # options.add_argument('--headless')
            options.add_argument('disable-infobars')
            options.add_argument("--no-sandbox")
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(options=options)
            driver.get(url)

            return driver

        except:
            print('webchrome end')
            # driver.quit()
            # exit()

    def flight_record(self, flight_id, data_timestamp, data_flight):

        flight_url = self.__flight_json_url % (data_flight, data_timestamp)

        driver = self.webdriver_chrome(flight_url)

        self.time_sleep(2)

        try:
            # data is Flight GPS record
            flight_data = driver.find_element_by_tag_name('pre').text

            flight_time = time.strftime("%Y-%m-%d", time.localtime(int(data_timestamp)))
            file_name = flight_time + "_" + flight_id
            # Data write file
            self.file.write_json(file_name, flight_data)
        except:
            pass
        finally:
            driver.quit()

    def main(self, airline_id):
        """
        Search the flight path of the query flight
        :Args:
        - airline_flight_id (String): Airplane flight.

        :Usage:
            Flightradar24.main(airline_flight_id)

         Note:
             'airline_flight_id' CI501 is China Airlines flights from China Taipei  (TPE) to China Shanghai Pudong (PVG)
             'airline_flight_id' BR771 is EVA Airlines flights from China Shanghai Hongqiao (PVG) to China Taipei  (TPE)

        """

        url = self.__url % (airline_id)
        driver = self.webdriver_chrome(url)

        try:
            # search CSV_button css name
            play_button = driver.find_elements_by_css_selector(self.__playButton_className)

            self.time_sleep(2)

            for i, t in enumerate(play_button):
                # Deduct the flight record on the day 扣除當天飛行中紀錄
                if t.get_attribute(self.__flightRadar24_flightId_attributes_name) != "" and i != 0:
                    flightRadar24_flightId = t.get_attribute(self.__flightRadar24_flightId_attributes_name)
                    flightRadar24_timestamp = t.get_attribute(self.__flightRadar24_timestamp_attributes_name)
                    t.click()
                    flight_json_url = self.__flight_json_url % (flightRadar24_flightId, flightRadar24_timestamp)
                    print(flight_json_url)

                    self.time_sleep(2)
                    # Check if this flight record is available for this machine

                    # # change use json save
                    # search_result = self.file.search_f24_file_id(
                    #     t.get_attribute(self.__flightRadar24_flightId_attributes_name))

                    # print(i)
                    # print(t.get_attribute(self.__flightRadar24_flightId_attributes_name))
                    # print(search_result)
                    # print('---')
                    # # -1 is no data
                    # if search_result < 0:
                        # Record the flight time of the day
                    self.flight_record(airline_id, flightRadar24_timestamp, flightRadar24_flightId)
                # if i == 9:
                #     break



        except:
            pass
        finally:
            driver.quit()
            print("program_end")


if __name__ == "__main__":
    # Flightradar24().main(sys.argv[1])
    Flightradar24().main('ci502')
