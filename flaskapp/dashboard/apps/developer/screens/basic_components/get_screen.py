import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def get_screen(DF, component_builder):
    layout = html.Div(children=[
        html.Div(className=component_builder.DASH_LAYOUT_CLASS, children=[
            html.Section(className='hero is-primary mb-3', children=[
                html.Div(className='hero-body', children=[
                    html.P('Otomatik Resize Olan Kolonlar', className='title')
                ])
            ]),
            html.Div(className='columns', children=[
                html.Div(className='column', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Cinsiyet'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-11',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['sex'].unique()],
                                value=DF['sex'].unique()[0]
                            ),
                        ])
                    ])
                ]),
                html.Div(className='column', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Sigara'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-12',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['smoker'].unique()],
                                value=DF['smoker'].unique()[0]
                            ),
                        ])
                    ])
                ]),
                html.Div(className='column', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Gün'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-13',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['day'].unique()],
                                value=DF['day'].unique()[0]
                            ),
                        ])
                    ])
                ]),
                html.Div(className='column', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Öğün'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-14',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['time'].unique()],
                                value=DF['time'].unique()[0]
                            ),
                        ])
                    ])
                ]),
            ]),
            html.Section(className='hero is-link mb-3', children=[
                html.Div(className='hero-body', children=[
                    html.P('En Küçük Boyuttaki Kolonlar',
                           className='title')
                ])
            ]),
            html.Div(className='columns', children=[
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Cinsiyet'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-21',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['sex'].unique()],
                                value=DF['sex'].unique()[0]
                            ),
                        ])
                    ])
                ]),
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Sigara'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-22',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['smoker'].unique()],
                                value=DF['smoker'].unique()[0]
                            ),
                        ])
                    ])
                ]),
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Gün'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-23',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['day'].unique()],
                                value=DF['day'].unique()[0]
                            ),
                        ])
                    ])
                ]),
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Öğün'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-24',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['time'].unique()],
                                value=DF['time'].unique()[0]
                            ),
                        ])
                    ])
                ]),
            ]),
            html.Section(className='hero is-info mb-3', children=[
                html.Div(className='hero-body', children=[
                    html.P('Butonlar',
                           className='title')
                ])
            ]),
            html.Div(className='columns', children=[
                html.Div(className='column', children=[
                    html.Div(className='field is-grouped', children=[
                        html.Div(className='control', children=[
                            html.Button('Buton', className='button is-primary')
                        ]),
                        html.Div(className='control', children=[
                            html.Button(
                                'Buton', className='button is-primary is-light')
                        ]),
                        html.Div(className='control', children=[
                            html.Button('Buton', className='button is-link')
                        ]),
                        html.Div(className='control', children=[
                            html.Button('Buton', className='button is-success')
                        ]),
                        html.Div(className='control', children=[
                            html.Button('Buton', className='button is-warning')
                        ]),
                        html.Div(className='control', children=[
                            html.Button('Buton', className='button is-danger')
                        ]),
                    ])
                ]),
            ]),
            html.Section(className='hero is-warning mb-3', children=[
                html.Div(className='hero-body', children=[
                    html.P('Genelde Ekranlarda Kullanacağımız Yapı',
                           className='title'),
                    html.P('Sevilen bir kullanım şekli', className='subtitle')
                ])
            ]),
            html.Div(className='columns', children=[
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Cinsiyet'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-31',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['sex'].unique()],
                                value=DF['sex'].unique()[0]
                            ),
                        ])
                    ]),
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                             'Sigara'
                             ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                 id='dd-32',
                                 style={'width': '100%'},
                                 options=[{'label': _, 'value': _}
                                          for _ in DF['smoker'].unique()],
                                 value=DF['smoker'].unique()[0]
                                 ),
                        ])
                    ]),
                ]),
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Cinsiyet'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-33',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['sex'].unique()],
                                value=DF['sex'].unique()[0]
                            ),
                        ])
                    ]),
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                             'Sigara'
                             ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                 id='dd-34',
                                 style={'width': '100%'},
                                 options=[{'label': _, 'value': _}
                                          for _ in DF['smoker'].unique()],
                                 value=DF['smoker'].unique()[0]
                                 ),
                        ])
                    ]),
                ]),
                html.Div(className='column is-one-fifth', children=[
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                            'Cinsiyet'
                        ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                id='dd-35',
                                style={'width': '100%'},
                                options=[{'label': _, 'value': _}
                                         for _ in DF['sex'].unique()],
                                value=DF['sex'].unique()[0]
                            ),
                        ])
                    ]),
                    html.Div(className='field', children=[
                        html.Label(className='label', children=[
                             'Sigara'
                             ]),
                        html.Div(className='control', children=[
                            dcc.Dropdown(
                                 id='dd-36',
                                 style={'width': '100%'},
                                 options=[{'label': _, 'value': _}
                                          for _ in DF['smoker'].unique()],
                                 value=DF['smoker'].unique()[0]
                                 ),
                        ])
                    ]),
                ]),
                html.Div(className='column', children=[
                    html.Table(className='table is-fullwidth is-hoverable', children=[
                        html.Thead(children=[
                            html.Tr(children=[
                                html.Th('Özet'),
                                html.Th(''),
                            ])
                        ]),
                        html.Tbody(children=[
                            html.Tr(children=[
                                html.Td('Yıl'),
                                html.Td('2020'),
                            ]),
                            html.Tr(children=[
                                html.Td('Toplam Harcama'),
                                html.Td('123456'),
                            ]),
                            html.Tr(children=[
                                html.Td('Kategori'),
                                html.Td('Dummy'),
                            ]),
                            html.Tr(children=[
                                html.Td('Text'),
                                html.Td('Dummy'),
                            ]),
                            html.Tr(children=[
                                html.Td('Birim'),
                                html.Td('Dummy'),
                            ]),
                            html.Tr(children=[
                                html.Td('Bölge'),
                                html.Td('Dummy'),
                            ]),
                        ])
                    ])
                ])
            ])
        ]),
        html.Section(className='section', children=[
            html.Div(className='columns', children=[
                html.Div(className='column is-one-third', children=[
                    html.Label('Cinsiyetlere Göre Bahşişler [Center]',
                               className='label has-text-centered'),
                    dcc.Graph(figure=px.bar(data_frame=DF,
                                            x='tip', y='sex').update_layout(paper_bgcolor=component_builder.FIGURE_STYLE[0]['paper_bgcolor'], plot_bgcolor=component_builder.FIGURE_STYLE[0]['plot_bgcolor']))
                ]),
                html.Div(className='column is-one-third', children=[
                    html.Label('Günlere Göre Bahşişler [Justified]',
                               className='label has-text-justified	has-text-primary'),
                    dcc.Graph(figure=px.pie(data_frame=DF,
                                            values='tip', names='day'))
                ]),
                html.Div(className='column is-one-third', children=[
                    html.Label('Sigara Durumuna Göre Bahşişler [Right]',
                               className='label has-text-right has-text-link'),
                    dcc.Graph(figure=px.pie(data_frame=DF,
                                            values='tip', names='smoker'))
                ]),
            ])
        ]),
        html.Section(className='section', children=[
            html.Div(className='box', children=[
                html.Div(className='columns', children=[
                    html.Div(className='column is-one-third', children=[
                        html.Label('Cinsiyetlere Göre Bahşişler [Center]',
                                   className='label has-text-centered'),
                        dcc.Graph(figure=px.bar(data_frame=DF,
                                                x='tip', y='sex').update_layout(paper_bgcolor=component_builder.FIGURE_STYLE[0]['paper_bgcolor'], plot_bgcolor=component_builder.FIGURE_STYLE[0]['plot_bgcolor']))
                    ]),
                    html.Div(className='column is-one-third', children=[
                        html.Label('Günlere Göre Bahşişler [Justified]',
                                   className='label has-text-justified	has-text-primary'),
                        dcc.Graph(figure=px.pie(data_frame=DF,
                                                values='tip', names='day'))
                    ]),
                    html.Div(className='column is-one-third', children=[
                        html.Label('Sigara Durumuna Göre Bahşişler [Right]',
                                   className='label has-text-right has-text-link'),
                        dcc.Graph(figure=px.pie(data_frame=DF,
                                                values='tip', names='smoker'))
                    ]),
                ])
            ])
        ]),
    ])
    return layout
