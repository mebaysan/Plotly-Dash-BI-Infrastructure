GUNLER = ['Pazartesi', 'Salı', 'Çarşamba',
          'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']

GUNLER_SAYI = [_ for _ in range(1, 32)]

AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
         'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

AYLAR_SAYI = [_ for _ in range(1, 13)]
AY_SAYI_DICT = dict(zip(AYLAR, AYLAR_SAYI))
SAYI_AY_DICT = dict(zip(AYLAR_SAYI, AYLAR))
AYLAR_FILTRE = []

for i in AY_SAYI_DICT:
    AYLAR_FILTRE.append({'label': i, 'value': AY_SAYI_DICT[i]})
