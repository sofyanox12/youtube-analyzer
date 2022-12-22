# Youtube Analyzer
Youtube Analyzer merupakan website sederhana yang menggunakan `Google API`sebagai perantara penerima statistik dari salah satu produk perusahaan `Google`, yaitu `Youtube.com` untuk setiap data channel yang telah teregistrasi dan valid.

</> Klasifikasi
-
Model yang digunakan didapatkan dari data yang sudah dibersihkan dan diproses menggunakan `pickle`. Sebelum membaca dataframe nya, terdapat library dasar yang digunakan sebagai berikut:
```
import numpy as np
import pandas as pd
```
Pengambilan dataframe dari `.csv` yang akan dipakai:
```
df = pd.read_csv('youtube.csv')
df
```
Membuang kolom yang tidak digunakan:
```
df.dropna(['Rank', 'Grade', 'Channel Name'], axis=1, inplace=true)
```
Mengubah nama kolom agar bersesuaian:
```
df.rename(columns={'Video Uploads': 'Videos', 'Subscribers': 'Subscribers', 'Video views' : 'Views'}, inplace=True)
```
Sebagai opsional, perlu dilihat nilai keunikan dari setiap kolom agar mudah di bersihkan:
```
df.nunique()
```
Mengkonversi dataframe kedalam bentuk numeric atau integer:
```
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)
```
Sebelum menganalisa, import library yang akan digunakan:
```
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split as split
```
Membatasi kriteria pembagian nilai:
```
df['Views'] = np.where(df['Views'] > 150000000, 1, 0)
df['Subscribers'] = np.where(df['Subscribers'] > 5000000, 1, 0)
df['Videos'] = np.where(df['Videos'] > 1000, 1, 0)
```
Membagi dataframe kedalam bentuk dataset yang akan di-latih dan di-test:
```
X_trainset, X_testset, y_trainset, y_testset = split(
    df[['Videos', 'Subscribers']], 
    df['Views'], 
    test_size=0.3, 
    random_state=3
)
```
Regresi kedalam bentuk pre-logistic secara `linear` menggunakan library yang telah di-import:
```
logistic_regression = LogisticRegression(solver='liblinear')
logistic_regression.fit(X_trainset, y_trainset)
```
Memprediksi nilai analisa:
```
y_predict = logistic_regression.predict(X_testset)
```
Meng-check akurasi dari model:
```
from sklearn.metrics import accuracy_score
accuracy_score(y_testset, y_predict)
```
Model tersebut akurat? langsung saja di simpan menggunakan `pickle`:
```
import pickle
pickle.dump(logistic_regression, open('model.pkl', 'wb'))
```
</> Cara Kerja
-
User memasukkan `url` dari sebuah channel kedalam input yang diminta sebagai variabel dasar untuk mencari apa `Channel ID` dari channel tersebut untuk digunakan dalam suntikan request `API`.
Data yang diterima dari request tersebut berupa sebuah halaman yang menampilkan data dalam bentuk `raw json`, untuk itu terjadilah `cleaning data` dengan menghapus string yang tidak diperlukan untuk membaca isi dari data mentah tersebut.
Hasil nya adalah beberapa variabel yang memberikan jumlah pelanggaan, total penonton dan hal-hal lain menyangkut channel yang dirujukan. Setelah itu, program akan mengkategorisasikan tingkat `kebagusan` channel sesuai model yang telah dibuat.

</> Pengkategorian
-
Kategori yang diberlakukan ada 2 macam saja, yaitu `good` dan `bad`. Keduanya didapat setelah menganalisa perbandingan jumlah pelanggan, like, hingga video yang diupload oleh `content creator` dari channel tersebut dalam upaya meningkatkan
tren channelnya.

Dibuat Oleh :

- [Muh. Sofyan Daud Pujas](https://www.github.com/sofyanox12)

