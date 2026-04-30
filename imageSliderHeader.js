
    const startLoopSlider = () => {
        // PEMBATASAN: Cari header dulu
        const header = document.querySelector('header'); 
        if (!header) return;

    // Pastikan container ada
        const container = document.querySelector('.heroslideshow-container'); 
        if (!container) return;

    // SAMAKAN CLASS: Pastikan di HTML class-nya adalah 'slide'
        const slides = document.querySelectorAll('.slide');
        let currentIndex = 0;

    //Jika tidak ada gambar dengan class 'slide', hentikan fungsi
        if (slides.length === 0) return;

        function changeSlide() {
        //1. Sembunyikan semua gambar secara instan
            slides.forEach(slide => {
                slide.style.display = 'none';
            });
        
        // 2. Tampilkan gambar saat ini
            slides[currentIndex].style.display = 'block';
        
        // 3. Hitung index berikutnya (Looping: kembali ke 0 jika sudah gambar terakhir)
        currentIndex = (currentIndex + 1) % slides.length;
        }

    // Jalankan pertama kali saat halaman dibuka
        changeSlide();

    // Jalankan otomatis terus menerus setiap 3000ms (3 detik)
        setInterval(changeSlide, 1000);
    };

// Pastikan script berjalan setelah semua elemen HTML termuat
document.addEventListener('DOMContentLoaded', startLoopSlider);

