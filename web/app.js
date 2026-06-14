const STORAGE_KEY = "memory-career-roadmap-progress";
const weekCards = [...document.querySelectorAll(".week-card")];
const filterButtons = [...document.querySelectorAll(".filter-button")];
const progressText = document.querySelector("#progressText");
const progressBar = document.querySelector("#progressBar");
const resetButton = document.querySelector("#resetProgress");

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveProgress(completedWeeks) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(completedWeeks));
}

function renderProgress() {
  const completed = loadProgress();
  weekCards.forEach((card) => {
    const week = Number(card.dataset.week);
    card.classList.toggle("completed", completed.includes(week));
    card.setAttribute("aria-pressed", completed.includes(week) ? "true" : "false");
  });

  progressText.textContent = `${completed.length} / 12 周`;
  progressBar.style.width = `${(completed.length / 12) * 100}%`;
}

weekCards.forEach((card) => {
  card.addEventListener("click", () => {
    const week = Number(card.dataset.week);
    const completed = loadProgress();
    const next = completed.includes(week)
      ? completed.filter((item) => item !== week)
      : [...completed, week].sort((a, b) => a - b);
    saveProgress(next);
    renderProgress();
  });
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.toggle("active", item === button));
    weekCards.forEach((card) => {
      card.classList.toggle(
        "hidden",
        filter !== "all" && card.dataset.category !== filter
      );
    });
  });
});

resetButton.addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  renderProgress();
});

renderProgress();
