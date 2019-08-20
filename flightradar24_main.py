# system
from selenium import webdriver
from os.path import dirname, join
import time
import random
from datetime import datetime, timedelta
import sys
#
from f24_access_file import F24AccessFile


class Flightradar24:
    # save data directory
    #
    __url = "https://www.flightradar24.com/data/flights/%s"
    # airline_name html tag id
    __airline_name_id = 'cnt-playback'
    # airline_name_attributes
    __airline_name_attributes_name = 'data-airline-name'
    # check button get parameter
    __playButton_className = '.btn.btn-sm.btn-playback.btn-table-action.text-white.bkg-blue.fs-10'
    # This is the attributes value of flightradar24 flight id
    __flightRadar24_flightId_attributes_name = 'data-flight-hex'
    # This is the attributes value of flightradar24 timestamp
    __flightRadar24_timestamp_attributes_name = 'data-timestamp'
    # get json file
    __flight_json_url = 'https://api.flightradar24.com/common/v1/flight-playback.json?flightId=%s&timestamp=%s&token='

    # airline_id

    #

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

    def flight_record(self, f24_timestamp, f24_flight_id, airline_name, airline_id):

        f24AccessFile = F24AccessFile()

        print('%s => %s _ %s  ' % (f24AccessFile.format_datetime(f24_timestamp), airline_name, airline_id,))

        status = f24AccessFile.search_f24_file(f24_timestamp, airline_name, airline_id, f24_flight_id)

        if not status:
            try:
                flight_url = self.__flight_json_url % (f24_flight_id, f24_timestamp)
                driver = self.webdriver_chrome(flight_url)
                #
                time.sleep(5)

                # data is Flight GPS record
                flight_data = driver.find_element_by_tag_name('pre').text
                # write file
                f24AccessFile.write_json(f24_timestamp, airline_name, airline_id, f24_flight_id, flight_data)

            except Exception as e:
                print('-- record errer --')
                print(e)
                print('-- record errer --')
                pass
            finally:
                driver.quit()

    #

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
        # start chrome
        driver = self.webdriver_chrome(url)

        try:
            # search CSV_button css name
            airline_name = \
                driver.find_element_by_id(self.__airline_name_id).get_attribute(self.__airline_name_attributes_name)
            play_button = driver.find_elements_by_css_selector(self.__playButton_className)

            # 判斷航班是否有飛行紀錄

            if len(play_button) != 0:

                # self.time_sleep(5)
                before_yesterday = int(datetime.timestamp(datetime.now() - timedelta(days=2)))

                for i, t in enumerate(play_button):
                    # Deduct the flight record on the day 扣除當天飛行中紀錄
                    if t.get_attribute(self.__flightRadar24_flightId_attributes_name) != "":
                        f24_flightId = t.get_attribute(self.__flightRadar24_flightId_attributes_name)
                        f24_timestamp = t.get_attribute(self.__flightRadar24_timestamp_attributes_name)

                        if int(f24_timestamp) < before_yesterday:
                            self.time_sleep(10)
                            t.click()
                            print('-- run --[ %s ] -> %s ' %
                                  (datetime.strftime(datetime.fromtimestamp(int(f24_timestamp)), '%Y_%m_%d'),
                                   airline_id))
                        self.flight_record(f24_timestamp, f24_flightId, airline_name, airline_id)
            else:
                print(airline_id + ' no data')
                print(' -- --- --- ---')

                self.time_sleep(1)
        except Exception as e:
            print('-- main errer --')
            print(e)

            f = F24AccessFile()
            f.write_error_mess(f24_timestamp, airline_id, str(e))
            print('-- main errer --')
            pass
        finally:
            driver.quit()

#
# if __name__ == "__main__":
#     for i in range(1000, 10000):
#         print(i)
#         f = Flightradar24()
#         f.main('ci%d' % i)
