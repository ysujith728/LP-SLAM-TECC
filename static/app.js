 // static/app.js

// -------------------------
// DOM ELEMENTS
// -------------------------
const analyzeBtn = document.getElementById("analyzeBtn");
const sampleBtn = document.getElementById("sampleBtn");
const imageUrlInput = document.getElementById("imageUrl");
const fileInput = document.getElementById("fileInput");  // NEW
const annotationsDiv = document.getElementById("annotations");
const logDiv = document.getElementById("log");
const semanticPre = document.getElementById("semantic");

function log(msg) {
  const time = new Date().toLocaleTimeString();
  const el = document.createElement("div");
  el.textContent = `[${time}] ${msg}`;
  logDiv.prepend(el);
}

async function fetchSemantic() {
  const res = await fetch("/semantic_map");
  const j = await res.json();
  semanticPre.textContent = JSON.stringify(j, null, 2);
}

function showAnnotations(list) {
  annotationsDiv.innerHTML = "";
  if (!list || list.length === 0) {
    annotationsDiv.innerHTML = "<div class='notice'>No text found</div>";
    return;
  }
  list.forEach(a => {
    const el = document.createElement("div");
    el.className = "annotation";
    el.innerHTML = `
      <div><strong>Detected:</strong> ${a.orig_text} (conf ${a.conf.toFixed(2)})</div>
      <div><strong>Corrected:</strong> ${a.corrected}</div>
      <div><strong>RAG Meaning:</strong> ${a.meaning || '—'}</div>
      <div><strong>Distance:</strong> ${a.distance?.toFixed(3) || '—'}</div>
    `;
    annotationsDiv.appendChild(el);
  });
}

// --------------------------------------------------
// 🔥 MAIN ANALYZE BUTTON (supports URL + File Upload)
// --------------------------------------------------
analyzeBtn.addEventListener("click", async () => {
  const url = imageUrlInput.value.trim();
  const file = fileInput.files[0];

  let formData = new FormData();

  if (file) {
    formData.append("file", file);
    log("📤 Uploading local image...");
  } 
  else if (url !== "") {
    formData.append("url", url);
    log(`🌐 Sending URL for analysis: ${url}`);
  } 
  else {
    return log("⚠ Please upload a file or enter a URL first.");
  }

  analyzeBtn.disabled = true;

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    showAnnotations(data.annotations || []);
    log(`✅ Analysis complete — ${data.annotations?.length || 0} annotations found`);

    await fetchSemantic();
  } 
  catch (err) {
    log("❌ Error: " + err.message);
  } 
  finally {
    analyzeBtn.disabled = false;
  }
});

// --------------------------------------------------
// SAMPLE BUTTON
// --------------------------------------------------
sampleBtn.addEventListener("click", () => {
  imageUrlInput.value = "https://upload.wikimedia.org/wikipedia/commons/4/4f/Exit_sign.svg";
  fileInput.value = ""; // clear file if sample is used
  log("📌 Sample image selected.");
});
