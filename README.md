# 🩸 Blood Glucose Monitor

A clinical Blood Glucose Monitoring Web Application built with **Flask and Python**. Designed for patients and doctors to track, analyze, and manage blood glucose levels with AI-powered predictions and automated email alerts.

---

## 🌐 Live Demo
> Coming soon after deployment on Render

---

## 📸 Screenshots

> Login Page | Patient Dashboard | Stats & AI Prediction | Doctor Panel

---

## ✨ Features

### 👤 Patient
- Secure login and registration
- Log glucose readings with date and meal type (Fasting / Post-Meal / Random)
- Automatic medical classification — Normal, Pre-Diabetic, Diabetic, Low
- View reading history with color coded status badges
- Interactive glucose trend graph
- AI risk score (0–100) with trend prediction
- Predicted next 3 glucose readings using Linear Regression
- Personalized health recommendations
- BMI calculator with health category
- PDF health report generation

### 🩺 Doctor
- Separate doctor login
- View all patient readings in one table
- Automatic email alert when a patient's reading is dangerous
- Filter readings by status

---

## 🤖 AI Prediction Engine

The AI module uses **Linear Regression (scikit-learn)** to:

- Calculate a **Risk Score (0–100)** based on:
  - % of readings in diabetic/pre-diabetic range → up to 50 points
  - Trend direction (slope of readings over time) → up to 30 points
  - Volatility (standard deviation of readings) → up to 20 points

- Predict **trend direction**:
  - ↑ Rising — readings getting worse
  - ↓ Improving — readings getting better
  - → Stable — consistent pattern

- Predict **next 3 glucose readings** based on current trend

---

## 📊 Medical Reference Ranges (mg/dL)

| Type | Low | Normal | Pre-Diabetic | Diabetic |
|---|---|---|---|---|
| Fasting | < 70 | 70 – 99 | 100 – 125 | ≥ 126 |
| Post-Meal (2hr) | < 70 | 70 – 139 | 140 – 199 | ≥ 200 |
| Random | < 70 | 70 – 139 | 140 – 199 | ≥ 200 |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS |
| AI / ML | scikit-learn, NumPy |
| Graph | Matplotlib |
| PDF Generation | ReportLab |
| Data Storage | JSON |
| Email Alerts | smtplib, Gmail SMTP |
| Version Control | Git, GitHub |

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/madhan-healthtech/blood-glucose-monitor.git
cd blood-glucose-monitor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure email alerts

Open `app.py` and update these lines:
```python
EMAIL_SENDER   = "your_gmail@gmail.com"
EMAIL_PASSWORD = "your_app_password"
DOCTOR_EMAIL   = "doctor_email@gmail.com"
```

> To get an App Password: Google Account → Security → 2-Step Verification → App Passwords

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## 👥 Default Accounts

| Role | Email | Password |
|---|---|---|
| Doctor | doctor@health.com | doctor123 |
| Patient | Register via app | Your choice |

---

## 📁 Project Structure

```
blood-glucose-monitor/
│
├── app.py                  ← Main Flask application
├── requirements.txt        ← Python dependencies
├── README.md               ← Project documentation
│
└── templates/
    ├── login.html          ← Login page
    ├── register.html       ← Register page
    ├── dashboard.html      ← Patient dashboard
    ├── stats.html          ← Stats, graph & AI prediction
    └── doctor.html         ← Doctor panel
```

---

## 📈 Project Levels

| Level | Feature | Status |
|---|---|---|
| 1 | Desktop app with login, logging, graph, BMI | ✅ Complete |
| 2 | AI risk score and trend prediction | ✅ Complete |
| 3A | PDF health report generator | ✅ Complete |
| 3B | Flask web application | ✅ Complete |
| 3C | Email alerts for doctors | ✅ Complete |
| 4 | ML model with real diabetes dataset | 🔜 Coming soon |

---

## 🎓 About

Built by a **Madhan kumar    2nd year Biomedical Engineering student** as a practical project combining:
- Biomedical domain knowledge (glucose ranges, BMI, risk assessment)
- Python programming and web development
- AI and Machine Learning in healthcare
- Real world clinical application design

**Domain:** Biomedical + Python + AI in Healthcare

---

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**. It does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ If you found this project useful, please give it a star on GitHub!
