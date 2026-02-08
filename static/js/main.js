// UKULIMA SAFI AI - Main Logic
// Integrates AI Dashboard (Camera/GPS) & Community Forum (Firebase)

// --- 1. FIREBASE IMPORTS & SETUP ---
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase, ref, push, onChildAdded, serverTimestamp, runTransaction } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyBxiBZy9MbojVEtDWkWOQjnKlc9qeuijjA",
    authDomain: "ukulima-safi.firebaseapp.com",
    projectId: "ukulima-safi",
    storageBucket: "ukulima-safi.firebasestorage.app",
    messagingSenderId: "1025506253951",
    appId: "1:1025506253951:web:08a3aed7878605f423b34a",
    measurementId: "G-T6E3XRJT4J"
};

// Initialize Firebase safely
let app, db;
try {
    app = initializeApp(firebaseConfig);
    db = getDatabase(app);
    console.log("🔥 Firebase Initialized");
} catch (error) {
    console.error("Firebase Error:", error);
}

// --- HELPER FUNCTION: Linkify Text ---
// Converts URLs, Emails, and Phone Numbers into clickable links
function linkify(text) {
    if (!text) return "";

    // 1. Detect URLs (http, https, www)
    const urlPattern = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    text = text.replace(urlPattern, '<a href="$1" target="_blank" style="color:var(--primary-green); text-decoration:underline;">$1</a>');

    // 2. Detect Emails
    const emailPattern = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    text = text.replace(emailPattern, '<a href="mailto:$1" style="color:var(--primary-green); font-weight:bold;">$1</a>');

    // 3. Detect Phone Numbers (e.g., 0712345678, +254712345678)
    // Matches formats common in Kenya
    const phonePattern = /(?:^|\s)((?:\+254|0)7\d{8})(?:\s|$)/g;
    text = text.replace(phonePattern, ' <a href="tel:$1" style="color:var(--primary-green); font-weight:bold;">$1</a> ');

    return text;
}

document.addEventListener("DOMContentLoaded", function () {

    // ======================================================
    //  SECTION A: AI DASHBOARD (Camera, GPS, Prediction)
    // ======================================================

    const uploadForm = document.getElementById("uploadForm");
    const fileInput = document.getElementById('imageUpload');
    
    // --- GPS Logic ---
    if (document.getElementById('userLat') && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                document.getElementById('userLat').value = pos.coords.latitude;
                document.getElementById('userLon').value = pos.coords.longitude;
                console.log("📍 GPS Coords Captured");
            },
            (err) => console.log("GPS Permission denied or unavailable.")
        );
    }

    // --- Camera Logic ---
    const startCameraBtn = document.getElementById('startCameraBtn');
    const cameraContainer = document.getElementById('cameraContainer');
    const video = document.getElementById('videoFeed');
    const canvas = document.getElementById('cameraCanvas');
    const captureBtn = document.getElementById('captureBtn');
    const closeCameraBtn = document.getElementById('closeCameraBtn');
    const capturedPreview = document.getElementById('capturedPreview');
    const previewImg = document.getElementById('previewImg');
    const retakeBtn = document.getElementById('retakeBtn');
    
    let stream = null;
    let capturedBlob = null;

    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', async () => {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                video.srcObject = stream;
                cameraContainer.style.display = 'block';
                startCameraBtn.style.display = 'none';
                if(fileInput) fileInput.value = ''; 
            } catch (err) {
                alert("Camera permission denied.");
            }
        });
    }

    if (captureBtn) {
        captureBtn.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob((blob) => {
                capturedBlob = blob;
                previewImg.src = URL.createObjectURL(blob);
                cameraContainer.style.display = 'none';
                capturedPreview.style.display = 'block';
                stopCamera();
            }, 'image/jpeg');
        });
    }

    function stopCamera() {
        if (stream) { stream.getTracks().forEach(track => track.stop()); stream = null; }
    }

    if (closeCameraBtn) {
        closeCameraBtn.addEventListener('click', () => {
            stopCamera();
            cameraContainer.style.display = 'none';
            startCameraBtn.style.display = 'block';
        });
    }

    if (retakeBtn) {
        retakeBtn.addEventListener('click', () => {
            capturedPreview.style.display = 'none';
            capturedBlob = null;
            startCameraBtn.click();
        });
    }

    // --- Form Submission (Prediction) ---
    if (uploadForm) {
        uploadForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(uploadForm);
            
            if (capturedBlob) {
                formData.set('file', capturedBlob, 'camera_capture.jpg');
            } else if (!fileInput.files[0]) {
                alert("Please select an image or take a photo.");
                return;
            }

            const loading = document.getElementById("loading");
            const results = document.getElementById("resultsArea");

            loading.style.display = "block";
            results.style.display = "none";

            fetch("/predict", { method: "POST", body: formData })
            .then(response => response.json())
            .then(data => {
                loading.style.display = "none";
                if (data.error) { alert(data.error); return; }

                results.style.display = "block";
                
                // Helper to safely set text
                const setText = (id, txt) => { if(document.getElementById(id)) document.getElementById(id).innerText = txt; }

                // 1. Diagnosis
                document.getElementById("resultImage").src = data.image_url;
                setText("resCrop", data.prediction.crop);
                setText("resDisease", data.prediction.disease);
                setText("resStage", data.prediction.growth_stage);
                setText("resConf", data.prediction.confidence);

                // 2. Treatment
                setText("treatInsect", data.prediction.treatment.insecticide || "N/A");
                setText("treatPest", data.prediction.treatment.pesticide || "N/A");
                setText("treatAdvice", data.prediction.treatment.advice || "N/A");

                // 3. Weather
                if (data.weather.data) {
                    const w = data.weather.data;
                    setText("weatherCond", `${w.temp}°C, ${w.humidity}% Humidity (${w.description})`);
                    setText("weatherAdvice", data.weather.advice);
                } else {
                    setText("weatherCond", "Unavailable");
                }

                // 4. Contacts (Agrovets)
                const agroList = document.getElementById("agrovetList");
                if(agroList) {
                    agroList.innerHTML = "";
                    if(data.prediction.contacts && data.prediction.contacts.agrovets){
                        data.prediction.contacts.agrovets.forEach(shop => {
                            const li = document.createElement("li");
                            li.innerHTML = `<strong>${shop.agrovet}</strong> (${shop.region}) - <a href="${shop.map_link}" target="_blank" style="color:var(--primary-green)">Get Directions</a>`;
                            agroList.appendChild(li);
                        });
                    }
                }

                // 5. Contacts (Agronomists)
                const agroDocList = document.getElementById("agronomistList");
                if(agroDocList) {
                    agroDocList.innerHTML = "";
                    if(data.prediction.contacts && data.prediction.contacts.agronomists){
                        data.prediction.contacts.agronomists.forEach(doc => {
                            const li = document.createElement("li");
                            li.innerHTML = `<strong>${doc.agronomist}</strong> (${doc.region}) - Tel: ${doc.phone}`;
                            agroDocList.appendChild(li);
                        });
                    }
                }
            })
            .catch(err => {
                loading.style.display = "none";
                alert("Error connecting to server.");
                console.error(err);
            });
        });
    }


    // ======================================================
    //  SECTION B: COMMUNITY FORUM (Firebase Realtime)
    // ======================================================
    
    const postBtn = document.getElementById('postBtn');
    const postContent = document.getElementById('postContent');
    const discussionContainer = document.getElementById('discussionContainer');

    // --- 1. Post Discussion ---
    if (postBtn && postContent) {
        postBtn.addEventListener('click', () => {
            const text = postContent.value.trim();
            if (!text) { alert("Please write something!"); return; }

            postBtn.disabled = true;
            postBtn.innerText = "Posting...";

            const postsRef = ref(db, 'discussions');
            push(postsRef, {
                user: "Farmer",
                content: text,
                likes: 0,
                dislikes: 0,
                timestamp: serverTimestamp()
            })
            .then(() => {
                postContent.value = "";
                postBtn.disabled = false;
                postBtn.innerText = "🚀 Post Discussion";
            })
            .catch((error) => {
                console.error("Post Error:", error);
                alert("Failed to post.");
                postBtn.disabled = false;
            });
        });
    }

    // --- 2. Load Discussions & Handle Interactions ---
    if (discussionContainer) {
        discussionContainer.innerHTML = ""; // Clear loader

        const postsRef = ref(db, 'discussions');
        onChildAdded(postsRef, (snapshot) => {
            const post = snapshot.val();
            const postId = snapshot.key;
            renderPost(postId, post);
        });
    }

    // --- 3. Render Post Function (Professional UI) ---
    function renderPost(postId, post) {
        const postDiv = document.createElement('div');
        postDiv.className = "post-card";
        
        // Safety check for counts
        const likes = post.likes || 0;
        const dislikes = post.dislikes || 0;

        // Process Content to make Links Clickable
        const processedContent = linkify(post.content);

        postDiv.innerHTML = `
            <div class="post-header">
                <span class="post-user">
                    <div class="user-avatar">👨‍🌾</div>
                    ${post.user || 'Fellow Farmer'}
                </span>
                <span class="post-time">Just now</span>
            </div>
            <!-- INJECTING PROCESSED HTML (with links) -->
            <div class="post-text">${processedContent}</div>
            
            <div class="action-bar">
                <button class="action-btn" id="like-${postId}">
                    👍 <span class="vote-count" id="like-count-${postId}">${likes}</span> Helpful
                </button>
                <button class="action-btn" id="dislike-${postId}">
                    👎 <span class="vote-count" id="dislike-count-${postId}">${dislikes}</span>
                </button>
                <button class="action-btn reply-toggle-btn" id="toggle-${postId}">
                    💬 Reply
                </button>
            </div>

            <!-- Replies Section (Hidden by default) -->
            <div class="replies-wrapper" id="replies-container-${postId}">
                <div id="replies-list-${postId}"></div>
                
                <div class="reply-input-group">
                    <input type="text" id="input-${postId}" class="reply-input" placeholder="Add your advice...">
                    <button class="send-reply-btn" id="btn-${postId}">Send</button>
                </div>
            </div>
        `;

        // Prepend to list (Newest shows at top conceptually)
        discussionContainer.insertBefore(postDiv, discussionContainer.firstChild);

        // --- ATTACH LISTENERS ---

        // A. Like Button (Transaction)
        document.getElementById(`like-${postId}`).addEventListener('click', () => {
            const likeRef = ref(db, `discussions/${postId}/likes`);
            runTransaction(likeRef, (currentLikes) => {
                return (currentLikes || 0) + 1;
            }).then(() => {
                // Optimistic UI Update
                const countSpan = document.getElementById(`like-count-${postId}`);
                countSpan.innerText = parseInt(countSpan.innerText) + 1;
            });
        });

        // B. Dislike Button (Transaction)
        document.getElementById(`dislike-${postId}`).addEventListener('click', () => {
            const dislikeRef = ref(db, `discussions/${postId}/dislikes`);
            runTransaction(dislikeRef, (currentDislikes) => {
                return (currentDislikes || 0) + 1;
            }).then(() => {
                const countSpan = document.getElementById(`dislike-count-${postId}`);
                countSpan.innerText = parseInt(countSpan.innerText) + 1;
            });
        });

        // C. Toggle Reply Section
        document.getElementById(`toggle-${postId}`).addEventListener('click', () => {
            const wrapper = document.getElementById(`replies-container-${postId}`);
            wrapper.style.display = (wrapper.style.display === "block") ? "none" : "block";
        });

        // D. Load Replies
        const repliesList = document.getElementById(`replies-list-${postId}`);
        const repliesRef = ref(db, `discussions/${postId}/replies`);
        
        onChildAdded(repliesRef, (replySnap) => {
            const reply = replySnap.val();
            const replyDiv = document.createElement('div');
            replyDiv.className = "reply-item";
            
            // Linkify replies too!
            const processedReply = linkify(reply.text);

            replyDiv.innerHTML = `
                <span class="reply-user">↳ Farmer replied:</span>
                ${processedReply}
            `;
            repliesList.appendChild(replyDiv);
        });

        // E. Send Reply
        const sendBtn = document.getElementById(`btn-${postId}`);
        const replyInput = document.getElementById(`input-${postId}`);

        sendBtn.addEventListener('click', () => {
            const replyText = replyInput.value.trim();
            if(!replyText) return;

            push(repliesRef, {
                text: replyText,
                timestamp: serverTimestamp()
            });
            replyInput.value = "";
        });
    }

});