# 🏡 Ames House Price Predictor

> A full-stack ML application that predicts house sale prices using the Ames Housing Dataset. Built with **FastAPI** backend and a premium **dark-themed HTML/CSS/JS** frontend.

---

## 📁 Project Structure

```
House_Prediction_Using_Amens_Housing_Dataset/
│
├── data/
│   └── AmesHousing.csv              ← Raw dataset (2,930 homes, 82 features)
│
├── notebooks/
│   ├── Project_2.ipynb              ← EDA, preprocessing, model training
│   └── Linkedin/
│       └── Project_2.ipynb          ← LinkedIn showcase version
│
├── models/
│   ├── ames_housing_model.pkl       ← Trained sklearn Pipeline
│   └── model_meta.json             ← Categorical feature options for frontend
│
├── backend/
│   ├── main.py                      ← FastAPI application
│   └── requirements.txt
│
├── frontend/
│   ├── index.html                   ← Main UI page
│   ├── style.css                    ← Premium dark theme styles
│   └── app.js                       ← API integration & UX logic
│
└── README.md
```

---

## 🤖 Model Details

| Property         | Value                                    |
|------------------|------------------------------------------|
| Algorithm        | Linear Regression                        |
| Training samples | 2,927 homes                              |
| Test R² Score    | **0.8544**                               |
| Features used    | 10 (6 numeric + 4 categorical)           |
| Preprocessing    | SimpleImputer + StandardScaler + OHE     |

### Features
**Numeric:** Year Built, Garage Cars, 1st Floor SF, Above-Grade Living Area, Full Bathrooms, Bedrooms Above Grade

**Categorical:** Neighborhood, Foundation, House Style, Building Type

---

## 🚀 Running the Application

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

- **Docs (Swagger):** `http://localhost:8000/docs`
- **Health check:** `http://localhost:8000/health`
- **Prediction:** `POST http://localhost:8000/predict`

### 3. Open the Frontend

Simply open `frontend/index.html` in your browser. No build step needed!

If the backend is running on port 8000, predictions will work immediately.

---

## 📡 API Reference

### `GET /health`
Returns API status.

### `GET /meta`
Returns valid categorical values for dropdowns.

### `POST /predict`
```json
{
  "year_built": 2005,
  "gr_liv_area": 1800,
  "first_flr_sf": 950,
  "garage_cars": 2,
  "full_bath": 2,
  "bedroom_abvgr": 3,
  "neighborhood": "NAmes",
  "foundation": "PConc",
  "house_style": "2Story",
  "bldg_type": "1Fam"
}
```

Response:
```json
{
  "predicted_price": 187432.5,
  "formatted_price": "$187,433",
  "model_r2": 0.8544
}
```

---

## 🎨 Frontend Preview

- **Dark glassmorphism UI** with gradient accents
- **Animated background particles**
- **Live API status badge**
- **Animated price bar** showing relative value ($50k → $800k+)
- **Sticky result panel** alongside the form
- **Input validation** with visual feedback

---

## 📊 Dataset

The [Ames Housing Dataset](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) contains detailed information about residential homes in Ames, Iowa, collected between 2006–2010. It has 82 features describing virtually every aspect of residential homes.
