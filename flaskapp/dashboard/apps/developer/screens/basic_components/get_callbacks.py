

def data_filtrele(DF, yil, fon, sektor, birim, calisma_sahasi, faliyet, kita):
    filtered_df = DF
    filtered_df = filtered_df[filtered_df['Yıl']
                              == yil] if yil != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['Fon Adı']
                              == fon] if fon != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['Sektör Adı']
                              == sektor] if sektor != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['Birim Adı']
                              == birim] if birim != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['Çalışma Sahası'] ==
                              calisma_sahasi] if calisma_sahasi != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['Faliyet Adı']
                              == faliyet] if faliyet != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['Kıta Adı']
                              == kita] if kita != 'Hepsi' else filtered_df
    return filtered_df


def get_callbacks(app, DF, component_builder):

    return app
