// UKULIMA SAFI AI - GPS Navigation Logic

document.addEventListener("DOMContentLoaded", function() {
    // Check if we already have a location saved from a previous page
    const savedLat = sessionStorage.getItem('userLat');
    const savedLon = sessionStorage.getItem('userLon');

    if (savedLat && savedLon) {
        showPosition({
            coords: { latitude: savedLat, longitude: savedLon }
        }, true); // 'true' indicates it was loaded from cache
    }
});

function getLocation() {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.querySelector('.btn-primary');

    // Update UI to show searching state
    statusDiv.innerHTML = "📡 Contacting Satellites...";
    statusDiv.className = "status-searching";
    gpsBtn.disabled = true;
    gpsBtn.innerText = "Locating...";

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError, {
            enableHighAccuracy: true, // Request best possible GPS
            timeout: 10000,           // Wait max 10 seconds
            maximumAge: 0             // Don't use old cached positions
        });
    } else {
        statusDiv.innerHTML = "⚠️ Geolocation is not supported by this browser.";
        statusDiv.className = "status-error";
        gpsBtn.disabled = false;
        gpsBtn.innerText = "Try Again";
    }
}

function showPosition(position, isCached = false) {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.querySelector('.btn-primary'); // The button in the HTML
    
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    // 1. SAVE TO STORAGE (So other pages can use it)
    sessionStorage.setItem('userLat', lat);
    sessionStorage.setItem('userLon', lon);

    // 2. UPDATE UI
    let message = isCached ? "📍 Location Retrieved from Memory:" : "✅ GPS Signal Locked:";
    
    statusDiv.innerHTML = `
        <div style="margin-bottom: 10px;">${message}</div>
        <span class="coords-box">Lat: ${lat.toFixed(4)}</span>
        <span class="coords-box">Lon: ${lon.toFixed(4)}</span>
        <div style="margin-top:10px; font-size: 0.9rem;">
            System is now calibrated to your location.
        </div>
    `;
    statusDiv.className = "status-success";

    // Reset button
    if (gpsBtn) {
        gpsBtn.innerText = "📡 Refresh Location";
        gpsBtn.disabled = false;
    }

    // 3. ENHANCE LINKS (Optional: Append coords to links if backend supports it)
    // This makes the "Find Agrovets" buttons smarter immediately
    updateLinkWithCoords('/shops', lat, lon);
    updateLinkWithCoords('/vets', lat, lon);
}

function showError(error) {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.querySelector('.btn-primary');
    
    let msg = "";
    switch(error.code) {
        case error.PERMISSION_DENIED:
            msg = "🚫 User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            msg = "❌ Location information is unavailable.";
            break;
        case error.TIMEOUT:
            msg = "?? The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            msg = "⚠️ An unknown error occurred.";
            break;
    }
    
    statusDiv.innerHTML = msg;
    statusDiv.className = "status-error";
    
    if (gpsBtn) {
        gpsBtn.disabled = false;
        gpsBtn.innerText = "Try Again";
    }
}

// Helper to add query params to the static links on the page
function updateLinkWithCoords(pathStub, lat, lon) {
    // Find links that contain the path (e.g., href="/shops")
    const links = document.querySelectorAll(`a[href^="${pathStub}"]`);
    links.forEach(link => {
        // Change href to /shops?lat=...&lon=...
        link.href = `${pathStub}?lat=${lat}&lon=${lon}`;
    });
}