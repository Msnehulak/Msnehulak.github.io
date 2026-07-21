// Inicializace Swiperu na elementu s třídou .mySwiper
const swiper = new Swiper('.mySwiper', {
  // Horizontální směr swipeování
  direction: 'horizontal',
  
  // ZÁKAZ nekonečného protáčení (má to pevný začátek a konec)
  loop: false,
  
  slidesPerView: 3,

  // Umožní chytit a tahat kartu myší na PC (změní i kurzor na ručičku)
  grabCursor: true,
  
  // Vytvoří lehký efekt "pružení" na první a poslední kartě
  resistanceRatio: 0.85,
 
spaceBetween: 20,

  // Rychlost přechodu mezi kartami v milisekundách
  speed: 400,
});
