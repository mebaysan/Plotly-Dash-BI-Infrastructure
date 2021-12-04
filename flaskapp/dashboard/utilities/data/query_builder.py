from config import Config
import pymssql


class QueryBuilder:
    MIN_YEAR = 2019
    MAX_YEAR = 2021

    def __init__(self, wh_type='MsSQL'):
        self.MIN_DATE = '20190101'
        self.MAX_DATE = '20211231'

        if wh_type == 'MsSQL':
            self.DB_CONN = pymssql.connect(
                server=Config.WH_CONFIG['SERVER'], user=Config.WH_CONFIG['USER'],
                password=Config.WH_CONFIG['PASSWORD'], database=Config.WH_CONFIG['DATABASE']
            )
        else:
            # ToDo: Add other databases' connections
            pass

    @classmethod
    def get_min_max(cls):
        return (cls.MIN_YEAR, cls.MAX_YEAR)
