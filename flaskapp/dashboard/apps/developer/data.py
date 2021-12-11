import pandas as pd
import os
from config import Config


def get_data():
    df = pd.read_pickle(os.path.join(
        Config.DATASET_CONTAINER, 'developer', 'tips.pickle'))
    return df
