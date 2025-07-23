const slideFrame = document.getElementById('slide-frame');
const playPauseBtn = document.getElementById('play-pause');
const nextBtn = document.getElementById('next-map');

let currentSlide = 0;
let slideInterval;
let playing = false;

function nextSlide() {
  const pages = ["rom1a.html", "rom1b.html", "rom1c.html", "pwrs.html"];
  currentSlide = (currentSlide + 1) % pages.length;
  slideFrame.src = pages[currentSlide];
}

function toggleSlideShow() {
  if (playing) {
    clearInterval(slideInterval);
    playPauseBtn.textContent = 'Play';
    playing = false;
  } else {
    slideInterval = setInterval(nextSlide, 30000); // Change 2000 to your desired interval in milliseconds
    playPauseBtn.textContent = 'Pause';
    playing = true;
  }
}

playPauseBtn.addEventListener('click', toggleSlideShow);
nextBtn.addEventListener('click', nextSlide);

/* Optional: Preload other pages for smoother transitions
window.onload = function() {
  const pages = ["rom1a.html", "rom1b.html"];
  pages.forEach(page => {
    const preloadFrame = document.createElement('iframe');
    preloadFrame.style.display = 'none';
    preloadFrame.src = page;
    document.body.appendChild(preloadFrame);
  });
}
*/