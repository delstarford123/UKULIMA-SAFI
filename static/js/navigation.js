/**
 * UKULIMA SAFI AI - Navigation Logic
 * Handles the responsive hamburger menu toggle and user interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        // 1. Toggle Menu on Click
        menuToggle.addEventListener('click', () => {
            // Slide the menu down/up
            navLinks.classList.toggle('active');
            
            // Animate the hamburger bars into an X
            menuToggle.classList.toggle('is-active');
        });

        // 2. Close menu when a link is clicked (Professional UX)
        // This ensures the menu shuts after a user selects a page on mobile
        const links = document.querySelectorAll('.nav-links a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('is-active');
            });
        });
        
        // 3. Close menu when clicking outside the navbar
        // This is important if the user opens the menu but changes their mind
        document.addEventListener('click', (e) => {
            const navbar = document.querySelector('.navbar');
            // If the click is NOT inside the navbar, close the menu
            if (!navbar.contains(e.target)) {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('is-active');
            }
        });
    }
});