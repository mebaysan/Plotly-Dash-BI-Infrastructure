import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def get_screen(DF, component_builder):
    layout = html.Div(children=[
        html.Div(className='box', children=[
            html.Div(className='columns', children=[

                component_builder.get_basic_table(['Özet', ''], {
                    'Kendi': 'Yaptığımız',
                    'Component': 'Builder',
                    'İle': 'Yapılan',
                    'Dummy': 'Deneme'})

            ]),
            html.Div(className='columns', children=[
                html.Div(className='column', children=[
                    component_builder.get_tabs(
                        tab_items={
                            'Tab Item 1': 'tab-item-1',
                            'Tab Item 2': 'tab-item-2',
                            'Tab Item 3': 'tab-item-3',
                            'Tab Item 4': 'tab-item-4',
                            'Tab Item 5': 'tab-item-5'
                        })
                ])
            ]),
            html.Div(className='columns', children=[
                component_builder.get_dropdown_input(
                    data_frame=DF, label='Column İçinde Classsız', filter_column='day', input_id='custom-dd1', default_value='first'),
                component_builder.get_dropdown_input(data_frame=DF, label='Column İçinde Classlı', filter_column='day',
                                                     input_id='custom-dd2', default_value='first', column_class='is-one-quarter'),
                component_builder.get_button(
                    label='Columnlu', button_id='custom-btn1', column_class='is-one-quarter mt-5', is_in_column=True),
            ]),
            component_builder.get_dropdown_input(
                data_frame=DF, label='Column İçinde Değil', filter_column='day', input_id='custom-dd3', default_value='self', is_in_column=False),
            component_builder.get_button(
                label='Columnsuz', button_id='custom-btn2'),
            html.Div(className='columns', children=[
                component_builder.get_graph_column(
                    label='Cinsiyetlere Göre', label_id='cinsiyet-label', figure=px.pie(data_frame=DF, values='tip', names='sex'), figure_id='cinsiyet-figure', label_class='has-text-centered has-text-primary'),
                component_builder.get_graph_column(
                    label='Günlere Göre', label_id='gun-label', figure=px.pie(data_frame=DF, values='tip', names='day'), figure_id='gun-figure', label_class='has-text-centered has-text-warning'),
                component_builder.get_graph_column(label='Sigara Durumuna Göre', label_id='smoker-label', figure=px.pie(
                    data_frame=DF, values='tip', names='smoker'), figure_id='smoker-figure', label_class='has-text-centered'),
                component_builder.get_graph_column(label='Öğünlere Göre', label_id='ogun-label', figure=px.pie(
                    data_frame=DF, values='tip', names='time'), figure_id='ogun-figure', label_class='has-text-centered'),
            ]),
            html.Div(className='columns', children=[
                component_builder.get_input_text('Input Box', 'cst-inpt-1', 'text', column_class='is-one-third',
                                                 help_text='Help text', help_text_class='is-link', default_value='Default', label_class='has-text-link', input_class='is-link'),
                component_builder.get_input_text('Input Box2', 'cst-inpt-2', 'number', column_class='is-one-third',
                                                 help_text='Sadece Sayı', help_text_class='is-warning', default_value=3, label_class='has-text-warning', input_class='is-warning'),
                component_builder.get_dropdown_input([{'label': 'İlk item', 'value': 'İlk İtem'}, {'label': 'İkinci item', 'value': 'İkinci İtem'}], filter_column='-',
                                                     label='Dropdown', input_id='cst-dd', default_value='first', column_class='is-one-third', help_text='Alt metin', help_text_class='is-danger', label_class='has-text-danger')
            ]),
            html.Div(className='columns', children=[
                html.Div(className='column', children=[
                    dcc.Graph(id='d-tablo')
                ])
            ])
        ])
    ])

    return layout
