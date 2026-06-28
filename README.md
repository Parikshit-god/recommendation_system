# 🎬 Movie Recommendation System

A Content-Based Movie Recommendation System that suggests movies similar to the one selected by the user. The application is built using Python, Machine Learning, and Streamlit, and is deployed for interactive use.

---

## 🚀 Live Demo

🔗 **Live Application:**  
(Add your Streamlit URL here)

---

## 📌 Features

- Search and select a movie from the dataset
- Get Top 5 similar movie recommendations
- Fast recommendations using a precomputed similarity matrix
- Clean and interactive Streamlit interface
- Machine Learning powered recommendation engine

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Pickle
- Git & GitHub
- Git LFS (for large model files)

---

## 📂 Project Structure

```
recommendation-system/
│
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
├── .gitattributes
├── README.md
└── assets/
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Parikshit-god/recommendation_system.git
```

Move into the project

```bash
cd recommendation_system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. Load the processed movie dataset.
2. Load the precomputed cosine similarity matrix.
3. User selects a movie.
4. Find the selected movie's index.
5. Retrieve similarity scores.
6. Sort movies by similarity.
7. Display the Top 5 recommendations.

---

## 📊 Machine Learning Workflow

Dataset
⬇️

Data Cleaning
⬇️

Feature Engineering
⬇️

Vectorization
⬇️

Cosine Similarity
⬇️

Similarity Matrix (.pkl)
⬇️

---

## 📈 Future Improvements

- Movie posters using TMDB API
- Search autocomplete
- Genre-based filtering
- IMDb ratings integration
- User authentication
- Hybrid recommendation system
- Personalized recommendations

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Parikshit Singh**

Computer Science Engineering Student

GitHub: https://github.com/Parikshit-god
