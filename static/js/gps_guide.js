/**
 * UKULIMA SAFI AI - GPS Navigation Logic
 * Handles Geolocation, Coordinate storage, and Google Maps Navigation Modal.
 * Includes Manual Location fallback for Desktops.
 */

// Global variable to store the selected destination temporarily for the modal
let currentDestination = "";

// --- 1. GEOLOCATION FUNCTIONS ---

function getLocation() {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.getElementById('gpsBtn');
    
    // Guard clause in case function is called on a page without these elements
    if (!statusDiv || !gpsBtn) return;

    // Clear previous sessions to force fresh data
    sessionStorage.removeItem('userLat');
    sessionStorage.removeItem('userLon');

    statusDiv.innerHTML = "📡 Connecting to Satellites...";
    statusDiv.style.color = "var(--primary-maroon)";
    statusDiv.className = "status-searching";
    gpsBtn.disabled = true;
    gpsBtn.innerText = "Locating...";

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(updateLocationData, showError, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    } else {
        statusDiv.innerHTML = "⚠️ Geolocation not supported by this browser.";
        gpsBtn.disabled = false;
    }
}

function updateLocationData(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.getElementById('gpsBtn');

    // 1. Save for session (so other pages know where we are)
    sessionStorage.setItem('userLat', lat);
    sessionStorage.setItem('userLon', lon);
    
    // 2. Update hidden inputs if they exist (for Form submission on Dashboard)
    if(document.getElementById('currentLat')) {
        document.getElementById('currentLat').value = lat;
        document.getElementById('currentLon').value = lon;
    }
    
    if(document.getElementById('userLat')) {
        document.getElementById('userLat').value = lat;
        document.getElementById('userLon').value = lon;
    }

    // 3. UI Feedback
    if (statusDiv && gpsBtn) {
        statusDiv.innerHTML = `✅ <strong>GPS Locked:</strong> ${lat.toFixed(4)}, ${lon.toFixed(4)}`;
        statusDiv.className = "status-success";
        gpsBtn.disabled = false;
        gpsBtn.innerText = "📍 Update Location";
        
        // Clear manual input to avoid confusion
        if(document.getElementById('manualLocation')) {
            document.getElementById('manualLocation').value = ""; 
        }
    }
}

function showError(error) {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.getElementById('gpsBtn');
    
    let msg = "⚠️ GPS Error: " + error.message;
    if (error.code === error.PERMISSION_DENIED) {
        msg = "🚫 GPS Denied. Please allow location access in your browser settings.";
    } else if (error.code === error.TIMEOUT) {
        msg = "⏱️ GPS Timeout. Please try again outside.";
    }

    if (statusDiv) statusDiv.innerHTML = msg;
    if (gpsBtn) {
        gpsBtn.disabled = false;
        gpsBtn.innerText = "Try Again";
    }
}

// --- 2. MODAL & NAVIGATION LOGIC ---

function openNavigationModal(destination) {
    const lat = sessionStorage.getItem('userLat');
    const manualInput = document.getElementById('manualLocation');
    const manualLoc = manualInput ? manualInput.value : "";

    // Check if we have EITHER GPS OR Manual Input
    if (!lat && !manualLoc) {
        alert("⚠️ Please Click 'Use My Live GPS' OR enter your location manually in the text box.");
        const gpsCard = document.querySelector('.gps-action-card');
        if (gpsCard) gpsCard.scrollIntoView({behavior: 'smooth'});
        return;
    }

    currentDestination = destination;
    const modalDest = document.getElementById('modalDestName');
    if (modalDest) modalDest.innerText = destination;

    const modal = document.getElementById('navModal');
    if (modal) modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('navModal');
    if (modal) modal.style.display = 'none';
}

function startNavigation(mode) {
    const lat = sessionStorage.getItem('userLat');
    const lon = sessionStorage.getItem('userLon');
    const manualInput = document.getElementById('manualLocation');
    const manualLoc = manualInput ? manualInput.value.trim() : "";
    
    let originParam = "";

    // PRIORITY: Use Manual Input if typed, otherwise use GPS
    if (manualLoc) {
        originParam = encodeURIComponent(manualLoc);
    } else if (lat && lon) {
        originParam = `${lat},${lon}`;
    } else {
        alert("Please enter a location or use GPS.");
        return;
    }

    // Construct Google Maps URL with Origin, Destination, and Travel Mode
    // mode options: 'driving', 'walking', 'bicycling'
    const url = `https://www.google.com/maps/dir/?api=1&origin=${originParam}&destination=${encodeURIComponent(currentDestination)}&travelmode=${mode}`;
    
    // Open in new tab
    window.open(url, '_blank');
    
    // Close modal
    closeModal();
}

// Close modal if user clicks outside of the content box
window.onclick = function(event) {
    const modal = document.getElementById('navModal');
    if (event.target == modal) {
        closeModal();
    }
}

// --- 3. AUTO-LOAD ON START ---
document.addEventListener("DOMContentLoaded", function() {
    const savedLat = sessionStorage.getItem('userLat');
    const savedLon = sessionStorage.getItem('userLon');
    
    // Only attempt to update if we have saved coords AND we are on the GPS page
    if (savedLat && savedLon) {
        // Mock a position object to reuse the update function
        const mockPosition = { 
            coords: { 
                latitude: parseFloat(savedLat), 
                longitude: parseFloat(savedLon) 
            } 
        };
        updateLocationData(mockPosition);
    }
});