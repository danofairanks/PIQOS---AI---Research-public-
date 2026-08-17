// Client-side filter across the index cards. Vanilla JS, no build step,
// no external dependency -- matches the rest of this repo's tooling.
// Purely cosmetic: hides non-matching .card elements (and any section /
// subgroup left with zero visible cards) by substring match against
// each card's own text. Does not touch, fetch, or alter any research
// content.
(function () {
  const input = document.getElementById("search");
  if (!input) return;

  const cards = Array.from(document.querySelectorAll(".card"));
  const grids = Array.from(document.querySelectorAll(".card-grid"));
  const sections = Array.from(document.querySelectorAll("section.doc-section"));
  const noResults = document.getElementById("no-results");

  input.addEventListener("input", function () {
    const query = input.value.trim().toLowerCase();
    let totalVisible = 0;

    cards.forEach(function (card) {
      const match = query === "" || card.textContent.toLowerCase().includes(query);
      card.classList.toggle("hidden", !match);
      if (match) totalVisible += 1;
    });

    // Collapse a subgroup heading (e.g. "Published"/"Drafts") together
    // with its own grid when every card inside that grid is hidden.
    grids.forEach(function (grid) {
      const anyVisible = grid.querySelectorAll(".card:not(.hidden)").length > 0;
      grid.classList.toggle("hidden", !anyVisible);
      const heading = grid.previousElementSibling;
      if (heading && heading.classList.contains("subgroup")) {
        heading.classList.toggle("hidden", !anyVisible);
      }
    });

    // Collapse an entire section (heading + intro note) when none of
    // its own cards match, so filtering doesn't leave a page of empty
    // headers between the search box and the "no results" message.
    sections.forEach(function (section) {
      const anyVisible = section.querySelectorAll(".card:not(.hidden)").length > 0;
      section.classList.toggle("hidden", !anyVisible);
    });

    if (noResults) {
      noResults.style.display = totalVisible === 0 ? "block" : "none";
    }
  });
})();
