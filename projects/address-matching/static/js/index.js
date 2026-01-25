$(document).ready(function () {
  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function () {
    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");

  });

  // Scoring info popup
  const scoringIcon = document.getElementById('scoringInfoIcon');
  const scoringPopup = document.getElementById('scoringPopup');
  const closePopup = document.querySelector('.close-popup');

  if (scoringIcon && scoringPopup) {
    scoringIcon.addEventListener('click', (e) => {
      e.stopPropagation();
      scoringPopup.classList.toggle('show');
    });

    if (closePopup) {
      closePopup.addEventListener('click', () => {
        scoringPopup.classList.remove('show');
      });
    }

    document.addEventListener('click', (e) => {
      if (!scoringPopup.contains(e.target) && e.target !== scoringIcon) {
        scoringPopup.classList.remove('show');
      }
    });
  }
})
