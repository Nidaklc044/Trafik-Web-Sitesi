from flask import Flask, render_template
import pypyodbc
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Bağlantı
    connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-UU1HEIE\SQLEXPRESS;DATABASE=Trafikk;UID=sa;PWD=1234')
    cursor = connection.cursor()

    # SQL sorgusu
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

    # Çekilen verileri pandas dataframe aktarma
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['sehir', 'kaza_tarih', 'kaza_bilgileri'])

    # Kullanıcıdan şehir girdisi alma
    sehir = input("Lütfen şehir giriniz: ")

    # Şehre göre filtreleme
    df = df.loc[df['sehir'] == sehir]

    cursor.close()
    connection.close()

    # Verileri HTML dosyasına aktararak gösterme
    return render_template('index.html', data=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
