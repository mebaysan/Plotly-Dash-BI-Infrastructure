"""
Dash uygulamalarımıza ait CONFIG sabitlerini bu dosyada URL_PATHS'e ekleyeceğiz
"""
from flaskapp.dashboard.apps.developer import app as developer

URL_PATHS = [
    developer.CONFIG,
]
