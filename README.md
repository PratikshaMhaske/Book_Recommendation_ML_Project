# 📚 Book Recommendation System

A machine learning project that recommends books using **Collaborative Filtering**.  
The system provides both **Item-Based** and **User-Based** recommendations with an interactive **Streamlit UI**.

---

## 🚀 Features

- 📖 Item-Based Book Recommendation
- 👤 User-Based Book Recommendation
- 🔍 Search/select book from dropdown
- 🎚️ Adjustable number of recommendations
- ⭐ Rating threshold control for user-based filtering
- 🖼️ Displays book title, author, and cover image
- 📊 EDA and data visualization included

---

## 🧠 Recommendation Techniques

### 1. Item-Based Collaborative Filtering
Recommends books similar to the selected book based on user rating patterns.

### 2. User-Based Collaborative Filtering
Finds users with similar reading behavior and recommends books liked by those similar users.

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Pickle

📊 Dataset

The project uses three datasets:

Books.csv
Users.csv
Ratings.csv

Main columns used:

User-ID
ISBN
Book-Rating
Book-Title
Book-Author
Image-URL-M

🔄 Project Workflow
Load datasets
Perform EDA
Handle missing values
Remove zero ratings
Merge books and ratings data
Filter active users
Filter popular books
Create user-item pivot table
Apply cosine similarity
Build item-based and user-based recommendation functions
Save model files using pickle
Build Streamlit UI

📌 Key Insights from EDA
Most ratings are between 7 and 10.
Dataset is positively biased because users mostly rate books they like.
Some authors dominate the dataset.
Young adults are the major user group.
Filtering active users and popular books improves recommendation quality.

🔮 Future Scope
Add content-based filtering
Add hybrid recommendation system
Improve UI design
Deploy on cloud platform
Add login-based personalized recommendations

---

## 📂 Project Structure

```text

Book_Recommendation_ML_Project/
│
├── Book_Recommend_app.py
├── Book_Recommendation_Main.ipynb
├── pt.pkl
├── books.pkl
├── similarity_scores.pkl
├── user_similarity.pkl
├── requirements.txt
└── README.md

Author

Er. Pratiksha Mhaske

LinkedIn: https://www.linkedin.com/in/pratiksha-mhaske-173643387

GitHub: https://github.com/PratikshaMhaske
