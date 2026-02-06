document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        // Toggle Menu on Click
        menuToggle.addEventListener('click', () => {
            // Slide the menu down/up
            navLinks.classList.toggle('active');
            
            // Animate the hamburger bars into an X
            menuToggle.classList.toggle('is-active');
        });

        // Optional: Close menu when a link is clicked (Professional UX)
        const links = document.querySelectorAll('.nav-links a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('is-active');
            });
        });
        
        // Optional: Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!menuToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('is-active');
            }
        });
    }
});

