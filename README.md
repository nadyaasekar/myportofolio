Nama : Nadya Sekar 

NPM : 2506607133

Kelas : PBP D


## REFLEKSI TUGAS INDIVIDUAL 1
1. ya, saya menggunakan elemen semantik HTML5 tersebut. Menggunakan elemen semantik membuat HTML lebih rapi sehingga setiap bagian halaman memiliki peran jelas serta dapat dengan mudah memahami hierarki halaman lebih baik
2. tantangan utama yang saya temukan saat mengatur CSS agar responsive adalah menyesuaikan tata letak seperti hero grid atau card grid agar tidak terasa sempit di layar kecil. saya mengevaluasinya dengan mengubah susunan elemen horizontal menjadi vertikal (stacking) pada tampilan mobile, serta menyesuaikan ukuran font dan padding agar konten lebih nyaman dibaca walaupun berpindah layar.
3. batasan utama dari static web murni adalah kontennya bersifat kaku, sehingga setiap ada perubahan data seperti skills atau experience harus diubah manual lewat kode HTML. pada iterasi selanjutnya, fungsionalitas dinamis yang paling ingin saya tambahkan adalah integrasi backend (seperti Django) untuk form kontak interaktif serta pengelolaan data portofolio secara dinamis dan rapi

## REFLEKSI TUGAS INDIVIDUAL 2
1. alur yang terjadi dimulai ketika browser pengguna mengirimkan permintaan HTTP ke server Django. permintaan tersebut diterima oleh urls.py tingkat proyek yang kemudian mengarahkannya ke urls.py di aplikasi main. berdasarkan named route yang cocok, fungsi view yang bersangkutan akan dipanggil untuk mengambil data objek dari database melalui model. view kemudian membungkus data ke dalam context dan memproses ke template HTML menggunakan **Django Template Language (DTL)** sebelum akhirnya dikembalikan sebagai respons ke browser pengguna.
2. data untuk bagian portofolio baru lebih baik disimpan pada model agar pengelolaannya bersifat dinamis dan terpusat di database, bukan ditulis langsung (hard-coded) di dalam template HTML. aplikasi menjadi jauh lebih mudah dipelihara dan dikembangkan karena penambahan, perubahan, maupun penghapusan data dapat dilakukan dengan mudah tanpa harus menyentuh atau merombak kode struktur HTML berulang kali.
3. perbedaan utamanya terletak pada tahap eksekusi: **'makemigrations'** berfungsi untuk membuat berkas script migrasi baru berdasarkan perubahan struktur pada file models.py, sedangkan migrate berfungsi untuk menerapkan perubahan tersebut secara nyata ke dalam database proyek. Contoh kasus yang mengharuskan keduanya adalah ketika kita menambahkan field baru pada model Experience (seperti menambahkan field kategori atau tanggal selesai), di mana kita harus menjalankan makemigrations untuk merekam perubahan rancangan tersebut, lalu menjalankan migrate agar tabel atau kolom baru benar-benar terbentuk di database.


## AI DISCLOSURE !!
Dalam pengerjaan Tugas 1 & 2 Pemrograman Berbasis Platform (PBP) ini, saya memanfaatkan Google Gemini sebagai thought partner dan kolaborator AI dengan rincian pemanfaatan sebagai berikut:

- Tools yang Digunakan: **Google Gemini** 
- Strategi Prompting: Menggunakan pendekatan iterative prompting dan contextual debugging—berdiskusi secara bertahap mulai dari perancangan model Experience, pengecekan kondisi kosong (empty state) pada Django Template Language (DTL), validasi named route dan navbar dengan tag {% url %}, hingga penyesuaian format pertanyaan reflektif.

**Bagian Spesifik yang Dibantu:**
- Membantu dalam perbaikan dan penyempurnaan kode HTML serta CSS untuk merapikan tampilan kartu experience agar konsisten dan responsif.
- Berdiskusi untuk memahami alur kerja MVT (Model-View-Template) Django secara mendalam guna menjawab pertanyaan reflektif pertama.
- Membantu memvalidasi cakupan unit test di tests.py agar memenuhi tiga kasus pengujian wajib (akses URL/template, kemunculan data model, dan penanganan kondisi kosong).
- Merumuskan struktur draf jawaban refleksi individu agar selaras dengan gaya bahasa pengerjaan tugas-tugas sebelumnya.

**Kontribusi Manusia:** 
Seluruh proses pengambilan keputusan (decision-making), perancangan struktur arsitektur aplikasi, implementasi kode aktual, integrasi komponen proyek, eksekusi perintah terminal (makemigrations, migrate, dan python manage.py test), pengujian fungsionalitas lokal di macOS, serta peninjauan dan penyesuaian akhir terhadap seluruh komponen tetap dikerjakan, diuji, dan diverifikasi secara mandiri.

**CHAT AI (contoh hanya beberapa)**

"(env) nadya@nadyas-MacBook-Air-10 myportofolio % git push origin main
error: src refspec main does not match any
error: failed to push some refs 
kenapa failed ya?"
"Error src refspec main does not match any ini muncul lagi karena ketika kita membuat virtual environment baru tadi (env), folder env yang.."


"boleh jelasin ga itu model tuh maksudnya apa ya?"
"Di arsitektur MVT (Model-View-Template) milik Django, Model adalah bagian yang bertugas mengelola data dan struktur database"


"cara liat submit shell yang kemarin kemarin bisa ga? mau liat data experience yang kemarin gitu"
"Bisa banget! Untuk melihat semua data Experience yang pernah kamu submit ke database via Django Shell, kamu punya 2 cara mudah:..."


"gimana cara button profile nya jadi kayak yg button gitu?"
"Teks link "Profile" dan "Experience" di navbar kamu masih menggunakan warna default link HTML (ungu/biru) dan belum menggunakan class tombol yang sama dengan SKILLS, EXPERIENCE, dan EDUCATION...."


