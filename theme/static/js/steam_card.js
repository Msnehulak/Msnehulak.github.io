document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('games-container');
  const sortSelect = document.getElementById('sort-select');
  const searchInput = document.getElementById('game-search');

  // Funkce pro řazení
  function sortGames() {
    const cards = Array.from(container.querySelectorAll('.game-card'));
    const [criterion, direction] = sortSelect.value.split('-');

    cards.sort((a, b) => {
      let valA, valB;

      if (criterion === 'playtime') {
        valA = parseInt(a.dataset.playtime, 10);
        valB = parseInt(b.dataset.playtime, 10);
      } else if (criterion === 'name') {
        valA = a.dataset.name.toLowerCase();
        valB = b.dataset.name.toLowerCase();
      }

      if (valA < valB) return direction === 'asc' ? -1 : 1;
      if (valA > valB) return direction === 'asc' ? 1 : -1;
      return 0;
    });

    // Znovu vložíme seřazené prkvy do DOMu
    cards.forEach(card => container.appendChild(card));
  }

  // Funkce pro vyhledávání / filtr
  function filterGames() {
    const query = searchInput.value.toLowerCase();
    const cards = container.querySelectorAll('.game-card');

    cards.forEach(card => {
      const name = card.dataset.name.toLowerCase();
      card.style.display = name.includes(query) ? '' : 'none';
    });
  }

  // Event Listenery
  sortSelect.addEventListener('change', sortGames);
  searchInput.addEventListener('input', filterGames);

  // Výchozí seřazení při načtení
  sortGames();
});
