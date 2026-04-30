// ============================================================
// MANUAL IMAGE SLIDER - GALLERY (Body Section)
// Terpisah sepenuhnya dari header auto-loop slider
// ============================================================
 
document.addEventListener('DOMContentLoaded', function () {
 
    // --- Ambil elemen slider gallery (bukan header) ---
    const galSlider = document.querySelector('.galimage-slider');
    if (!galSlider) return; // Hentikan jika elemen tidak ada di halaman ini
 
    const slides   = galSlider.querySelectorAll('.galslide');
    const buttons  = document.querySelectorAll('.slider-btn');
    const btnPrev  = document.getElementById('btn-prev');
    const btnNext  = document.getElementById('btn-next');
 
    if (slides.length === 0) return;
 
    let currSlide = 0;
    const lastSlide = slides.length - 1;

    //Manual Image Slider
    var manualNav = function (manual)
    {   //function tp dimasukkan ke item var, manual itu parameter
        slides.forEach(function (galslide) {
            galslide.classList.remove("active");      

            buttons.forEach((btn) => {
            btn.classList.remove("active");     
            });
        });

        slides[manual].classList.add("active");
        buttons[manual].classList.add("active");
    }

 
    // --- Fungsi utama: tampilkan slide tertentu ---
    function goToSlide(index) {
        // Hapus class active dari semua slide & tombol navigasi
        slides.forEach(function (slide) {
            slide.classList.remove('active');
        });
        buttons.forEach(function (btn) {
            btn.classList.remove('active');
        });
 
        // Aktifkan slide & tombol sesuai index
        slides[index].classList.add('active');
        if (buttons[index]) {
            buttons[index].classList.add('active');
        }
 
        currSlide = index;
    }
 
    // --- Inisialisasi: tampilkan slide pertama ---
    goToSlide(0);
 
    // --- Navigasi dot (tombol bulat kecil) ---
    buttons.forEach(function (btn, idx) {
        btn.addEventListener('click', function () {
            goToSlide(idx);
        });
    });
 
    // --- Tombol Prev ---
    if (btnPrev) {
        btnPrev.addEventListener('click', function () {
            const target = currSlide <= 0 ? lastSlide : currSlide - 1;
            goToSlide(target);
        });
    }
 
    // --- Tombol Next ---
    if (btnNext) {
        btnNext.addEventListener('click', function () {
            const target = currSlide >= lastSlide ? 0 : currSlide + 1;
            goToSlide(target);
        });
    }
 
    // --- Autoplay (opsional, hapus/comment jika tidak diinginkan) ---
    //setInterval(function () {
        //const target = currSlide >= lastSlide ? 0 : currSlide + 1;
        //goToSlide(target);
    //}, 4000);//

        buttons.forEach(function(btn, idx) 
    {   
        btn.addEventListener("click", function() {
            manualNav(idx); //idx adlh manual
            currSlide = idx;
            console.log(currSlide);
        });
    })

    function prev() 
    {
        currSlide--;
        if(currSlide < 0){
            currSlide = lastSlide;
        }
        manualNav(currSlide);
    }

    function next() 
    {
        currSlide++;
        if(currSlide > lastSlide){
            currSlide = 0;
        }
        manualNav(currSlide);
    }
    // Jalankan otomatis terus menerus setiap 3000ms (3 detik)
    setInterval(changeSlide, 4000);

document.addEventListener('DOMContentLoaded', startLoopSlider);
});
 
