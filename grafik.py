import pypyodbc
import matplotlib.pyplot as plt
import pandas as pd

# Connect to the database
connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-UU1HEIE\SQLEXPRESS;DATABASE=Trafikk;UID=sa;PWD=1234')

# Set up the cursor
cursor = connection.cursor()

# Execute the query
cursor.execute("""
SELECT
  CASE MONTH(tablo_kaza.kaza_tarih)
    WHEN 1 THEN 'Ocak'
    WHEN 2 THEN 'Şubat'
    WHEN 3 THEN 'Mart'
    WHEN 4 THEN 'Nisan'
    WHEN 5 THEN 'Mayıs'
    WHEN 6 THEN 'Haziran'
    WHEN 7 THEN 'Temmuz'
    WHEN 8 THEN 'Ağustos'
    WHEN 9 THEN 'Eylül'
    WHEN 10 THEN 'Ekim'
    WHEN 11 THEN 'Kasım'
    WHEN 12 THEN 'Aralık'
  END AS ay,
  SUM(tablo_insan.yarali_sayisi) AS toplam_yarali,
  SUM(tablo_insan.olu_sayisi) AS toplam_olu,
  SUM(tablo_insan.karisan_insan_sayisi) AS toplam_karisan
FROM tablo_kaza
INNER JOIN tablo_insan ON tablo_kaza.kaza_insan_id = tablo_insan.insan_id
GROUP BY MONTH(tablo_kaza.kaza_tarih);""")

# Fetch the results and create pandas dataframe
data = cursor.fetchall()
df = pd.DataFrame(data, columns=['ay', 'toplam_yarali', 'toplam_olu', 'toplam_karisan'])

# Create individual bar charts for each metric
plt.figure(figsize=(10, 6))
plt.bar(df['ay'], df['toplam_yarali'])
plt.xlabel("Ay")
plt.ylabel("Toplam Yaralı")
plt.title("Toplam Yaralı Sayısı (Aylara Göre)")
plt.show()

# Repeat for 'toplam_olu' and 'toplam_karisan'
plt.figure(figsize=(10, 6))
plt.bar(df['ay'], df['toplam_olu'])
plt.xlabel("Ay")
plt.ylabel("Toplam Ölü")
plt.title("Toplam Ölü Sayısı (Aylara Göre)")
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(df['ay'], df['toplam_karisan'])
plt.xlabel("Ay")
plt.ylabel("Toplam Karışan Kişi Sayısı")
plt.title("Toplam Karışan Kişi Sayısı (Aylara Göre)")
plt.show()

# Create a multi-bar chart to compare metrics
df.plot(x='ay', kind='bar', stacked=True)
plt.xlabel("Ay")
plt.ylabel("Toplam Sayı")
plt.title("Trafik Kazası İstatistikleri (Aylara Göre)")
plt.legend()
plt.show()

# Close the cursor and connection
cursor.close()
connection.close()
