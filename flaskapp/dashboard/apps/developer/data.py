import pandas as pd
import os


def get_data():
    df = pd.read_pickle(os.path.join(
        os.getenv('DATASET_CONTAINER'), 'developer', 'tips.pickle'))
    return df
