from os.path import dirname, join
import os, sys
import json
import datetime, time

from datetime import datetime, timedelta


class F24AccessFile:
    __save_data_path = join(dirname(__file__), 'f24_data')

    # 航班紀錄寫入json
    def write_json(self, f24_timestamp, airline_name, airline_id, f24_flight_id, flight_data):

        new_director_path = self.get_f24_directory_path(f24_timestamp, airline_name)
        self.create_directory_path(new_director_path)
        file_path = join(new_director_path, self.get_f24_file_name(airline_id, f24_flight_id))

        try:
            data = json.loads(flight_data)
            # timestamp = data['result']['request']['timestamp']
            # airline_name_json = str(data['result']['response']['data']['flight']['airline']['name'])
            # airline_flight_id = \
            #     str(data['result']['response']['data']['flight']['identification']['number']['default']).upper()

            # print(airline_flight_id)
            # print(airline_name)
            # print(self.format_datetime(timestamp))

            if not 'errors' in data:
                with open(file_path, 'w') as the_file:
                    the_file.write(flight_data)
                print('-- ok --')
            else:
                os.remove(file_path)

        except Exception as e:
            print(e)
            # , airline_id, error_mess
            self.write_error_mess(f24_timestamp, airline_id, e)
            os.remove(file_path)
            pass

    def search_f24_file(self, f24_timestamp, airline_name, airline_id, f24_flight_id):
        search_file = join(self.get_f24_directory_path(f24_timestamp, airline_name),
                           self.get_f24_file_name(airline_id, f24_flight_id))

        if os.path.isfile(search_file):
            return True
        else:
            return False

    def create_directory_path(self, path):
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
                pass
                # exit()

    def format_datetime(self, timestamp):
        dt = datetime.strftime(datetime.fromtimestamp(int(timestamp)), '%Y_%m_%d')
        return dt

    def get_f24_directory_path(self, f24_timestamp, airline_name):
        path = join(self.__save_data_path, self.format_datetime(f24_timestamp), airline_name)
        return path

    def get_f24_file_name(self, airline_id, f24_flight_id):
        file_name = '%s_f24#%s.json' % (airline_id.upper(), f24_flight_id)
        return file_name

    def write_error_mess(self, f24_timestamp, airline_id, error_mess):

        new_director_path = self.create_directory(join(self.__save_data_path, 'error_mess'))

        file_name = \
            '%s_%s.txt' % (datetime.strftime(datetime.fromtimestamp(int(f24_timestamp)), '%Y_%m_%d'), airline_id)

        file_path = join(new_director_path, file_name)

        with open(file_path, 'w') as the_file:
            the_file.write(error_mess)


#
#
# # #
# # # #
# if __name__ == "__main__":
#
#     dict = {}
#
#
#     dict["A"]=''
#     dict["B"]=''
#
#     print(dict)
#
#     # a = list['CI201']
#
#
#     # a =list.index('CI202')
#
#     exit()
#     __save_data_path = join(dirname(__file__), 'f24_data', 'flight_info', 'CI')
#
#     f = F24AccessFile()
#     f.create_directory_path(__save_data_path)
#
#     path = join(__save_data_path, 'CI_flight_ID.json')
#
#     # def
#
#     if os.path.isfile(path):
#         with open(path, 'r') as the_file:
#             data = json.loads(the_file.read())
#     else:
#
#         with open(path, 'w') as file:
#             list = []
#             file.write(json.dumps(list))
#
#     print(type(data))
