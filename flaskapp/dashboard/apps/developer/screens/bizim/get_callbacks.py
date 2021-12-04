from dash.dependencies import Input, Output


def get_callbacks(app, DF, component_builder):

    @app.callback(
        Output('d-tablo', 'figure'),
        Input('custom-btn1', 'n_clicks')
    )
    def get_table(n_clicks):
        basliklar = ['Başlık 1', 'Başlık 2']
        degerler = [
            [1, 2],
            [1, 2],
        ]
        fig = component_builder.get_data_table('Tablo', basliklar, degerler)
        fig = component_builder.update_figure_layout(fig)
        return fig

    return app
