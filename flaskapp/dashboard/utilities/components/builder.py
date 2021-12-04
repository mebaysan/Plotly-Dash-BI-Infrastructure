import plotly.express as px
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from plotly.subplots import make_subplots
import math
import dash
from flaskapp.dashboard.layout import html_layout
from dash.dependencies import Input, Output
import dash_table
from flaskapp.models.file import FileModel


class ComponentBuilder(object):

    """
    Kullanmak için Dash uygulamasına Bulma CSS'i eklemelisiniz:
    dash.Dash(__name__,
                    external_stylesheets=[
                        "/static/node_modules/bulma/css/bulma.min.css"
                    ])
    """

    def __init__(self):
        self.PLOT_THEME = 'plotly_white'
        self.MAIN_COLOR_1 = '#66bb6a'
        self.MAIN_COLOR_2 = '#bcaaa4'
        self.MAIN_TEXT_FONT_SIZE = 14
        self.HELPER_TEXT_FONT_SIZE = 12
        self.FIGURE_STYLE = {
            'figureTextSize': self.HELPER_TEXT_FONT_SIZE,
            'figureTitleTextSize': self.MAIN_TEXT_FONT_SIZE,
            'paper_bgcolor': '#fff',  # plotly grafik kağıdı arka plan rengi
            'plot_bgcolor': '#fff',  # plotly grafik arka plan rengi
            'header_fill_color': self.MAIN_COLOR_1,
            'header_font': '#FFFFFF',
            'cells_fill_color': self.MAIN_COLOR_2,
            'cells_font': '#F5F5F5',
            'color_discrete_sequence': px.colors.qualitative.Dark2
        },
        self.SPECIAL_INPUT_KEY = 'Hepsi'  # Verileri filtrelerken kendi ekranlarımız için bir özel key. Mesela 'Hepsi' olduğunda dropdownlara 'Hepsi' gelecek bu sayede bir değişkende bir değeri filtrelerken diğerlerinde hepsini seçebiliyoruz
        self.EXTERNAL_STYLESHEETS = [
            "/static/node_modules/bulma/css/bulma.min.css",
            "/static/css/customdash.css"
        ]  # Dash instance oluştururken component builder'in style sheets'ini göndereceğiz
        self.META_TAGS = [
            {"name": "viewport",
             "content": "width=device-width, initial-scale=1"}
        ]  # Dash instance oluştururken component builder'in meta tags'lerini göndereceğiz
        self.LAYOUT_CLASSNAME = 'container'
        self.MONTHS = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs',
                               'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        self.MONTHS_NUMBERS = [_ for _ in range(1, 13)]
        self.DAYS = ['Pazartesi', 'Salı', 'Çarşamba',
                     'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        self.DAYS_NUMBERS = [_ for _ in range(1, 32)]
        self.TABLE_ALIGN = 'center'  # table yazı pozisyonu
        self.TABLE_HEADER_COLOR = '#FFFFFF'  # table header yazı color
        # table header fill (arka plan) color
        self.TABLE_HEADER_FILL_COLOR = 'grey'
        self.TABLE_CELLS_COLOR = 'grey'  # table hücre yazı color
        # table cells fill (arka plan) color
        self.TABLE_CELLS_FILL_COLOR = '#FFFAFA'
        # table hücre aralarındaki çizgi renkleri
        self.TABLE_LINE_COLOR = 'darkslategray'
        # basic table içerisindeki metinlerin font size'ı
        self.TABLE_STYLE = {'fontSize': self.MAIN_TEXT_FONT_SIZE}
        self.INPUT_LABEL_STYLE = {
            'fontSize': self.MAIN_TEXT_FONT_SIZE}  # input label font
        # input'lar içerisindeki font
        self.INPUT_STYLE = {'fontSize': self.HELPER_TEXT_FONT_SIZE}
        self.HELP_TEXT_STYLE = {
            'fontSize': self.HELPER_TEXT_FONT_SIZE}  # help text font
        # button text font
        self.BUTTON_STYLE = {'fontSize': self.MAIN_TEXT_FONT_SIZE}
        self.DASH_LAYOUT_CLASS = 'box'  # dash app'lerine ait tabların layoutları için
        # ana dash uygulamalarının layoutu için
        self.LAYOUT_STYLE = {'marginTop': '50px'}

    def get_basic_table(self, headers, rows, is_in_column=True, column_class='', table_style={}):
        """
        headers -> liste olarak gelecek
        rows    ->  dict olarak gelecek
        """
        _table_style = self.TABLE_STYLE.copy()
        if table_style:
            for i in table_style:
                _table_style[i] = table_style[i]
        table_rows = []
        for row in rows:
            table_rows.append(
                html.Tr(children=[html.Td(f'{row}'), html.Td(f'{rows[row]}')]))
        table = html.Table(style=_table_style, className='table is-fullwidth is-hoverable',
                           children=[
                               html.Thead(children=[
                                   html.Tr(children=[
                                       html.Th(headers[0]),
                                       html.Th(headers[1]),
                                   ])
                               ]),
                               html.Tbody(children=table_rows)
                           ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[table])
            return column
        return table

    def get_tabs(self, tabs_style='is-fullwidth', tabs_id='tabs', tab_items={}):
        """
        Tab Style için:
        https://bulma.io/documentation/components/tabs/
        is-fullwidth
        is-right
        is-centered
        is-small
        is-medium
        is-large
        *********************************
        tabs_id -> sayesinde sayfa içeriğini değiştirebileceğiz
        *********************************
        tab_items -> {'Tab Title':'Tab-Link'}
        """
        _tab_items = []
        for tab_item in tab_items:
            _tab_items.append(
                html.Li(html.A(tab_item, href=tab_items[tab_item])))
        tabs = html.Div(className=f'tabs {tabs_style}', id=tabs_id, children=[
            html.Ul(children=_tab_items)
        ])
        return tabs

    def get_dropdown_input(self, data_frame, filter_column, label,  input_id, label_class='', label_style={}, special_key_in_option=True, default_value='self', dropdown_style={}, is_in_column=True, column_class='', help_text='', help_text_class='is-success', is_year=False, is_month=False):
        """
        data_frame -> hangi veri seti
        filter_column -> dropdown'da hangi değişkene ait veriler gözükecek
        label -> input başlığı
        label_class -> label'a extra class gelecek mi
        label_style -> label'a özel stil verilecek mi
        input_id -> callback'leri çalıştırırken hangi id ile bu elementi yakalayacağız
        special_key_in_option -> self.SPECIAL_INPUT_KEY filtrede olacak mı (mesela Hepsi seçeneği)
        default_value -> dropdown'un başlangıç değeri (first veya self alabilir, first alırsa ilgili değişkenin tekil değerlerinin ilk elemanını başlangıç değeri olarak set eder), max alırsa ilgili kolonun en büyük değerini alır (Yıl vb için kullanıyoruz)
        dropdown_style -> dropdown'a css verilecekse dict olarak gelmeli
        is_in_column -> input column içine alınacak mı
        column_class -> column içine alınacaksa column style'ı ne olacak
        help_text -> input altında uyarı metni yazacak mı
        help_text_class -> help textin class'ı (Bulma'dan gelen is-primary vb)
        is_year -> Bu dropdown yılları mı listeleyecek, öyle ise büyükten küçüğe sıralayacak
        is_month -> Bu dropdown ayları mı listeleyecek, öyle ise bu sınıfın kendi MONTHS prop'una göre sıralanacak
        """
        if type(data_frame) == list:
            # liste içinde dict'ler -> [{'label':'Türk Lirası','value':'TL Cinsinden Proje Toplam'}]
            options = data_frame
            if default_value == 'first':
                value = options[0]['value']
            elif default_value == 'last':
                value = options[len(options) - 1]['value']
            else:
                value = self.SPECIAL_INPUT_KEY
        elif type(data_frame) == pd.DataFrame:  # DataFrame gelirse
            if is_year:
                data_frame.sort_values(
                    filter_column, ascending=False, inplace=True)
            if is_month:
                data_frame[filter_column] = pd.Categorical(
                    data_frame[filter_column], categories=self.MONTHS, ordered=True)  # eğer ay değişkeni ise gelen veri setinin ilgili değişkenini Categorical olarak işaretle ve bunu kendi ay sıralamana göre (self.MONTHS) sırala
                data_frame.sort_values(f'{filter_column}', inplace=True)
            OPTIONS = data_frame[f'{filter_column}'].unique()
            options = [{'label': _, 'value': _} for _ in OPTIONS]
            options.insert(0, {'label': self.SPECIAL_INPUT_KEY,
                               'value': self.SPECIAL_INPUT_KEY}) if special_key_in_option else options
            if default_value == 'first':
                value = data_frame[filter_column].unique()[0]
            elif default_value == 'max':
                value = data_frame[filter_column].max()
            elif default_value == 'min':
                value = data_frame[filter_column].min()
            elif default_value == 'last':
                value = data_frame[filter_column].unique()[-1]
            elif type(default_value) == tuple:
                value = default_value[0]
            else:
                value = self.SPECIAL_INPUT_KEY
        else:
            return TypeError

        _label_style = self.INPUT_LABEL_STYLE.copy()
        if label_style:
            for i in label_style:
                _label_style[i] = label_style[i]

        _dropdown_style = self.INPUT_STYLE.copy()
        if dropdown_style:
            for i in dropdown_style:
                _dropdown_style[i] = dropdown_style[i]

        field = html.Div(className='field', children=[
            html.Label(className=f'label {label_class}', style=_label_style, children=[
                f'{label}'
            ]),
            html.Div(className='control', children=[
                dcc.Dropdown(
                    id=input_id,
                    options=options,
                    value=value,
                    style=_dropdown_style
                ),
            ]),
            html.P(f'{help_text}', className=f'help {help_text_class}')
        ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[field])
            return column
        return field

    def get_input_text(self, label,  input_id, input_type, label_class='', label_style={}, default_value='self', input_style={}, input_class='is-primary', is_in_column=True, column_class='', help_text='', help_text_class='is-success', help_text_style={}, editable=True):
        """
        label -> input başlığı
        label_class -> label'a extra class gelecek mi
        label_style -> label'a özel stil verilecek mi
        input_id -> callback'leri çalıştırırken hangi id ile bu elementi yakalayacağız
        input_type -> number, text, email vb (dcc'den bakabilirsiniz)
        input_style -> input'a extra css vermek ister misiniz
        input_class -> input'a extra class vermek ister misiniz
        default_value -> input'un başlangıç değeri
        is_in_column -> input column içine alınacak mı
        column_class -> column içine alınacaksa column style'ı ne olacak
        help_text -> input altında uyarı metni yazacak mı
        help_text_class -> help textin class'ı (Bulma'dan gelen is-primary vb)
        editable -> True ise yazmaya izin vermez
        """
        if default_value == 'self':
            value = self.SPECIAL_INPUT_KEY
        else:
            value = default_value

        _label_style = self.INPUT_LABEL_STYLE.copy()
        if label_style:
            for i in label_style:
                _label_style[i] = label_style[i]

        _input_style = self.INPUT_STYLE.copy()
        if input_style:
            for i in input_style:
                _input_style[i] = input_style[i]

        _help_text_style = self.HELP_TEXT_STYLE.copy()
        if help_text_style:
            for i in help_text_style:
                _help_text_style[i] = help_text_style[i]

        field = html.Div(className='field', children=[
            html.Label(className=f'label {label_class}', style=_label_style, children=[
                f'{label}'
            ]),
            html.Div(className='control', children=[
                dcc.Input(
                    id=input_id,
                    className=f'input {input_class}',
                    type=input_type,
                    value=value,
                    style=_input_style,
                    readOnly=False if editable == True else True
                ),
            ]),
            html.P(f'{help_text}', className=f'help {help_text_class}',
                   style=_help_text_style)
        ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[field])
            return column
        return field

    def get_button(self, label, button_id, button_class='is-primary', button_style={}, default_nclick=1, is_in_column=False, column_class='', is_href=False, href=''):
        """
        label -> buton üzerinde ne yazacak
        button_id -> butona nasıl erişilecek (callbackler için hangi id'den tetiklenecek vb.)
        button_class -> butona özel class verecek miyiz
        button_style -> butona özel stil vermek istersek
        default_nclick -> default kaç click ile initialize olacak
        is_in_column -> column içinde mi
        column_class -> column içindeyse column class'ı ne olacak (boş gelirse auto olarak alır)
        is_href -> True ise button A tagı içerisine gömülür
        href -> is_href = True ise A tagına koyulacak olan link (ref)
        """

        _button_style = self.BUTTON_STYLE.copy()
        if button_style:
            for i in button_style:
                _button_style[i] = button_style[i]

        button = html.Div(className='buttons', children=[
            html.Button(
                f'{label}', className=f'button {button_class}', id=button_id, n_clicks=default_nclick, style=_button_style)
        ])
        if is_href:
            button = html.A(children=[button], href=href)
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[button])
            return column
        return button

    def get_graph_column(self, label, label_id, figure, figure_id, label_class='', column_class='', label_style={}, column_style={}):
        """
        label -> grafiğin başlığı (ya da üzerinde ne gözükecekse / bu sayede grafiğin oluşturulduğu svg içine title atmadan daha fazla yer kazanabileceğiz)
        label_id -> filtrelerden gelen verilere göre dinamik olarak title oluşturmak istersek çıktıyı Output() ile göndermek için bu id'e ihtiyacımız olacak
        figure -> column içindeki dcc.Graph() altında gözükecek olan figure
        figure_id -> figure'e output vermek için kullanacağımız id
        label_class -> labellara class vermek istersek kullanacağımız parametre
        column_class -> columnlara class vermek istersek kullanacağımız parametre
        label_style -> label'a özel olarak stil vermek istersek
        column_style -> column'a özel olarak stil vermek istersek
        """
        column = html.Div(className=f'column {column_class}', style=column_style, children=[
            html.Label(f'{label}', id=label_id,
                       style=label_style,
                       className=f'label {label_class}'),
            dcc.Graph(id=figure_id, figure=figure)])

        return column

    def get_sankey(self, data, path, value_col):
        # bir veri seti alır, ve gelen path parametresine göre sankey diyagramı için dict oluşturur
        # value_col parametresine göre diyagram üzerinde göstereceği value'leri set eder
        """
        Örnek bir kullanım

        my_sankey = get_sankey(
            sankey_df,['Kategori','Projeli_mi','Ürün Adı'],'Miktar')
        fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = my_sankey['label'],
        color = "blue"
        ),
        link = dict(
        source = my_sankey['source'],
        target = my_sankey['target'],
        value = my_sankey['value']
        ))])
        """

        sankey_data = {
            'label': [],
            'source': [],
            'target': [],
            'value': []
        }
        counter = 0
        while (counter < len(path) - 1):
            for parent in data[path[counter]].unique():
                sankey_data['label'].append(parent)
                for sub in data[data[path[counter]] == parent][path[counter+1]].unique():
                    sankey_data['source'].append(
                        sankey_data['label'].index(parent))
                    sankey_data['label'].append(sub)
                    sankey_data['target'].append(
                        sankey_data['label'].index(sub))
                    sankey_data['value'].append(
                        data[data[path[counter+1]] == sub][value_col].sum())

            counter += 1
        return sankey_data

    def get_data_table(self, title, headers, values, row_size=0, is_autosize=False, row_height=30, is_return_trace=False, is_fill_color=False, color_palette=[]):
        """Özet

        Args:
            title (string): oluşacak grafiğin başlığı
            headers (list): tablonun başlıklarını liste olarak alır
            values (list): tablonun hücrelerini (cells) liste olarak alır. her sütun bir liste içerisinde gelmelidir. [[Sütun 1], [Sütun 2], [Sütun 3]...]
            row_size(int): veri seti içerisindeki satır adedi
            is_autosize(bool): tablo otomatik olarak resize olsun mu
            row_height(int): bir satırın yüksekliği ne kadar olsun
            is_return_trace(bool): True olursa trace'i döner, False olursa figure döner
            is_fill_color(bool): True olursa color_palette parametresini color olarak set eder
            color_palette(list): satırları boyayacağımız renk kodlarını içerir, her satıra karşılık gelen bir renk kodu içermeli (liste içerisinde liste gelmeli)
                    - Ör: color_palette = [df['Renk']]
        Returns:
            figure: graph objects figure döner (table)
        """
        trace = go.Table(
            header=dict(values=headers,
                        fill_color=self.TABLE_HEADER_FILL_COLOR,
                        font={'color': self.TABLE_HEADER_COLOR},
                        line_color=self.TABLE_LINE_COLOR,
                        align=self.TABLE_ALIGN),
            cells=dict(values=values,
                       font={'color': self.TABLE_CELLS_COLOR},
                       #    line_color=self.TABLE_LINE_COLOR if is_fill_color == False else color_palette,
                       line_color=self.TABLE_LINE_COLOR,
                       fill_color=self.TABLE_CELLS_FILL_COLOR if is_fill_color == False else color_palette,
                       align=self.TABLE_ALIGN
                       ))
        if is_return_trace:
            return trace
        layout = go.Layout(title=title,
                           template=self.PLOT_THEME)
        fig = go.Figure(data=[trace], layout=layout)
        if is_autosize:
            height = row_size * row_height
            if row_size <= 13:
                height = 450
            elif row_size >= 26:
                height = height + height / 3
            fig.update_layout(height=height)
        return fig

    def get_real_data_table(self, id, headers, values, editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            row_deletable=False,
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            style_header={},
                            style_cell={},
                            style_data={}):
        """Özet

        Args:
            id (string): oluşacak grafiğin başlığı
            headers (list): tablonun başlıklarını liste olarak alır
            values (list): tablonun hücrelerini (cells) liste olarak alır. her sütun bir liste içerisinde gelmelidir. [[Sütun 1], [Sütun 2], [Sütun 3]...]
        Returns:
            table: html children içerisine dönecek olan element, children içerisinde dönmelidir. Graph değildir
        """
        values = [_.values for _ in values]
        df = pd.DataFrame(dict(zip(headers, values)))
        style_header['fontSize'] = self.MAIN_TEXT_FONT_SIZE
        # style_header['backgroundColor'] = self.TABLE_HEADER_COLOR
        ########################
        style_cell['fontSize'] = self.HELPER_TEXT_FONT_SIZE
        ########################
        style_data['fontSize'] = self.HELPER_TEXT_FONT_SIZE
        # style_data['backgroundColor'] = self.TABLE_CELLS_COLOR

        table = dash_table.DataTable(id=id, columns=[{'name': i, 'id': i} for i in headers], data=df.to_dict('records'),
                                     editable=editable,
                                     filter_action=filter_action,
                                     sort_action=sort_action,
                                     sort_mode=sort_mode,
                                     row_deletable=row_deletable,
                                     page_action=page_action,
                                     page_current=page_current,
                                     page_size=page_size,
                                     style_header=style_header,
                                     style_cell=style_cell,
                                     style_data=style_data
                                     )
        return table

    def get_download_button(self, id, button_text='Veri Setini İndir', button_style={}, default_nclicks=0):
        """Download button verir

        Args:
            id (str): Button id
            button_text (str, optional): Button üzerinde yazacak metin. Defaults to 'Veri Setini İndir'.
            button_style (dict, optional): Butona eklenmek istenen css özellikleri. Defaults to {}.
            default_nclicks (int, optional): Buton default olarak kaç adet clicklenmiş gelecek. Defaults to 0.

        Returns:
            button: Html Div ile sarmalanmış A etiketi.
        """
        style = {}
        # style = {'float': 'left'}
        for stl in button_style:
            style[stl] = button_style[stl]
        button = html.Div(style=style, className='navbar-item has-dropdown is-hoverable baysan-download-div', children=[
            html.A(button_text, id=id, className='navbar-link baysan-download-btn',
                   n_clicks=default_nclicks)
        ])
        return button

    def get_download_action(self, app, config, download_button_id, states, df, filter_function, file_name, file_type='csv'):
        """Download butonunun id'sine göre otomatik olarak ekrana filtrelenmiş veriyi indirme özelliği sağlıyor

        Args:
            app (Dash): hangi ekranda bu özelliği kullanmak istiyorsak, o ekranın Dash app'inin tutulduğu `app` değişkeni
            config (dict): dashboard sabitlerinin tutulduğu CONFIG değişkeni
            download_button_id (str): dashboard'ın screen dosyasındaki download button id
            states (State): Dash State, ekran hangi componentlerden filtre girdisi alıyor
            df (DataFrame): hangi veri setini filtrelemek istiyoruz
            filter_function (function): Veri setini filtrelemek için hangi değişkeni kullanacağız
            csv_name (str): Export edilecek CSV dosya adı

        Returns:
            app değişkenine callback'i yükler, return yok

        Examples:
            component_builder = ComponentBuilder()
            component_builder.get_download_action(app, CONFIG, 'yetim-sponsorluklar-data-download-btn', STATES, DF, data_filtrele, 'YetimSponsorluklar.xls')
        """
        file_name = file_name + '.' + file_type

        @app.callback(
            Output(download_button_id, 'href'),
            Input(download_button_id, 'n_clicks'),
            states
        )
        def get_data_download_csv(n_clicks, *args):
            if n_clicks >= 1:
                filtered_df = filter_function(df, *args)
                return FileModel.create_csv_and_return_url(file_name, config['APP_PATH'], filtered_df)

    def get_subplot_tables_three_columns(self, df, main_col, first_col, second_col, third_col, _titles, _print_grid=False):
        """
        df = gruplanmış veri seti
        main_col = hangi kolona göre gruplanacak
        first_col = ilk kolon
        second_col = ikinci kolon
        third_col = üçüncü kolon
        _titles = liste olarak title'lar

        Bu fonksiyon kontrol_denetim altındaki aylık işlem özet ekranı için yazıldı.
            Daha da güzelleştirilebilir.
            Eğer bu yorumu okuyorsanız gelişmişine ihtiyaç duymadığımızdan sadece o ekrandaki tablolara özel kalmıştır demektir :)
        """

        row_count = math.ceil(len(df[main_col].unique()) / 2)
        col_count = 2

        fig_specs = []  # hangi subplot nereye gelecek
        for i in range(row_count):
            fig_specs.append([{"type": "table"} for _ in range(col_count)])

        titles = []
        for baskanlik in df[main_col].unique():
            dummy = df.groupby(main_col, as_index=False).sum()
            titles.append("{} (%{})".format(baskanlik, round(
                dummy[dummy[main_col] == baskanlik][third_col].sum(), 2)))

        fig = make_subplots(rows=row_count, cols=col_count,
                            specs=fig_specs, subplot_titles=titles, vertical_spacing=0.08, print_grid=_print_grid)

        row_counter = 1
        col_counter = 1
        counter = 0

        for trace in df[main_col].unique():
            fig.add_trace(
                self.get_data_table(
                    trace, _titles, [
                        df[df[main_col] == trace][first_col],
                        df[df[main_col] == trace][second_col],
                        df[df[main_col] == trace][third_col].apply(
                            lambda x: round(x, 2))
                    ], is_return_trace=True),
                row=row_counter,
                col=col_counter
            )
            counter += 1
            if counter % 2 == 1:
                col_counter = 2
            else:
                col_counter = 1
            if counter % col_count == 0:
                row_counter += 1
        return fig

    def update_figure_layout(self, fig,
                             title_x=None,
                             title_y=None,
                             paper_bgcolor=None,
                             plot_bgcolor=None,
                             plot_theme=None,
                             font_size=None,
                             title_font_size=None,
                             autosize=True,
                             margin={},
                             margin_autoexpand=True,
                             width=None,
                             height=None,
                             title=None,
                             **kwargs
                             ):
        """
        parametre olarak aldığı figürü update eder ve döndürür
        """
        fig.update_layout(
            paper_bgcolor=self.FIGURE_STYLE[0]['paper_bgcolor'] if paper_bgcolor == None else paper_bgcolor,
            plot_bgcolor=self.FIGURE_STYLE[0]['plot_bgcolor'] if plot_bgcolor == None else plot_bgcolor,
            template=self.PLOT_THEME if plot_theme == None else plot_theme,
            font_size=self.FIGURE_STYLE[0]['figureTextSize'] if font_size == None else font_size,
            title_font_size=self.FIGURE_STYLE[0]['figureTitleTextSize'] if title_font_size == None else title_font_size,
            autosize=autosize,
            margin=margin,
            margin_autoexpand=margin_autoexpand,
            **kwargs
        )
        if title_x:
            fig.update_layout(title_x=title_x)
        if title_y:
            fig.update_layout(title_y=title_y)
        if width:
            fig.update_layout(width=width)
        if height:
            fig.update_layout(height=height)
        if title:
            fig.update_layout(title=title)
        return fig

    def create_figure_layout(self, title):
        """
        gelen başlığa göre bir layout oluşturur
        """
        layout = go.Layout(title=title, template=self.PLOT_THEME)
        return layout

    def create_columns_with_figures(self, ids=[], styles=None, types=None):
        """
        her id için column içinde bir Graph oluşturur ve columns div ile sarmalar
        styles eğer gelmezse klasik column style ekler, eğer column'lara class verilmek istenirse ilgili id'nin indexini ilgili class ile göndermek gerek,
            diğerlerini '' boş str olarak gönder
        types eğer gelmezse hepsini graph olarak işaretler. Bu liste içerisine graph veya div değerleri gelebilir. graph gelirse o id ile bir Graph ekler, div gelirse Div ekler.
        """
        graphs = []
        if styles == None:
            styles = ['column ' for _ in ids]
        else:
            styles = [f'column {_}' for _ in styles]

        if types == None:
            types = ['graph' for _ in ids]
        else:
            types = types

        for (id, style, type) in zip(ids, styles, types):
            if type == 'graph':
                graphs.append(html.Div(className=style,
                                       children=[dcc.Graph(id=id)]))
            elif type == 'div':
                graphs.append(html.Div(id=id, className=style))

        columns = html.Div(className='columns', children=graphs)
        return columns

    def get_tabs_layout(self, tabs):
        """
        parametre olarak aldığı tablardan oluşan bir div döner (dash appleri içerisinde navigasyon için)
        tab_items -> dict olarak kelmeli key: Tab Text, value: Tab URL
        """
        layout = html.Div(
            [
                dcc.Location(id="url"), tabs,
                html.Div(id="page-content")
            ],
            className=self.LAYOUT_CLASSNAME,
            style=self.LAYOUT_STYLE
        )
        return layout

    def get_tab_screens(self, app, config, screens):
        """
        her tab url'e ilgili screen'i dönmesi için kullanılır
        screens -> dict'lerden oluşan bir list olarak gelmeli
        Her dict -> {'screen': 'screen-value', 'function': function, 'data': [Data1, Data2]}
        """
        @app.callback(
            Output("page-content", "children"),
            Input('url', 'pathname')
        )
        def render_tab_content(pathname):
            if len(screens) <= 1:  # eğer tek ekran varsa ilk sayfa açıldığında ilk elemanı dönsün
                scr = screens[0]
                func = scr['function']
                return func(*scr['data'])
            else:
                for screen in screens:
                    if pathname == config['BASE_URL']+screen['screen']:
                        func = screen['function']
                        return func(*screen['data'])
                    # elif pathname != config['BASE_URL']+screen['screen']:  # ilk sayfa açıldığında ilk elemanı dönsün
                    #     scr = screens[0]
                    #     func = scr['function']
                    #     return func(*scr['data'])
        return app

    def bind_callbacks_to_app(self, app, callbacks):
        """
        gelen callback'leri app'e uygular ve app'i return eder
        callbacks -> dict'lerden oluşan bir liste olarak gelmeli
        Her dict -> {'function':function,'data':[Data1,Data2]}
        """
        for obj in callbacks:
            func = obj['function']
            # her callback fonksiyonunun ilk parametresi app olduğundan ilgili listeye app'i ekler
            obj['data'].insert(0, app)
            app = func(*obj['data'])
        return app

    def get_dash_app(self, server, config, tabs, callbacks, screens):
        """
        Dash instance'indan app oluşturur ve döner
        """
        app = dash.Dash(server=server,
                        routes_pathname_prefix=config['BASE_URL'],
                        suppress_callback_exceptions=True,
                        external_stylesheets=self.EXTERNAL_STYLESHEETS)
        app.index_string = html_layout
        app.layout = self.get_tabs_layout(tabs)
        app = self.bind_callbacks_to_app(app, callbacks)
        app = self.get_tab_screens(app, config, screens)
        return app
