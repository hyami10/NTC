# NTC - Website Pembelajaran C++
## Deskripsi Umum
NTC adalah website pembelajaran bahasa pemrograman C++ yang dirancang untuk membantu pengguna mempelajari C++ dengan pendekatan terstruktur. Website ini akan menggunakan tema warna biru putih pastel untuk memberikan pengalaman visual yang nyaman bagi pengguna.

## Fitur Utama

### 1. Learning Path
- **Deskripsi**: Jalur pembelajaran terstruktur untuk mempelajari C++ dari dasar hingga tingkat lanjut
- **Komponen**:
  - Materi pembelajaran bertahap (beginner, intermediate, advanced)
  - Tutorial dan contoh kode untuk setiap topik
  - Quiz dan latihan untuk menguji pemahaman
  - Tracking kemajuan belajar pengguna
  - Sistem penyelesaian modul (completion tracking)

### 2. Scoreboard
- **Deskripsi**: Sistem peringkat untuk memotivasi pengguna
- **Komponen**:
  - Poin berdasarkan penyelesaian materi dan quiz
  - Leaderboard global untuk semua pengguna
  - Leaderboard berdasarkan level (beginner, intermediate, advanced)
  - Badge/achievement untuk pencapaian tertentu
  - Statistik kemajuan personal

### 3. Sistem Pengguna
- **Deskripsi**: Manajemen akun pengguna
- **Komponen**:
  - Registrasi dan login
  - Profil pengguna
  - Tracking kemajuan personal
  - Riwayat aktivitas belajar

## Struktur Database

### Tabel Users
- id (PK)
- username
- email
- password_hash
- created_at
- last_login
- role (admin/user)
- total_score
- profile_picture

### Tabel Courses
- id (PK)
- title
- description
- level (beginner/intermediate/advanced)
- order_in_path
- estimated_hours
- created_at
- updated_at

### Tabel Lessons
- id (PK)
- course_id (FK)
- title
- content
- order_in_course
- created_at
- updated_at

### Tabel Quizzes
- id (PK)
- lesson_id (FK)
- title
- description
- points
- created_at
- updated_at

### Tabel Questions
- id (PK)
- quiz_id (FK)
- question_text
- options (JSON)
- correct_answer
- explanation
- points

### Tabel UserProgress
- id (PK)
- user_id (FK)
- lesson_id (FK)
- completed
- completion_date
- score
- attempts

### Tabel UserQuizResults
- id (PK)
- user_id (FK)
- quiz_id (FK)
- score
- completed_at
- attempts

### Tabel Achievements
- id (PK)
- title
- description
- badge_image
- points
- requirements

### Tabel UserAchievements
- id (PK)
- user_id (FK)
- achievement_id (FK)
- earned_at

## Desain UI/UX

### Tema Warna
- **Warna Utama**: Biru pastel (#A5C8E1)
- **Warna Sekunder**: Putih (#F8F9FA)
- **Aksen**: Biru tua pastel (#7DA2C9)
- **Text**: Abu-abu gelap (#343A40)
- **Highlight**: Biru muda (#C1D8F0)

### Halaman Utama
- Header dengan logo NTC dan menu navigasi
- Hero section dengan call-to-action untuk memulai belajar
- Penjelasan singkat tentang learning path
- Preview scoreboard (top 5 pengguna)
- Testimonial atau statistik pengguna

### Dashboard Pengguna
- Ringkasan kemajuan belajar
- Learning path yang sedang diikuti
- Skor dan peringkat terkini
- Achievement yang diperoleh
- Rekomendasi materi berikutnya

### Halaman Learning Path
- Visualisasi jalur pembelajaran dengan node dan koneksi
- Status penyelesaian untuk setiap modul
- Filter berdasarkan level kesulitan
- Detail materi saat node diklik

### Halaman Scoreboard
- Tabel peringkat global
- Filter berdasarkan periode (minggu/bulan/sepanjang masa)
- Filter berdasarkan level
- Profil singkat pengguna saat nama diklik

## Teknologi yang Digunakan
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy dengan MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Styling**: Custom CSS dengan tema biru putih pastel

## Tantangan Potensial
- Memastikan konten pembelajaran C++ yang akurat dan terstruktur
- Mengimplementasikan sistem scoring yang adil dan memotivasi
- Membuat visualisasi learning path yang intuitif
- Memastikan responsivitas UI pada berbagai perangkat
