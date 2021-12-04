from flaskapp.dashboard.utilities.data.query_builder import QueryBuilder
from flaskapp.dashboard.apps.developer.fetch_data import fetch_data as fetch_developer


queryBuilder = QueryBuilder()

fetch_developer(queryBuilder)
