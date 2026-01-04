<h1 align="center">🚀 LP-SLAM-TECC</h1>

<h3 align="center">
Language-Perception SLAM with <br>
Text Error Correction (TECC) + RAG + LLM
</h3>

<p align="center">
<b>Semantic SLAM system that understands text in the environment</b>
</p>

<p align="center">
<a href="https://github.com/ysujith728/LP-SLAM-TECC">GitHub Repository</a>
</p>

<hr>

<h2>📌 Abstract</h2>

<p>
Traditional SLAM systems focus primarily on geometry and ignore semantic
information present in the environment. <b>LP-SLAM-TECC</b> enhances SLAM by
integrating scene text understanding into the mapping process.
</p>

<p>
The system detects text from images, corrects OCR errors using
<b>Text Error Correction & Classification (TECC)</b>, enriches understanding
using <b>Retrieval-Augmented Generation (RAG)</b>, and stores results in a
semantic map. This enables robots to understand signs like <i>EXIT</i>,
room numbers, and labels in a human-like way.
</p>

<hr>

<h2>🧠 System Architecture</h2>

<pre>
Camera / Image
      ↓
OCR (EasyOCR)
      ↓
TECC (Correction + Classification)
      ↓
RAG (FAISS + Knowledge Base)
      ↓
Semantic Map
</pre>

<hr>

<h2>✨ Key Features</h2>

<ul>
  <li>🔍 Robust OCR using EasyOCR</li>
  <li>🛠 Text Error Correction (handles OCR noise)</li>
  <li>🧠 Semantic Classification using LLM-ready TECC</li>
  <li>📚 Retrieval-Augmented Generation (RAG)</li>
  <li>🗺 In-memory Semantic Map for SLAM</li>
  <li>🌐 Interactive Web UI (FastAPI + HTML/CSS/JS)</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>

<pre>
LP-SLAM-TECC/
├── app.py                  # FastAPI backend
├── requirements.txt
├── knowledge_base/
│   └── rag_data.jsonl
├── slam_engine/
│   ├── text_detection.py
│   ├── tecc_model.py
│   ├── rag_engine.py
│   └── tecc_db.json
├── static/
│   ├── app.js
│   └── ui.css
├── templates/
│   └── index.html
├── build_rag_index.py
├── rag_index.faiss
├── test_pipeline.py
└── README.md
</pre>

<hr>

<h2>⚙️ Installation & Setup</h2>

<h3>1️⃣ Clone the Repository</h3>

<pre>
git clone https://github.com/ysujith728/LP-SLAM-TECC.git
cd LP-SLAM-TECC
</pre>

<h3>2️⃣ Create Virtual Environment</h3>

<pre>
python -m venv venv
venv\Scripts\activate
</pre>

<h3>3️⃣ Install Dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<hr>

<h2>🚀 Running the Project</h2>

<pre>
uvicorn app:app --reload
</pre>

<p>
Open your browser and go to:
<b>http://127.0.0.1:8000</b>
</p>

<hr>

<h2>🧪 Example Output</h2>

<p>
Input image containing text:
</p>

<pre>
EXIT
</pre>

<p>
Semantic Map Output:
</p>

<pre>
{
  "text": "EXIT",
  "label": "exit_sign",
  "meaning": "Indicates an emergency exit used for evacuation."
}
</pre>

<hr>

<h2>🗺 Semantic Mapping</h2>

<p>
The semantic map stores:
</p>

<ul>
  <li>Detected text</li>
  <li>Corrected text</li>
  <li>Semantic label</li>
  <li>Contextual meaning</li>
</ul>

<p>
This allows the SLAM system to reason about the environment instead of
just mapping walls.
</p>

<hr>

<h2>🎯 Applications</h2>

<ul>
  <li>🤖 Indoor robot navigation</li>
  <li>🏢 Smart buildings</li>
  <li>♿ Assistive navigation systems</li>
  <li>📍 Human-aware SLAM research</li>
</ul>

<hr>

<h2>🔬 Research Contribution</h2>

<ul>
  <li>Introduces text as a first-class SLAM landmark</li>
  <li>Demonstrates TECC + RAG synergy</li>
  <li>Reduces OCR misclassification errors</li>
  <li>Bridges vision, language, and mapping</li>
</ul>

<hr>

<h2>👨‍💻 Author</h2>

<p>
<b>Sujith Y</b><br>
B.Tech CSE<br>
GitHub: <a href="https://github.com/ysujith728">ysujith728</a>
</p>

<hr>

<h2>📜 License</h2>

<p>
This project is intended for academic and research purposes.
</p>

<hr>

<p align="center">
⭐ If you like this project, consider starring the repository ⭐
</p>
