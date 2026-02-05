// UKULIMA SAFI AI - Main Logic
document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    
    // Attempt to get GPS immediately on load
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            document.getElementById('userLat').value = position.coords.latitude;
            document.getElementById('userLon').value = position.coords.longitude;
            console.log("GPS Location set.");
        });
    }

    // --- CAMERA LOGIC ---
    const startCameraBtn = document.getElementById('startCameraBtn');
    const cameraContainer = document.getElementById('cameraContainer');
    const video = document.getElementById('videoFeed');
    const canvas = document.getElementById('cameraCanvas');
    const captureBtn = document.getElementById('captureBtn');
    const closeCameraBtn = document.getElementById('closeCameraBtn');
    const capturedPreview = document.getElementById('capturedPreview');
    const previewImg = document.getElementById('previewImg');
    const retakeBtn = document.getElementById('retakeBtn');
    const fileInput = document.getElementById('imageUpload');
    
    let stream = null;
    let capturedBlob = null; // Store the captured image blob

    // 1. Start Camera
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', async () => {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "environment" } // Prefer back camera on phones
                });
                video.srcObject = stream;
                cameraContainer.style.display = 'block';
                startCameraBtn.style.display = 'none';
                fileInput.value = ''; // Clear file input if user switches to camera
            } catch (err) {
                alert("Could not access camera. Please allow camera permissions.");
                console.error("Camera Error:", err);
            }
        });
    }

    // 2. Capture Photo
    if (captureBtn) {
        captureBtn.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Convert to Blob
            canvas.toBlob((blob) => {
                capturedBlob = blob;
                // Create object URL for preview
                previewImg.src = URL.createObjectURL(blob);
                
                // Switch UI
                cameraContainer.style.display = 'none';
                capturedPreview.style.display = 'block';
                stopCamera();
            }, 'image/jpeg');
        });
    }

    // 3. Stop/Close Camera
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }

    if (closeCameraBtn) {
        closeCameraBtn.addEventListener('click', () => {
            stopCamera();
            cameraContainer.style.display = 'none';
            startCameraBtn.style.display = 'block';
        });
    }

    // 4. Retake Photo
    if (retakeBtn) {
        retakeBtn.addEventListener('click', () => {
            capturedPreview.style.display = 'none';
            capturedBlob = null;
            startCameraBtn.click(); // Restart camera
        });
    }


    // --- FORM SUBMISSION ---
    if (uploadForm) {
        uploadForm.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const formData = new FormData(uploadForm);
            
            // If user took a photo, append it to formData manually
            // We give it a filename 'camera_capture.jpg' so Flask sees it as a file
            if (capturedBlob) {
                formData.set('file', capturedBlob, 'camera_capture.jpg');
            } else if (!fileInput.files[0]) {
                alert("Please select an image or take a photo.");
                return;
            }

            const loading = document.getElementById("loading");
            const results = document.getElementById("resultsArea");

            // UI Updates
            loading.style.display = "block";
            results.style.display = "none";

            fetch("/predict", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = "none";
                if (data.error) {
                    alert(data.error);
                    return;
                }

                results.style.display = "block";

                // 1. Diagnosis
                document.getElementById("resultImage").src = data.image_url;
                document.getElementById("resCrop").innerText = data.prediction.crop;
                document.getElementById("resDisease").innerText = data.prediction.disease;
                document.getElementById("resStage").innerText = data.prediction.growth_stage;
                document.getElementById("resConf").innerText = data.prediction.confidence;

                // 2. Treatment
                document.getElementById("treatInsect").innerText = data.prediction.treatment.insecticide || "N/A";
                document.getElementById("treatPest").innerText = data.prediction.treatment.pesticide || "N/A";
                document.getElementById("treatAdvice").innerText = data.prediction.treatment.advice || "N/A";

                // 3. Weather
                if (data.weather.data) {
                    const w = data.weather.data;
                    document.getElementById("weatherCond").innerText = `${w.temp}°C, ${w.humidity}% Humidity (${w.description})`;
                    document.getElementById("weatherAdvice").innerText = data.weather.advice;
                } else {
                    document.getElementById("weatherCond").innerText = "Unavailable";
                }

                // 4. Contacts (Agrovets)
                const agroList = document.getElementById("agrovetList");
                agroList.innerHTML = "";
                if(data.prediction.contacts && data.prediction.contacts.agrovets){
                    data.prediction.contacts.agrovets.forEach(shop => {
                        const li = document.createElement("li");
                        li.innerHTML = `<strong>${shop.agrovet}</strong> (${shop.region}) - <a href="${shop.map_link}" target="_blank" style="color:var(--primary-green)">Get Directions</a>`;
                        agroList.appendChild(li);
                    });
                }

                // 5. Contacts (Agronomists)
                const agroDocList = document.getElementById("agronomistList");
                agroDocList.innerHTML = "";
                if(data.prediction.contacts && data.prediction.contacts.agronomists){
                    data.prediction.contacts.agronomists.forEach(doc => {
                        const li = document.createElement("li");
                        li.innerHTML = `<strong>${doc.agronomist}</strong> (${doc.region}) - Tel: ${doc.phone}`;
                        agroDocList.appendChild(li);
                    });
                }

            })
            .catch(err => {
                loading.style.display = "none";
                alert("Error connecting to AI server.");
                console.error(err);
            });
        });
    }
});