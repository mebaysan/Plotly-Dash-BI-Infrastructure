from flaskapp.dashboard.apps.developer.data import get_data
from flaskapp.dashboard.apps.developer.screens.basic_components.get_callbacks import get_callbacks as basic_components_callbacks
from flaskapp.dashboard.apps.developer.screens.basic_components.get_screen import get_screen as basic_components_screen
from flaskapp.dashboard.apps.developer.screens.bizim.get_callbacks import get_callbacks as bizim_callbacks
from flaskapp.dashboard.apps.developer.screens.bizim.get_screen import get_screen as bizim_screen
from flaskapp.dashboard.utilities.components.builder import ComponentBuilder

CONFIG = {
    'BASE_URL': '/h123rP239dsaXZXCZXaCMNBYklhsd123451MacLhxcbhkS/developer/',
    'APP_URL': 'developer',
    'APP_NAME': 'Developer',
}


def add_dash(server):
    component_builder = ComponentBuilder()
    DF = get_data()

    TABS = component_builder.get_tabs(
        tab_items={
            'Temel Bileşenler': 'basic-components',
            'Component Builder': 'bizim'
        }
    )
    app = component_builder.get_dash_app(server, CONFIG, TABS,
                                         callbacks=[
                                             {'function': basic_components_callbacks, 'data': [
                                                 DF,component_builder]},
                                             {'function': bizim_callbacks,
                                                 'data': [DF,component_builder]}
                                         ],
                                         screens=[
                                             {'screen': 'basic-components', 'function': basic_components_screen, 'data': [
                                                 DF, component_builder]},
                                             {'screen': 'bizim', 'function': bizim_screen, 'data': [
                                                 DF, component_builder]}
                                         ])
    return app.server
