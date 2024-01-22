import pypyodbc
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Veritabanından veri çekmek için fonksiyon
def veri_al(sehir):
    connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-UU1HEIE\SQLEXPRESS;DATABASE=Trafikk;UID=sa;PWD=1234')
    cursor = connection.cursor()


    cursor.execute("""
    SELECT
      sehir,
      MIN(CAST(kaza_tarih AS DATE)) AS kaza_tarih,
      kaza_bilgileri
    FROM
      tablo_kaza haber
    INNER JOIN
      tablo_adres adres
    ON
      haber.kaza_adres_id = adres.adres_id
    GROUP BY
      sehir, kaza_bilgileri
    ORDER BY
      sehir ASC;
    """)

    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['sehir', 'kaza_tarih', 'kaza_bilgileri'])
    
    if sehir:
        df = df.loc[df['sehir'] == sehir]

    cursor.close()
    connection.close()

    return df

# Ana sayfa için route
@app.route('/')
def ana_sayfa():
    sehir = request.args.get('sehir', '')
    df = veri_al(sehir)
    return render_template('index.html', data=df.to_html(index=False))

if __name__ == '__main__':
    app.run(debug=True)
