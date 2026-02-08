/**
 * UKULIMA SAFI AI - Navigation Logic
 * Handles responsive menu toggle and Active Link Highlighting.
 */

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    const allLinks = document.querySelectorAll('.nav-links a');

    // --- 1. ACTIVE LINK HIGHLIGHTER ---
    // Automatically adds 'current-page' class to the link matching the browser URL
    const currentPath = window.location.pathname;
    
    allLinks.forEach(link => {
        // Get the path from the link (e.g., /dashboard)
        const linkPath = link.getAttribute('href');
        
        // Exact match (e.g. / == /) OR partial match for sub-pages (e.g. /guide matches /guide)
        if (linkPath === currentPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('current-page');
        }
    });

    // --- 2. MOBILE MENU LOGIC ---
    if (menuToggle && navLinks) {
        // Toggle Menu
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('is-active');
        });

        // Close menu when a link is clicked
        allLinks.forEach(link => {
            link.addEventListener('click', () => {
                closeMenu();
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navLinks.classList.contains('active') && 
                !navLinks.contains(e.target) && 
                !menuToggle.contains(e.target)) {
                closeMenu();
            }
        });

        // Safety: Close menu on screen resize to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1100) {
                closeMenu();
            }
        });
        
        function closeMenu() {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('is-active');
        }
    }
});