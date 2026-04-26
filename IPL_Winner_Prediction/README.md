# 🏏 IPL Match Winner Predictor

> ⚠️ **Note:** This project is currently a work in progress. I am actively learning Machine Learning and some features may have bugs or errors. Contributions and suggestions are welcome!

---

## 📌 About the Project

This is an end-to-end Machine Learning project that predicts the **winner of an IPL match** based on pre-match information such as the teams playing, venue, toss result, and season.

The project is built as part of my Machine Learning learning journey — covering the full pipeline from raw data to a deployed web application.

---

## 🚀 Features

- Predicts IPL match winner based on pre-match inputs
- Trained on **IPL ball-by-ball data from 2007 to 2026** (1169 matches)
- Compared multiple ML models — Logistic Regression, Random Forest, XGBoost
- Interactive web app built with **Streamlit**

---

## 🧠 ML Pipeline

1. **Data Collection** — IPL ball-by-ball dataset (283,678 rows)
2. **Data Preprocessing** — Aggregated ball-by-ball data to match-level (1 row per match)
3. **Feature Engineering** — Extracted team1, team2, fixed duplicate team names across seasons
4. **Label Encoding** — Encoded all categorical features using sklearn LabelEncoder
5. **Model Training** — Trained and compared 3 models
6. **Deployment** — Streamlit web app

---

## 📊 Model Comparison

| Model | Accuracy |
|---|---|
| Logistic Regression | 24% |
| XGBoost | 47% |
| **Random Forest** | **49% ✅ Best** |

> Note: Cricket match prediction is inherently uncertain. Even expert analysts achieve ~60-65% accuracy. Random guessing with 13 teams = 7.7%, so 49% is ~6x better than random.

---

## 🛠️ Tech Stack

- **Python 3.13**
- **Pandas, NumPy** — Data processing
- **Scikit-learn** — ML models, Label Encoding, train/test split
- **XGBoost** — Gradient boosting model
- **Streamlit** — Web app frontend
- **Pickle** — Model serialization

---

## 📁 Project Structure

```
IPL_Winner_Prediction/
│
├── data/
│   └── training_data/
│       └── IPL.csv
│
├── model/
│   ├── rf_model.pkl
│   └── label_encoders.pkl
│
├── notebooks/
│   └── notebook_1.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/IPL_Winner_Prediction.git
cd IPL_Winner_Prediction

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🎯 Input Features

| Feature | Description |
|---|---|
| Team 1 | First batting team |
| Team 2 | Second batting team |
| Venue | Stadium where match is played |
| Toss Winner | Team that won the toss |
| Toss Decision | Bat or Field |
| Season | Year of the IPL season |

---

## ⚠️ Known Issues & Work in Progress

- [ ] Streamlit app has a path/environment issue being debugged
- [ ] Model accuracy can be improved with hyperparameter tuning
- [ ] Class imbalance exists (some teams have fewer matches in training data)
- [ ] Plan to add win probability % instead of just predicted winner
- [ ] Plan to add a second pipeline for **live match win probability prediction**

---

## 📈 Future Improvements

- Hyperparameter tuning with GridSearchCV
- Add live match situation inputs (current over, runs, wickets)
- Deploy on Hugging Face Spaces or Streamlit Cloud
- Add visual charts showing team win history

---

## 🙋 About

I am currently learning Machine Learning and building this project to strengthen my understanding of end-to-end ML pipelines. This project covers data preprocessing, feature engineering, model training, and deployment.

> This is a learning project — feedback and suggestions are always welcome!

---

## 📜 License

This project is for educational purposes only.
IPL data sourced from public datasets on Kaggle.