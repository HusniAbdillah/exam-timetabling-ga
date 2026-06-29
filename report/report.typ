#import "@preview/bamdone-ieeeconf:0.1.3": *

#show: ieee.with(
  title: [Optimasi Penjadwalan Ujian Universitas Menggunakan Algoritma Genetika],
  abstract: [
    Penyusunan jadwal ujian universitas merupakan permasalahan optimasi kombinatorial yang kompleks karena harus menempatkan banyak mata kuliah pada slot waktu terbatas sambil menghindari bentrokan ujian mahasiswa. Penelitian ini menyajikan implementasi #emph[Genetic Algorithm] (GA) untuk #emph[University Examination Timetabling Problem] (UETP) dengan representasi kromosom satu dimensi, #emph[tournament selection], #emph[one-point] dan #emph[uniform crossover], #emph[swap] dan #emph[move mutation], elitisme, serta varian Hybrid GA yang memanfaatkan solusi Greedy dan mekanisme #emph[repair] lokal. Kualitas solusi dihitung sebagai total penalti dari #emph[hard constraint] dan #emph[soft constraint], sehingga nilai yang lebih rendah menunjukkan jadwal yang lebih baik. Eksperimen pada #emph[dataset] simulasi berisi 2.340 mahasiswa, 150 mata kuliah, 6.220 relasi #emph[enrollment], 10 slot ujian, dan 10 ruang menunjukkan bahwa Hybrid GA menghasilkan penalti terbaik 1.114.518,5 pada eksperimen utama, lebih rendah daripada Pure GA 1.202.688,5 dan Greedy 1.221.557,5. Pada pengujian 30 kali, Hybrid GA juga memperoleh rata-rata penalti lebih rendah dan simpangan baku lebih kecil dibanding Pure GA. Hasil ini menunjukkan bahwa pendekatan evolusioner, terutama saat dikombinasikan dengan #emph[seed] Greedy dan #emph[repair] lokal, efektif untuk meningkatkan kualitas jadwal ujian dibanding #emph[baseline] deterministik.
  ],
  authors: (
    (
      given: "Husni",
      surname: "Abdillah",
      email: [ray25husni],
      affiliation: 1,
    ),
    (
      given: "Daffa Aulia Musyaffa",
      surname: "Subyantoro",
      email: [daffaaulia],
      affiliation: 1,
    ),
    (
      given: "Qois",
      surname: "Firosi",
      email: [qoisfirosi],
      affiliation: 1,
    ),
    (
      given: "Ghiffari Bravia",
      surname: "Hisham",
      email: [ghiffaribravia],
      affiliation: 1,
    ),
    (
      given: "Naufal Ghifari",
      surname: "Afdhala",
      email: [naufalghifari],
      affiliation: 1,
    ),
  ),
  affiliations: (
    (
      name: [Departemen Ilmu Komputer, Institut Pertanian Bogor],
      address: [Bogor, Jawa Barat, Indonesia],
      email-suffix: [apps.ipb.ac.id],
    ),
  ),
  index-terms: ("Genetic Algorithm", "Timetabling", "UETP", "Optimasi", "Hybrid GA"),
  bibliography: bibliography("refs.bib"),
  draft: false,
  paper-size: "us-letter",
)

= Pendahuluan <sec:pendahuluan>
== Latar Belakang
Penyusunan jadwal ujian perguruan tinggi merupakan aktivitas akademik rutin yang memiliki tingkat kompleksitas tinggi. Setiap mata kuliah harus ditempatkan pada slot waktu tertentu, sementara mahasiswa dapat mengambil beberapa mata kuliah lintas semester, lintas program studi, atau mata kuliah umum universitas. Jika dua mata kuliah yang diambil mahasiswa yang sama dijadwalkan pada waktu yang sama, maka jadwal tersebut menghasilkan konflik yang tidak dapat diterima.

Masalah ini termasuk keluarga #emph[University Examination Timetabling Problem] (UETP), yaitu masalah optimasi kombinatorial yang sulit diselesaikan secara eksak pada skala besar karena banyaknya kombinasi waktu, ruang, peserta, dan preferensi institusi @chen2021 @bashab2023 @abdipoor2023. Pendekatan manual biasanya bergantung pada pengalaman operator akademik dan sulit mengevaluasi seluruh kombinasi jadwal secara sistematis. Oleh karena itu, metode metaheuristik seperti #emph[Genetic Algorithm] (GA) menjadi relevan karena mampu mengeksplorasi ruang solusi yang besar melalui proses evolusi populasi dan dapat dikombinasikan dengan perbaikan lokal @son2021 @aslan2023 @fuladi2024.

Pada proyek ini, GA digunakan untuk membangun sistem penjadwalan ujian otomatis berbasis #emph[dataset] CSV. Sistem tidak hanya mengevaluasi konflik mahasiswa, tetapi juga mempertimbangkan batasan jumlah ujian per hari, kapasitas ruang, blokir slot fakultas, penyebaran ujian, serta preferensi jarak antarujian. Hasil GA kemudian dibandingkan dengan algoritma Greedy sebagai #emph[baseline].

== Rumusan Masalah
Rumusan masalah penelitian ini adalah sebagai berikut:
1. Bagaimana memodelkan solusi penjadwalan ujian universitas agar dapat diproses oleh #emph[Genetic Algorithm]?
2. Bagaimana merancang fungsi #emph[fitness] yang menggabungkan #emph[hard constraint] dan #emph[soft constraint] secara terukur?
3. Seberapa efektif Pure GA dan Hybrid GA dibandingkan #emph[baseline] Greedy dalam menurunkan total penalti jadwal?
4. Bagaimana pengaruh parameter populasi dan mutasi terhadap konvergensi kualitas solusi?

== Tujuan
Tujuan penelitian dan pengembangan sistem ini adalah:
1. Mengimplementasikan sistem penjadwalan ujian otomatis berbasis #emph[Genetic Algorithm].
2. Meminimalkan konflik jadwal ujian mahasiswa dan pelanggaran batasan tambahan.
3. Membandingkan performa Pure GA, Hybrid GA, dan #emph[baseline] Greedy.
4. Menyediakan artefak hasil berupa jadwal ujian, riwayat #emph[fitness], statistik evaluasi, dan visualisasi eksperimen.

== Manfaat
Sistem yang dikembangkan dapat membantu proses administrasi akademik dalam menghasilkan jadwal ujian yang lebih konsisten dan mudah dievaluasi. Dari sisi akademik, proyek ini juga menjadi studi kasus penerapan metaheuristik untuk masalah optimasi kombinatorial, lengkap dengan representasi solusi, operator evolusioner, fungsi #emph[fitness], #emph[baseline], serta analisis hasil eksperimen.

= Tinjauan Pustaka <sec:tinjauan-pustaka>
== University Examination Timetabling Problem (UETP)
#emph[University Examination Timetabling Problem] adalah masalah penempatan ujian ke sejumlah periode waktu dan sumber daya tertentu dengan tujuan memenuhi batasan wajib dan mengoptimalkan preferensi kualitas jadwal. Dalam konteks universitas, batasan utama biasanya berupa larangan mahasiswa mengikuti dua ujian pada waktu yang sama. Selain itu, institusi dapat memiliki batasan kapasitas ruang, ketersediaan waktu tertentu, serta preferensi agar beban ujian mahasiswa tersebar dengan baik.

UETP bersifat NP-Hard karena jumlah kemungkinan kombinasi penempatan ujian meningkat sangat cepat seiring bertambahnya jumlah mata kuliah dan slot waktu. Jika terdapat $N$ mata kuliah dan $T$ slot waktu, maka ruang solusi kasar dapat mencapai $T^N$. Dengan 150 mata kuliah dan 10 slot, ruang solusi teoritisnya adalah $10^150$, jauh melampaui kemampuan enumerasi penuh. Bahkan pada #emph[benchmark] UETP yang lebih terstandar, pembuktian optimalitas dapat membutuhkan dekomposisi dan kombinasi pendekatan MIP serta #emph[heuristic] khusus @dimitsas2025.

== Algoritma Genetika
#emph[Genetic Algorithm] adalah metode pencarian berbasis populasi yang meniru mekanisme seleksi alam. Setiap kandidat solusi direpresentasikan sebagai kromosom. Populasi solusi dievaluasi menggunakan fungsi #emph[fitness], kemudian individu yang lebih baik memiliki peluang lebih besar untuk mewariskan informasi genetiknya melalui operator seleksi, #emph[crossover], dan mutasi. Pada #emph[examination timetabling], GA banyak digunakan karena mudah dipadukan dengan representasi slot, objektif penalti, dan strategi #emph[multi-objective] atau #emph[local search] @son2021 @aslan2023 @hafsa2025.

Pada masalah minimisasi seperti penjadwalan ujian, #emph[fitness] dimaknai sebagai total penalti. Semakin kecil penalti, semakin baik kualitas jadwal. Siklus GA yang digunakan pada sistem ini terdiri atas inisialisasi populasi, evaluasi #emph[fitness], elitisme, pemilihan induk menggunakan #emph[tournament selection], #emph[crossover], mutasi, #emph[optional repair] pada Hybrid GA, dan pembentukan generasi baru sampai batas generasi tercapai.

== Representasi Kromosom
Representasi kromosom menentukan bagaimana suatu solusi potensial dimodelkan secara digital agar dapat dimanipulasi oleh operator genetika. Pada sistem ini, kromosom direpresentasikan sebagai sebuah larik satu dimensi (#emph[1D array] atau #raw("list[int]") pada Python).

Setiap elemen dalam larik tersebut memenuhi ketentuan sebagai berikut:
1. *Indeks larik* mewakili identitas mata kuliah. Urutan indeks dipetakan secara konsisten berdasarkan urutan data courses.csv.
2. *Nilai gen* pada indeks mewakili ID slot waktu yang dialokasikan untuk mata kuliah tersebut. Nilai berupa bilangan bulat dalam rentang $[1, T]$, dengan $T$ sebagai jumlah slot waktu.

Keunggulan representasi ini adalah efisiensi memori dan kesederhanaan operator. Dibandingkan matriks mata kuliah terhadap slot waktu, representasi satu dimensi menghindari struktur #emph[sparse] dan memudahkan #emph[crossover] serta mutasi langsung pada tingkat gen. Pendekatan ini juga memastikan setiap mata kuliah selalu memiliki tepat satu slot ujian.

== Batasan pada Penjadwalan
#emph[Constraint] dalam sistem dibagi menjadi #emph[hard constraint] dan #emph[soft constraint]. #emph[Hard constraint] diberi bobot penalti besar karena pelanggarannya berdampak langsung terhadap kelayakan jadwal. #emph[Soft constraint] diberi bobot lebih kecil karena berfungsi meningkatkan kenyamanan dan kualitas distribusi jadwal.

#emph[Hard constraint] utama adalah konflik ujian mahasiswa, yaitu ketika seorang mahasiswa memiliki dua atau lebih ujian pada slot yang sama. Batasan tambahan yang juga dipenalti tinggi meliputi jumlah ujian maksimum per hari, kapasitas ruang ujian, dan blokir slot fakultas. #emph[Soft constraint] meliputi ujian berturut-turut, terlalu banyak ujian dalam satu hari, ketidakseimbangan penyebaran slot, kedekatan mata kuliah inti semester yang sama, kedekatan mata kuliah berpeserta besar, #emph[preferred gap], dan penalti ujian Jumat sore. Pemisahan #emph[hard] dan #emph[soft constraint] seperti ini umum pada literatur #emph[timetabling] karena kelayakan jadwal dan kualitas preferensi sering perlu dievaluasi secara bersamaan @algethami2021 @arratia2021 @mokhtari2021 @rappos2022.

== Studi Literatur
Penelitian penjadwalan akademik mutakhir menempatkan #emph[timetabling] sebagai masalah optimasi kombinatorial yang bergantung kuat pada konteks institusi. Survei Chen et al. dan Bashab et al. menunjukkan bahwa variasi #emph[constraint], #emph[dataset], dan tujuan optimasi membuat satu metode sulit berlaku universal untuk semua kampus @chen2021 @bashab2023. Abdipoor et al. juga menekankan bahwa metaheuristik dan #emph[hybrid metaheuristic] menjadi pilihan dominan karena dapat menyeimbangkan eksplorasi ruang solusi dan pemenuhan #emph[constraint] praktis @abdipoor2023.

Pendekatan eksak tetap penting sebagai pembanding dan sebagai cara memodelkan #emph[constraint] secara formal. #emph[Mixed-integer programming] dan #emph[integer linear programming] telah digunakan untuk #emph[course timetabling], penugasan dosen, dan #emph[examination timetabling] dengan #emph[constraint] realistis seperti kapasitas ruang, preferensi pengajar, pemilihan hari, dan penggunaan ruang @algethami2021 @arratia2021 @mokhtari2021 @rappos2022 @laisupannawong2024. Namun, studi tersebut juga memperlihatkan bahwa model eksak cenderung membutuhkan reduksi masalah, #emph[solver] khusus, atau batas waktu komputasi ketika skala dan kompleksitas #emph[instance] meningkat.

Pada sisi #emph[heuristic] dan #emph[metaheuristic], #emph[local search], #emph[hyper-heuristic], dan algoritma populasi banyak dipakai untuk memperbaiki solusi secara iteratif. Bykov dan Petrovic menunjukkan efektivitas #emph[Step Counting Hill Climbing] pada UETP, sedangkan Kheiri dan Keedwell serta Muklason et al. menunjukkan bahwa pemilihan #emph[heuristic] dan operator #emph[neighborhood] dapat berdampak besar pada performa pencarian @bykov2016 @kheiri2016 @muklason2024. Studi Nand et al. dan Siew et al. memperkuat temuan ini pada #emph[dataset examination timetabling] modern dengan #emph[Firefly Algorithm], #emph[Whale Optimization Algorithm], dan komponen #emph[local search] @nand2024 @siew2025.

#emph[Genetic Algorithm] tetap relevan karena fleksibel dalam merepresentasikan kandidat solusi dan mudah dikombinasikan dengan #emph[local search] atau #emph[repair]. Son et al. menggunakan GA untuk #emph[examination timetabling] #emph[multi-objective], Aslan menunjukkan bahwa #emph[hybrid] GA dengan #emph[local search] kompetitif pada UETP, dan Hafsa et al. menerapkan #emph[evolutionary algorithms] pada #emph[timetabling] profesional #emph[multi-objective] @son2021 @aslan2023 @hafsa2025. Selain domain pendidikan, Fuladi dan Kim serta Al-Mudahka dan Alhamad memperlihatkan bahwa #emph[scheduling]/#emph[timetabling] berbasis optimasi juga digunakan pada konteks produksi dinamis dan kesehatan, sehingga desain fungsi penalti dan mekanisme perbaikan lokal menjadi prinsip yang dapat ditransfer lintas domain @fuladi2024 @almudahka2022. Dalam perkembangan terbaru, Kallestad et al. menunjukkan arah #emph[hyperheuristic] berbasis #emph[deep reinforcement learning] untuk memilih operator pada masalah optimasi kombinatorial, yang relevan sebagai pengembangan lanjutan dari mekanisme #emph[repair] atau #emph[adaptive operator selection] @kallestad2023.

= Metodologi <sec:metodologi>
== Data dan Pemodelan Universitas
Data yang digunakan merupakan #emph[dataset] simulasi universitas multijurusan. Data disimpan dalam format CSV agar mudah dibaca, diuji, dan diregenerasi. Struktur utama #emph[dataset] terdiri atas mahasiswa, mata kuliah, #emph[enrollment], slot ujian, ruang, dan slot blokir fakultas.

#figure(
  table(
    stroke: none,
    columns: (auto, auto, auto),
    align: (left, right, left),
    inset: 5pt,
    table.hline(),
    table.header([*Berkas*], [*Jumlah Data*], [*Keterangan*]),
    table.hline(),
    [#raw("students.csv")], [2.340], [Mahasiswa beserta fakultas, departemen, dan semester],
    [#raw("courses.csv")], [150], [Mata kuliah umum, fakultas, dan departemen],
    [#raw("enrollment.csv")], [6.220], [Relasi mahasiswa terhadap mata kuliah],
    [#raw("timeslots.csv")], [10], [Slot ujian berdasarkan hari dan sesi],
    [#raw("rooms.csv")], [10], [Ruang ujian dan kapasitas],
    [#raw("slot_blocks.csv")], [6], [Larangan slot tertentu untuk fakultas],
    table.hline(),
  ),
  caption: [Ringkasan data yang digunakan dalam eksperimen],
)<tab:dataset>

Relasi #emph[enrollment] menjadi sumber utama pembentukan konflik. Dua mata kuliah dianggap berkonflik jika terdapat minimal satu mahasiswa yang mengambil keduanya. Dengan demikian, kualitas jadwal tidak hanya bergantung pada jumlah mata kuliah, tetapi juga pada kepadatan hubungan antar mata kuliah dalam data #emph[enrollment].

== Prapemrosesan Data
Tahap prapemrosesan dimulai dari pembacaan CSV menjadi objek domain seperti #raw("Student"), #raw("Course"), #raw("Enrollment"), dan #raw("Timeslot"). Setelah itu, validator memastikan kolom wajib tersedia dan nilai numerik seperti semester, slot, hari, sesi, serta kapasitas dapat diproses.

Matriks konflik dibangun dengan mengelompokkan #emph[enrollment] berdasarkan mahasiswa. Untuk setiap mahasiswa, semua pasangan mata kuliah yang diambil mahasiswa tersebut ditambahkan sebagai #emph[edge] konflik. Hasil akhirnya berupa #emph[adjacency list], sehingga setiap mata kuliah memiliki daftar mata kuliah lain yang tidak ideal dijadwalkan pada slot yang sama.

== Representasi Solusi
Sebagai perwujudan konkret dari rancangan kromosom, representasi solusi dalam kode diimplementasikan secara langsung untuk memetakan penugasan slot ujian.

Misalkan terdapat 5 mata kuliah dengan penugasan slot waktu berikut:
#align(center)[
  [3, 5, 2, 1, 7]
]

Secara struktural, kromosom tersebut diartikan sebagai pemetaan mata kuliah ke slot waktu seperti pada @tab:representasi-solusi.

#figure(
  table(
    stroke: none,
    columns: (auto, auto),
    align: (center, center),
    inset: 8pt,
    table.hline(),
    table.header([*Mata Kuliah*], [*Slot Waktu*]),
    table.hline(),
    [Kalkulus], [3],
    [Pancasila], [5],
    [Basis Data], [2],
    [Struktur Data], [1],
    [Kecerdasan Buatan], [7],
    table.hline(),
  ),
  caption: [Contoh pemetaan representasi solusi],
)<tab:representasi-solusi>

Melalui pemetaan linier ini, indeks $i$ dari larik merujuk pada elemen ke-$i$ di dalam daftar mata kuliah terurut, dan nilai $"chromosome"_i$ menentukan waktu pelaksanaan ujiannya. Representasi ini menjamin bahwa setiap mata kuliah pasti mendapatkan tepat satu slot waktu.

== Inisialisasi Populasi
Proses pencarian solusi optimal diawali dengan pembentukan populasi awal yang terdiri atas sejumlah individu acak. Hal ini bertujuan memberikan titik awal pencarian yang tersebar di ruang solusi, meminimalkan risiko konvergensi dini, dan mempertahankan diversitas genetik.

Pada #raw("population.py"), fungsi #raw("initialize_population") menerima jumlah mata kuliah ($N$), jumlah slot waktu ($T$), ukuran populasi ($P$), dan #emph[seed] opsional. Fungsi ini menghasilkan $P$ individu, dengan setiap gen dipilih secara acak dari rentang slot valid:

$ "chromosome" = [R_1, R_2, ..., R_N] $
$ R_i ~ "Uniform"(1, T) $

Pada Hybrid GA, populasi dapat diberi #emph[seed] dari solusi Greedy. #emph[Seed] ini menjadi titik awal yang sudah relatif layak, sementara individu acak tetap disertakan untuk menjaga eksplorasi.

== Operator Algoritma Genetika
Operator genetika memproses generasi saat ini untuk menghasilkan generasi baru yang diharapkan memiliki kualitas solusi lebih baik. Implementasi operator diletakkan secara modular pada direktori #raw("src/ga/").

#strong[Seleksi.] Sistem menggunakan #emph[Tournament Selection] melalui fungsi #raw("tournament_selection"). Sebanyak #raw("tournament_size") individu dipilih secara acak dari populasi, kemudian individu dengan penalti terkecil menjadi pemenang turnamen dan digunakan sebagai induk. Nilai #raw("tournament_size") mengatur tekanan seleksi: semakin besar nilainya, semakin kuat preferensi terhadap individu terbaik, tetapi diversitas populasi dapat menurun lebih cepat.

#strong[Crossover.] Operator #emph[crossover] menggabungkan dua induk untuk menghasilkan dua anak. Sistem menggunakan #emph[one-point crossover], yaitu memilih satu titik potong lalu menukar segmen kromosom setelah titik tersebut, dan #emph[uniform crossover], yaitu mengevaluasi setiap posisi gen dan menukar gen antarinduk berdasarkan peluang #raw("swap_prob"). Pada #raw("engine.py"), tipe #emph[crossover] dipilih secara acak dengan peluang seimbang setelah pasangan induk lolos probabilitas #raw("crossover_rate").

#strong[Mutasi.] Mutasi mengenalkan variasi genetik baru agar pencarian tidak mudah terjebak pada optimum lokal. Sistem menggunakan #emph[swap mutation], yaitu menukar dua gen secara acak, dan #emph[move mutation], yaitu mengganti nilai gen dengan slot baru berdasarkan probabilitas #raw("mutation_rate"). #emph[Move mutation] penting pada UETP karena satu perubahan slot dapat langsung mengurangi konflik besar pada mata kuliah tertentu.

#strong[Elitisme dan repair.] Elitisme mempertahankan sejumlah #raw("elite_count") individu terbaik secara utuh ke generasi berikutnya. Hybrid GA menambahkan #emph[repair] lokal ketika #raw("enable_repair") aktif. #emph[Repair] dijalankan secara probabilistik pada anak hasil evolusi untuk mengevaluasi alternatif slot yang menurunkan penalti.

== Pemodelan Batasan
Fungsi objektif sistem adalah minimisasi total penalti. Nilai #emph[fitness] dihitung sebagai penjumlahan berbobot dari pelanggaran #emph[constraint]:

#align(center)[
  $
    P &= 1000H + 10C + 5D + 30S \
      &+ 3M + 2E + G + 5F \
      &+ 200X + 300R + 250B
  $
]

dengan $P$ adalah total penalti. Definisi simbol ditunjukkan pada @tab:constraint-weight.

#figure(
  table(
    stroke: none,
    columns: (auto, auto, auto),
    align: (center, right, left),
    inset: 3.5pt,
    table.hline(),
    table.header([*Simbol*], [*Bobot*], [*Komponen*]),
    table.hline(),
    [$H$], [1000], [Konflik mahasiswa],
    [$C$], [10], [Ujian berturut-turut],
    [$D$], [5], [Terlalu banyak ujian harian],
    [$S$], [30], [Ketimpangan distribusi slot],
    [$M$], [3], [Mata kuliah inti terlalu dekat],
    [$E$], [2], [Mata kuliah berpeserta besar],
    [$G$], [1], [Preferred gap],
    [$F$], [5], [Jumat sesi 3],
    [$X$], [200], [Maksimum ujian per hari],
    [$R$], [300], [Kapasitas ruang],
    [$B$], [250], [Slot blokir fakultas],
    table.hline(),
  ),
  caption: [Simbol dan bobot batasan dalam fungsi #emph[fitness]],
)<tab:constraint-weight>

== Fungsi Fitness
Fungsi #emph[fitness] berada pada #raw("src/fitness/fitness.py") dan mengembalikan total penalti bertipe #raw("float"). Semakin kecil nilai #emph[fitness], semakin baik solusi. Komponen #emph[hard constraint] dihitung dari daftar mata kuliah setiap mahasiswa dengan menghitung pasangan ujian yang berada pada slot sama. Komponen #emph[soft constraint] dihitung dengan memetakan slot menjadi pasangan hari-sesi sehingga sistem dapat mengevaluasi beban ujian per hari, kedekatan sesi, dan distribusi ujian.

Fungsi #emph[fitness] juga menggunakan #emph[cache] data global untuk mempercepat evaluasi berulang. Hal ini penting karena GA mengevaluasi banyak kromosom pada setiap generasi. Dengan parameter populasi 50 dan 50 generasi, sedikitnya terdapat ribuan evaluasi #emph[fitness] dalam satu eksperimen.

== Algoritma Greedy Baseline
#emph[Baseline] Greedy digunakan sebagai pembanding deterministik. Algoritma ini mengurutkan mata kuliah berdasarkan derajat konflik, yaitu jumlah mata kuliah lain yang berbenturan dengannya. Mata kuliah dengan konflik terbanyak dijadwalkan lebih awal. Untuk setiap mata kuliah, Greedy mencoba semua slot yang tersedia dan memilih slot yang menghasilkan penalti terkecil pada kondisi saat itu.

Pendekatan ini cepat dan mudah dipahami, tetapi memiliki kelemahan utama: keputusan awal tidak direvisi secara global. Jika suatu mata kuliah sudah ditempatkan pada slot tertentu, keputusan tersebut dapat membatasi pilihan mata kuliah berikutnya. GA mengatasi kelemahan ini dengan mempertahankan banyak kandidat solusi dan memperbaikinya lintas generasi.

== Arsitektur Sistem
Arsitektur sistem dirancang modular agar prapemrosesan, GA, #emph[fitness], evaluasi, dan visualisasi dapat diuji secara terpisah. Alur data utama ditunjukkan pada @fig:architecture-flow.

#figure(
  align(center)[
    #set text(size: 7.5pt)
    #grid(
      columns: (1fr,),
      row-gutter: 2.5pt,
      box(width: 72%, inset: 4pt, stroke: 0.5pt, radius: 1pt)[Data CSV],
      [↓],
      box(width: 72%, inset: 4pt, stroke: 0.5pt, radius: 1pt)[Prapemrosesan dan Validasi],
      [↓],
      box(width: 72%, inset: 4pt, stroke: 0.5pt, radius: 1pt)[Matriks Konflik],
      [↓],
      box(width: 72%, inset: 4pt, stroke: 0.5pt, radius: 1pt)[Mesin GA / Greedy],
      [↓],
      box(width: 72%, inset: 4pt, stroke: 0.5pt, radius: 1pt)[Evaluasi Fitness],
      [↓],
      box(width: 72%, inset: 4pt, stroke: 0.5pt, radius: 1pt)[Jadwal, Statistik, Visualisasi],
    )
  ],
  caption: [Flowchart arsitektur sistem penjadwalan ujian],
)<fig:architecture-flow>

Modul prapemrosesan bertanggung jawab membaca dan memvalidasi data. Modul #raw("ga") menjalankan proses evolusi. Modul #raw("fitness") menghitung penalti. Modul #raw("evaluation") menyediakan #emph[baseline] Greedy dan #emph[benchmark]. Modul #raw("visualization") menghasilkan tabel jadwal serta grafik performa.

= Hasil dan Pembahasan <sec:hasil-pembahasan>
== Spesifikasi Eksperimen
Eksperimen utama menggunakan konfigurasi GA pada @tab:experiment-config. Selain eksperimen utama, dilakukan analisis sensitivitas terhadap ukuran populasi dan #raw("mutation_rate"), pengujian statistik 30 #emph[run], serta profil waktu eksekusi.

#figure(
  table(
    stroke: none,
    columns: (auto, auto),
    align: (left, center),
    inset: 6pt,
    table.hline(),
    table.header([*Parameter*], [*Nilai*]),
    table.hline(),
    [Jumlah mata kuliah], [150],
    [Jumlah slot ujian], [10],
    [Ukuran populasi], [50],
    [Generasi maksimum], [50],
    [Laju #emph[crossover]], [0,8],
    [Laju mutasi], [0,1],
    [Ukuran turnamen], [5],
    [Jumlah elit], [2],
    [Probabilitas #emph[repair] Hybrid GA], [0,20],
    table.hline(),
  ),
  caption: [Konfigurasi utama eksperimen],
)<tab:experiment-config>

== Hasil Algoritma Genetika
Hasil utama pada #raw("outputs/statistics.json") menunjukkan bahwa Hybrid GA memperoleh total penalti terendah. Pure GA masih lebih baik daripada Greedy, tetapi perbaikannya lebih kecil dibanding Hybrid GA. Ringkasan hasil ditunjukkan pada @tab:main-result.

#figure(
  table(
    stroke: none,
    columns: (auto, auto, auto, auto, auto, auto),
    align: (left, right, right, right, right, right),
    inset: 4pt,
    table.hline(),
    table.header([*Metode*], [*Waktu (s)*], [*Penalti*], [*Konflik*], [*Ujian Harian*], [*Sebaran*]),
    table.hline(),
    [Greedy], [14,265], [1.221.557,5], [1.216], [25], [4,25],
    [Pure GA], [21,578], [1.202.688,5], [1.198], [18], [22,25],
    [Hybrid GA], [19,078], [1.114.518,5], [1.114], [0], [7,25],
    table.hline(),
  ),
  caption: [Perbandingan hasil eksperimen utama],
)<tab:main-result>

Dibanding Greedy, Pure GA menurunkan #emph[fitness] sebesar 18.869 poin atau sekitar 1,54%. Hybrid GA menurunkan #emph[fitness] sebesar 107.039 poin atau sekitar 8,77%. Hybrid GA juga menghilangkan pelanggaran terlalu banyak ujian harian pada hasil utama, sedangkan Greedy masih memiliki 25 pelanggaran dan Pure GA 18 pelanggaran.

== Visualisasi Konvergensi
Riwayat #emph[fitness] pada #raw("outputs/fitness_history.csv") menunjukkan penurunan penalti sepanjang generasi. Pure GA dimulai dari 2.159.201,5 pada generasi 0 dan mencapai 1.202.688,5 pada generasi akhir. Hybrid GA dimulai dari 1.221.557,5 karena menggunakan #emph[seed] Greedy, lalu turun ke 1.114.518,5.

#figure(
  image("assets/sensitivity_pure_ga.png", width: 100%),
  caption: [Konvergensi sensitivitas parameter pada Pure GA],
)<fig:sensitivity-pure>

#figure(
  image("assets/sensitivity_hybrid_ga.png", width: 100%),
  caption: [Konvergensi sensitivitas parameter pada Hybrid GA],
)<fig:sensitivity-hybrid>

Pada @fig:sensitivity-pure dan @fig:sensitivity-hybrid, Pure GA tampak lebih bergantung pada populasi dan #raw("mutation_rate"). Populasi 100 dengan #raw("mutation_rate") 0,05 menghasilkan #emph[fitness] terbaik pada analisis sensitivitas, sedangkan #raw("mutation_rate") 0,2 cenderung lebih buruk karena perubahan gen terlalu agresif. Hybrid GA memiliki nilai awal jauh lebih rendah karena #emph[seed] Greedy dan menghasilkan kurva yang lebih stabil.

== Visualisasi Jadwal
Jadwal terbaik diekspor ke #raw("outputs/schedule.csv") dan berisi 150 mata kuliah. Setiap baris memuat kode mata kuliah, nama mata kuliah, slot, hari, dan sesi. Contoh sebagian jadwal ditampilkan pada @tab:schedule-sample.

#figure(
  table(
    stroke: none,
    columns: (auto, auto, auto, auto, auto),
    align: (left, left, center, center, center),
    inset: 4pt,
    table.hline(),
    table.header([*Kode*], [*Mata Kuliah*], [*Slot*], [*Hari*], [*Sesi*]),
    table.hline(),
    [GEN101], [Pancasila], [4], [4], [1],
    [GEN102], [Pendidikan Agama], [2], [2], [1],
    [GEN103], [Bahasa Indonesia], [4], [4], [1],
    [GEN104], [Bahasa Inggris], [3], [3], [1],
    [GEN105], [Kewirausahaan], [1], [1], [1],
    [KOM201], [Pemrograman Dasar], [3], [3], [1],
    [KOM401], [Struktur Data], [4], [4], [1],
    [KOM603], [Kecerdasan Buatan], [1], [1], [1],
    table.hline(),
  ),
  caption: [Contoh keluaran jadwal ujian terbaik],
)<tab:schedule-sample>

Selain keluaran CSV, sistem menyediakan antarmuka Streamlit untuk menjalankan optimasi, mengatur parameter GA, memfilter jadwal, serta mengunduh hasil. Tampilan halaman utama aplikasi ditunjukkan pada @fig:streamlit-dashboard.

#figure(
  image("assets/streamlit_dashboard.png", width: 100%),
  caption: [Tampilan dashboard Streamlit untuk jadwal ujian],
)<fig:streamlit-dashboard>

== Perbandingan dengan Greedy
Greedy memiliki keunggulan pada kesederhanaan dan determinisme. Pada eksperimen utama, waktu Greedy adalah 14,265 detik, lebih cepat daripada Pure GA. Namun, kualitas jadwal Greedy lebih rendah karena total penalti dan pelanggaran #emph[hard constraint] lebih tinggi.

Perbandingan dengan Greedy juga bergantung pada jumlah generasi yang diberikan kepada GA. Pada profil kompleksitas waktu, Greedy menghasilkan solusi tetap karena tidak memiliki parameter generasi, sedangkan kualitas GA berubah seiring bertambahnya generasi. Pure GA membutuhkan generasi lebih banyak untuk keluar dari populasi awal yang buruk. Sebaliknya, Hybrid GA dapat melampaui Greedy lebih cepat karena menggunakan #emph[seed] Greedy dan #emph[repair] lokal, tetapi biaya waktunya meningkat ketika jumlah generasi diperbesar.

Pengujian statistik 30 kali pada #raw("outputs/statistical_significance.json") memperlihatkan pola yang lebih kuat. #emph[Baseline] Greedy memiliki #emph[fitness] 1.218.831,5. Pure GA memiliki rata-rata #emph[fitness] 1.126.067,87 dengan simpangan baku 39.893,37, sedangkan Hybrid GA memiliki rata-rata #emph[fitness] 1.088.218,17 dengan simpangan baku 17.692,77. Artinya, Hybrid GA tidak hanya menghasilkan rata-rata penalti yang lebih rendah, tetapi juga lebih stabil antar-#emph[run].

#figure(
  table(
    stroke: none,
    columns: (auto, auto, auto, auto, auto),
    align: (left, right, right, right, right),
    inset: 5pt,
    table.hline(),
    table.header([*Metode*], [*Terbaik*], [*Terburuk*], [*Rata-rata*], [*Simp. Baku*]),
    table.hline(),
    [Pure GA], [1.048.819,5], [1.203.468,5], [1.126.067,87], [39.893,37],
    [Hybrid GA], [1.062.901,5], [1.122.514,5], [1.088.218,17], [17.692,77],
    table.hline(),
  ),
  caption: [Ringkasan pengujian statistik 30 #emph[run]],
)<tab:stat-result>

== Analisis Hasil
Hasil eksperimen memperlihatkan tiga temuan utama. Pertama, representasi kromosom satu dimensi cukup efektif karena semua operator dapat bekerja langsung pada slot mata kuliah tanpa perlu memperbaiki struktur solusi yang tidak valid. Setiap individu selalu merepresentasikan jadwal lengkap.

Kedua, Pure GA mampu memperbaiki solusi melalui eksplorasi populasi, tetapi membutuhkan generasi yang cukup untuk mendekati kualitas Greedy. Hal ini terlihat pada riwayat #emph[fitness] yang turun bertahap dari nilai awal yang tinggi. Ketika ruang solusi sangat besar, populasi acak awal sering memiliki konflik tinggi.

Ketiga, Hybrid GA memberikan #emph[trade-off] terbaik pada eksperimen ini. #emph[Seed] Greedy menyediakan solusi awal yang sudah cukup baik, sedangkan operator GA dan #emph[repair] lokal memperbaiki kelemahan keputusan Greedy yang terlalu lokal. Waktu eksekusi Hybrid GA memang dapat meningkat pada profil generasi yang lebih panjang, tetapi peningkatan kualitas dan stabilitas solusi membuatnya lebih sesuai untuk skenario penjadwalan akademik yang tidak harus dilakukan secara #emph[real-time].

#figure(
  image("assets/time_complexity_profile.png", width: 100%),
  caption: [Profil waktu eksekusi terhadap jumlah generasi],
)<fig:time-profile>

= Kesimpulan dan Saran <sec:kesimpulan-saran>
== Kesimpulan
Berdasarkan implementasi dan eksperimen, dapat disimpulkan bahwa:
1. Masalah penjadwalan ujian dapat dimodelkan secara efektif menggunakan kromosom satu dimensi yang memetakan mata kuliah ke slot ujian.
2. Fungsi #emph[fitness] berbasis penalti berbobot mampu menggabungkan konflik mahasiswa, kapasitas ruang, slot blokir, dan #emph[soft constraint] kualitas jadwal.
3. Pure GA berhasil menurunkan penalti dibanding Greedy pada eksperimen utama, dari 1.221.557,5 menjadi 1.202.688,5.
4. Hybrid GA memberikan hasil terbaik dengan penalti 1.114.518,5 pada eksperimen utama dan rata-rata 1.088.218,17 pada 30 #emph[run], lebih rendah serta lebih stabil daripada Pure GA.
5. #emph[Seed] Greedy dan #emph[repair] lokal terbukti membantu GA memulai dari solusi yang lebih baik serta mengurangi risiko pencarian terlalu lama pada area solusi buruk.

== Saran
Pengembangan berikutnya dapat diarahkan pada beberapa aspek. Pertama, sistem dapat menggunakan #emph[adaptive mutation] agar laju mutasi berubah berdasarkan stagnasi #emph[fitness]. Kedua, #emph[repair] lokal dapat dibuat lebih selektif dengan memprioritaskan mata kuliah penyebab konflik terbesar. Ketiga, #emph[dataset] riil dari sistem akademik dapat digunakan untuk menguji ketahanan model terhadap distribusi #emph[enrollment] yang lebih kompleks. Keempat, optimasi dapat diperluas ke #emph[multi-objective optimization] agar konflik, kenyamanan mahasiswa, pemakaian ruang, dan preferensi institusi dapat dianalisis sebagai objektif terpisah.
