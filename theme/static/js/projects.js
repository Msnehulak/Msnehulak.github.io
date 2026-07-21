document.addEventListener('DOMContentLoaded', () => {
    if (typeof Swiper !== 'undefined') {
        const swiper = new Swiper('.mySwiper', {
            direction: 'horizontal',
            loop: false, 
            slidesPerView: 'auto',
            grabCursor: true,  
            resistanceRatio: 0.85, 
            spaceBetween: 20,
            speed: 400,
        });
    }
});
