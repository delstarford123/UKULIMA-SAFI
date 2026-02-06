/**
 * UKULIMA SAFI AI - GPS & Embedded Map Navigation
 * Features: Auto-GPS, Leaflet Routing, and Smart Fallback for unknown locations.
 */

let currentDestination = "";
let currentRegion = ""; // Store region for fallback logic
let mapInstance = null;
let routingControl = null;

// =========================================================
// 1. GEOLOCATION FUNCTIONS
// =========================================================

function getLocation(auto = false) {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.getElementById('gpsBtn');
    
    if (!statusDiv || !gpsBtn) return;

    // If auto-load and we already have data, don't show "Connecting..." text
    if (auto && sessionStorage.getItem('userLat')) return;

    statusDiv.innerHTML = "Connecting to Satellites...";
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
    
    // 1. Save session data
    sessionStorage.setItem('userLat', lat);
    sessionStorage.setItem('userLon', lon);
    
    // 2. Update UI
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.getElementById('gpsBtn');

    if (statusDiv && gpsBtn) {
        statusDiv.innerHTML = ` <strong>GPS Locked:</strong> ${lat.toFixed(4)}, ${lon.toFixed(4)}`;
        statusDiv.style.color = "var(--primary-green)";
        statusDiv.className = "status-success";
        gpsBtn.disabled = false;
        gpsBtn.innerText = "Update Location";
        
        // Clear manual input to avoid confusion
        const manualInput = document.getElementById('manualLocation');
        if(manualInput) manualInput.value = ""; 
    }
}

function showError(error) {
    const statusDiv = document.getElementById('status');
    const gpsBtn = document.getElementById('gpsBtn');
    
    let msg = " GPS Error: " + error.message;
    if (error.code === error.PERMISSION_DENIED) {
        msg = " GPS Denied. Please allow location access.";
    } else if (error.code === error.TIMEOUT) {
        msg = " GPS Timeout. Try moving outside.";
    }

    if (statusDiv) statusDiv.innerHTML = msg;
    if (gpsBtn) {
        gpsBtn.disabled = false;
        gpsBtn.innerText = "Try Again";
    }
}

// =========================================================
// 2. MODAL & EMBEDDED MAP LOGIC
// =========================================================

function initMap() {
    // If map already exists, don't re-initialize
    if (mapInstance) return;

    // Default center (Kenya)
    mapInstance = L.map('embeddedMap').setView([0.2827, 34.7519], 13); // Centered on Kakamega

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(mapInstance);
}

// NOTE: Now accepts two arguments (Name AND Region)
async function openNavigationModal(destName, destRegion) {
    const userLat = sessionStorage.getItem('userLat');
    const userLon = sessionStorage.getItem('userLon');
    const manualLoc = document.getElementById('manualLocation')?.value;

    // 1. Check if we have an Origin (GPS or Manual)
    if ((!userLat || !userLon) && !manualLoc) {
        alert("Please enable GPS or enter your town first!");
        document.querySelector('.gps-action-card').scrollIntoView({behavior: 'smooth'});
        return;
    }

    currentDestination = destName;
    currentRegion = destRegion; // Save for fallback
    document.getElementById('modalDestName').innerText = destName;
    
    // Show Modal
    const modal = document.getElementById('navModal');
    modal.style.display = 'block';

    // 2. Initialize Map (Must happen after modal is visible)
    setTimeout(() => {
        initMap();
        mapInstance.invalidateSize(); // CRITICAL: Fixes grey map issue
        calculateRoute(userLat, userLon, manualLoc, destName, destRegion);
    }, 200);
}

async function calculateRoute(lat, lon, manualLoc, destName, destRegion) {
    // A. Define Origin Waypoint
    let originLatLng;

    if (lat && lon) {
        originLatLng = L.latLng(lat, lon);
        document.getElementById('originLabel').innerText = "My GPS Location";
    } else {
        // Geocode manual origin
        const coords = await getCoordsFromNominatim(manualLoc);
        if (coords) {
            originLatLng = L.latLng(coords.lat, coords.lon);
            document.getElementById('originLabel').innerText = manualLoc;
        } else {
            alert("Could not find YOUR location. Please check spelling.");
            return;
        }
    }

    // B. Define Destination Waypoint (WITH FALLBACK)
    let destLatLng;
    
    // Attempt 1: Search for specific "Shop Name, Region, Kenya"
    let destCoords = await getCoordsFromNominatim(`${destName}, ${destRegion}, Kenya`);

    if (!destCoords) {
        console.warn("Exact shop not found, trying region fallback...");
        
        // Attempt 2: Fallback to just "Region, Kenya"
        destCoords = await getCoordsFromNominatim(`${destRegion}, Kenya`);
        
        if (destCoords) {
            // Update UI to be honest with the user
            document.getElementById('modalDestName').innerText = `${destName} (Map showing route to ${destRegion} center)`;
        }
    }

    // Attempt 3: If still nothing, give up and use external Google Maps
    if (!destCoords) {
        alert(`Could not locate ${destRegion} on the map. Opening Google Maps directly.`);
        openExternalGoogleMaps('driving');
        closeModal();
        return;
    }
    
    destLatLng = L.latLng(destCoords.lat, destCoords.lon);

    // C. Draw Route using Leaflet Routing Machine
    if (routingControl) {
        mapInstance.removeControl(routingControl); // Remove old line
    }

    routingControl = L.Routing.control({
        waypoints: [originLatLng, destLatLng],
        routeWhileDragging: false,
        showAlternatives: false,
        fitSelectedRoutes: true, // Auto-zoom to fit route
        lineOptions: {
            styles: [{color: '#800000', opacity: 0.8, weight: 6}] // Maroon line
        },
        createMarker: function(i, wp, nWps) {
            if (i === 0) return L.marker(wp.latLng).bindPopup("You");
            if (i === nWps - 1) return L.marker(wp.latLng).bindPopup(destName);
            return null;
        },
        show: false // Hide text instructions to save space
    }).addTo(mapInstance);
}

// Helper: Fetch Coordinates using OpenStreetMap (Nominatim)
async function getCoordsFromNominatim(query) {
    try {
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`;
        const response = await fetch(url);
        const data = await response.json();
        if (data && data.length > 0) {
            return { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
        }
        return null;
    } catch (e) {
        console.error("Geocoding error:", e);
        return null;
    }
}

// =========================================================
// 3. EXTERNAL HANDOFF (GOOGLE MAPS)
// =========================================================

function openExternalGoogleMaps(mode) {
    const lat = sessionStorage.getItem('userLat');
    const lon = sessionStorage.getItem('userLon');
    const manualLoc = document.getElementById('manualLocation')?.value;
    
    let originParam = "";

    // Determine Origin
    if (manualLoc) {
        originParam = `origin=${encodeURIComponent(manualLoc)}`;
    } else if (lat && lon) {
        originParam = `origin=${lat},${lon}`;
    }

    // Determine Destination (Name + Region is best for Google)
    const fullDest = `${currentDestination}, ${currentRegion}`;
    
    // Standard Google Maps Universal URL
    const url = `https://www.google.com/maps/dir/?api=1&${originParam}&destination=${encodeURIComponent(fullDest)}&travelmode=${mode}`;
    
    window.open(url, '_blank');
}

function closeModal() {
    const modal = document.getElementById('navModal');
    if (modal) modal.style.display = 'none';
}

// Close modal if user clicks outside
window.onclick = function(event) {
    const modal = document.getElementById('navModal');
    if (event.target == modal) {
        closeModal();
    }
}

// =========================================================
// 4. AUTO-LOAD ON START
// =========================================================
document.addEventListener("DOMContentLoaded", function() {
    const savedLat = sessionStorage.getItem('userLat');
    
    // Only auto-trigger if we don't have location yet
    if (savedLat) {
        const statusDiv = document.getElementById('status');
        if(statusDiv) statusDiv.innerHTML = "✅ GPS Ready (Saved)";
    } else {
        getLocation(true); // True = silent mode (no loading text if fails)
    }
});