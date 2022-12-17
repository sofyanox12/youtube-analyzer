# Youtube Analyzer
Youtube Analyzer merupakan website sederhana yang menggunakan `Google API`sebagai perantara penerima statistik dari salah satu produk perusahaan `Google`, yaitu `Youtube.com` untuk setiap data channel yang telah teregistrasi dan valid.

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

