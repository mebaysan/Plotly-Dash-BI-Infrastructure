from config import Config
import os


class Fetcher:
    def __init__(self, app_name):
        self.app_name = app_name
        self.data_folder = os.path.join(
            Config.DATASET_CONTAINER, self.app_name)
        self.create_folder_if_is_not_exists()

    def create_folder_if_is_not_exists(self):
        if not os.path.isdir(self.data_folder):
            os.makedirs(self.data_folder)

    def write_data_as_pickle(self, dataframe, file_name):
        dataframe.to_pickle(os.path.join(self.data_folder, file_name))
