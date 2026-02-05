document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            // Toggle the .active class on the links (shows/hides them)
            navLinks.classList.toggle('active');
            
            // Toggle the .is-active class on the hamburger (animates to X)
            menuToggle.classList.toggle('is-active');
        });
    }
});