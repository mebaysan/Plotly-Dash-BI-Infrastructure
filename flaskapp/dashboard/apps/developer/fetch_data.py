import seaborn as sns
from flaskapp.dashboard.utilities.data.fetcher import Fetcher

fetcher = Fetcher('developer')


def fetch_data(queryBuilder):
    df = sns.load_dataset('tips')
    fetcher.write_data_as_pickle(df, 'tips.pickle')
