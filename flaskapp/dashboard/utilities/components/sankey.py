def get_sankey(data, path, value_col):
    # bir veri seti alır, ve gelen path parametresine göre sankey diyagramı için dict oluşturur
    # value_col parametresine göre diyagram üzerinde göstereceği value'leri set eder
    """
    Örnek bir kullanım
    
    my_sankey = get_sankey(sankey_df,['Kategori','Projeli_mi','Ürün Adı'],'Miktar')
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
                sankey_data['target'].append(sankey_data['label'].index(sub))
                sankey_data['value'].append(
                    data[data[path[counter+1]] == sub][value_col].sum())

        counter += 1
    return sankey_data
