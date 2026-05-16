# 🇮🇳 YojanaSetu AI

An AI-powered government scheme recommendation system built using Streamlit, Sentence Transformers, and Google Gemini AI.

YojanaSetu AI helps users discover relevant Indian government welfare schemes based on their needs using semantic search and AI-generated explanations.

---

# 🚀 Features

- 🔎 Smart scheme recommendation system
- 🤖 AI-generated scheme explanations using Gemini AI
- 🎤 Voice input support
- 🌐 Multi-language explanation support
- 📚 Semantic search using Sentence Transformers
- 🧠 Embedding-based retrieval system
- 🖥️ Clean Streamlit UI

---

# 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Sentence Transformers
- Pandas
- Scikit-learn

---

# 📂 Project Structure

```bash
YojanaSetu-AI/
│
├── app.py
├── logic.py
├── check_models.py
├── updated_data.csv
├── scheme_embeddings.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/yojanasetu-ai.git
```

## Navigate into the project folder

```bash
cd yojanasetu-ai
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setup Gemini API Key

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 🧠 How It Works

1. User enters a query or uses voice input
2. Sentence Transformer generates embeddings
3. Semantic similarity search finds matching schemes
4. Gemini AI explains schemes in simple language
5. Results are displayed in Streamlit UI

---

# 📸 Screenshots

(Add your screenshots here later)

---

# 🔮 Future Improvements

- Better multilingual support
- Mobile responsive UI
- Deployment on Streamlit Cloud
- Scheme eligibility prediction
- User authentication
- Real-time government API integration

---

# 👨‍💻 Author

Prakhar Sharma

---

# 📜 License

This project is licensed under the MIT License.