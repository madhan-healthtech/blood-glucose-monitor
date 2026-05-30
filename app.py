import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib
matplotlib.use('Agg')  # important — stops matplotlib from opening a window
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import base64
import io
from collections import Counter
from flask import Flask, render_template, request, redirect, session, url_for
import json, os
from datetime import date
from dotenv import load_dotenv
load_dotenv()
print("SECRET KEY:",os.getenv("SECRET_KEY"))
import os

app = Flask(__name__) 
app.secret_key = os.getenv("SECRET_KEY")
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DOCTOR_EMAIL   = os.getenv("DOCTOR_EMAIL")

def send_alert_email(patient_name, patient_email, glucose, status, meal, date):
    try:
        subject = f"🚨 Glucose Alert — {patient_name} ({status.upper()})"

        body = f"""
        <html>
        <body style="font-family:Arial,sans-serif;background:#f8fafc;padding:20px;">
        <div style="max-width:500px;margin:auto;background:white;border-radius:12px;overflow:hidden;">

          <div style="background:#1a3557;padding:24px;text-align:center;">
            <h1 style="color:white;margin:0;font-size:20px;">🩸 Blood Glucose Alert</h1>
          </div>

          <div style="padding:24px;">
            <p style="color:#334155;font-size:14px;">A patient reading requires your attention:</p>

            <table style="width:100%;border-collapse:collapse;margin-top:16px;">
              <tr style="background:#f1f5f9;">
                <td style="padding:10px 14px;font-size:13px;color:#64748b;">Patient</td>
                <td style="padding:10px 14px;font-size:13px;font-weight:bold;">{patient_name}</td>
              </tr>
              <tr>
                <td style="padding:10px 14px;font-size:13px;color:#64748b;">Email</td>
                <td style="padding:10px 14px;font-size:13px;">{patient_email}</td>
              </tr>
              <tr style="background:#f1f5f9;">
                <td style="padding:10px 14px;font-size:13px;color:#64748b;">Date</td>
                <td style="padding:10px 14px;font-size:13px;">{date}</td>
              </tr>
              <tr>
                <td style="padding:10px 14px;font-size:13px;color:#64748b;">Meal Type</td>
                <td style="padding:10px 14px;font-size:13px;">{meal}</td>
              </tr>
              <tr style="background:#f1f5f9;">
                <td style="padding:10px 14px;font-size:13px;color:#64748b;">Glucose Level</td>
                <td style="padding:10px 14px;font-size:20px;font-weight:bold;color:#ef4444;">{glucose} mg/dL</td>
              </tr>
              <tr>
                <td style="padding:10px 14px;font-size:13px;color:#64748b;">Status</td>
                <td style="padding:10px 14px;font-size:14px;font-weight:bold;color:#ef4444;">{status.upper()}</td>
              </tr>
            </table>

            <div style="margin-top:20px;padding:14px;background:#fef2f2;border-radius:8px;border-left:4px solid #ef4444;">
              <p style="color:#991b1b;font-size:13px;margin:0;">
                ⚠️ This patient's glucose level is in the <b>{status}</b> range.
                Please follow up with them as soon as possible.
              </p>
            </div>

            <p style="color:#94a3b8;font-size:11px;margin-top:20px;text-align:center;">
              This alert was sent automatically by Blood Glucose Monitor.
              For informational purposes only.
            </p>
          </div>

        </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = DOCTOR_EMAIL
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, DOCTOR_EMAIL, msg.as_string())

        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

USERS_FILE = "users.json"
DATA_FILE  = "data.json"

# ── File helpers ──────────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        data = {"doctor@health.com": {"password": "doctor123", "role": "doctor", "name": "Dr. Smith"}}
        save_users(data)
        return data
    return json.load(open(USERS_FILE))

def save_users(data):
    json.dump(data, open(USERS_FILE, "w"), indent=2)

def load_data():
    if not os.path.exists(DATA_FILE): return []
    return json.load(open(DATA_FILE))

def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=2)

def classify(g, meal):
    ranges = {
        "Fasting":         {"low":(0,70),"normal":(70,100),"prediabetic":(100,126),"diabetic":(126,9999)},
        "Post-Meal (2hr)": {"low":(0,70),"normal":(70,140),"prediabetic":(140,200),"diabetic":(200,9999)},
        "Random":          {"low":(0,70),"normal":(70,140),"prediabetic":(140,200),"diabetic":(200,9999)},
    }
    r = ranges.get(meal, ranges["Random"])
    for status,(lo,hi) in r.items():
        if lo <= g < hi: return status
    return "diabetic"

# ── Routes ────────────────────────────────────
@app.route("/")
def home():
    if "user" in session: return redirect("/dashboard")
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        pwd   = request.form["password"]
        users = load_users()
        if email not in users:
            error = "Email not found. Please register."
        elif users[email]["password"] != pwd:
            error = "Incorrect password."
        else:
            session["user"] = email
            session["name"] = users[email]["name"]
            session["role"] = users[email]["role"]
            return redirect("/dashboard")
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET","POST"])
def register():
    error = ""
    if request.method == "POST":
        name  = request.form["name"]
        email = request.form["email"]
        pwd   = request.form["password"]
        users = load_users()
        if email in users:
            error = "Email already registered."
        else:
            users[email] = {"password":pwd,"role":"patient","name":name}
            save_users(users)
            return redirect("/login")
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect("/login")
    if session["role"] == "doctor": return redirect("/doctor")
    readings = [r for r in load_data() if r["username"] == session["user"]]
    return render_template("dashboard.html", readings=readings[-10:][::-1], today=date.today().isoformat())

@app.route("/add", methods=["POST"])
def add():
    if "user" not in session: return redirect("/login")
    g      = float(request.form["glucose"])
    meal   = request.form["meal"]
    dt     = request.form["date"]
    status = classify(g, meal)
    data   = load_data()
    data.append({"username":session["user"],"date":dt,"meal":meal,"glucose":g,"status":status})
    save_data(data)

    # Send alert if reading is dangerous
    if status in ("diabetic", "prediabetic", "low"):
        send_alert_email(
            patient_name  = session["name"],
            patient_email = session["user"],
            glucose       = g,
            status        = status,
            meal          = meal,
            date          = dt
        )

    return redirect("/dashboard")

@app.route("/doctor")
def doctor():
    if "user" not in session or session["role"] != "doctor":
        return redirect("/login")
    data = load_data()
    return render_template("doctor.html", readings=data[::-1])

@app.route("/stats")
def stats():
    if "user" not in session: return redirect("/login")
    readings = [r for r in load_data() if r["username"] == session["user"]]

    if len(readings) < 2:
        return render_template("stats.html", 
                               graph=None, 
                               risk_score=-1,
                               trend=None,
                               recs=["Add at least 2 readings to see stats."],
                               stats=None)

    glucoses = [r["glucose"] for r in readings]
    statuses = [r["status"]  for r in readings]
    dates    = [r["date"]    for r in readings]

    # ── Stats ──────────────────────────────
    sc = Counter(statuses)
    stats_data = {
        "total":       len(glucoses),
        "avg":         round(sum(glucoses)/len(glucoses), 1),
        "max":         max(glucoses),
        "min":         min(glucoses),
        "normal":      sc.get("normal", 0),
        "prediabetic": sc.get("prediabetic", 0),
        "diabetic":    sc.get("diabetic", 0),
        "low":         sc.get("low", 0),
    }

    # ── Graph ──────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#1e293b")
    ax.set_facecolor("#0f172a")

    color_map = {"normal":"#22c55e","prediabetic":"#f59e0b","diabetic":"#ef4444","low":"#3b82f6"}
    pt_colors = [color_map.get(s,"#94a3b8") for s in statuses]

    ax.plot(dates, glucoses, color="#3b82f6", linewidth=2, zorder=2)
    ax.scatter(dates, glucoses, c=pt_colors, s=80, zorder=3)

    ax.axhspan(0,   70,  alpha=0.07, color="#3b82f6")
    ax.axhspan(70,  100, alpha=0.07, color="#22c55e")
    ax.axhspan(100, 126, alpha=0.07, color="#f59e0b")
    ax.axhspan(126, 400, alpha=0.07, color="#ef4444")

    ax.tick_params(colors="white")
    ax.set_xlabel("Date", color="#94a3b8")
    ax.set_ylabel("Glucose (mg/dL)", color="#94a3b8")
    ax.set_title("Glucose Trend", color="white", fontsize=13)
    ax.grid(color="#334155", linestyle="--", alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor("#334155")
    plt.xticks(rotation=40, color="white", fontsize=8)
    plt.yticks(color="white")
    plt.tight_layout()

    # Convert graph to base64 image for HTML
    buf = io.BytesIO()
    plt.savefig(buf, format="png", facecolor="#1e293b")
    buf.seek(0)
    graph_b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    # ── AI Risk Score ──────────────────────
    n = len(glucoses)
    bad = sum(1 for s in statuses if s in ("prediabetic","diabetic"))
    status_score = (bad / n) * 50

    x   = np.arange(n).reshape(-1,1)
    y   = np.array(glucoses)
    reg = LinearRegression().fit(x, y)
    slope = reg.coef_[0]
    trend_score = min(max(slope * 5, 0), 30)
    volatility_score = min((np.std(y) / 10) * 5, 20)
    risk_score = min(int(status_score + trend_score + volatility_score), 100)

    # Trend
    next_idx  = np.array([n, n+1, n+2]).reshape(-1,1)
    next_pred = reg.predict(next_idx)
    if slope > 1.5:
        direction, icon, color = "RISING",    "↑", "#ef4444"
    elif slope < -1.5:
        direction, icon, color = "IMPROVING", "↓", "#22c55e"
    else:
        direction, icon, color = "STABLE",    "→", "#f59e0b"

    trend = {
        "direction":  direction,
        "icon":       icon,
        "color":      color,
        "slope":      round(slope, 2),
        "next_preds": [round(p,1) for p in next_pred]
    }

    # Recommendations
    recs = []
    if risk_score < 25:
        recs.append("✅ Your glucose control is good. Keep your current diet and exercise.")
    elif risk_score < 50:
        recs.append("⚠️ Moderate risk. Reduce sugar and refined carbs.")
        recs.append("⚠️ Aim for 30 minutes of physical activity daily.")
    elif risk_score < 75:
        recs.append("🚨 High risk. Schedule a doctor appointment soon.")
        recs.append("🚨 Avoid sugary drinks, white rice, and processed foods.")
    else:
        recs.append("🔴 Critical risk. See a doctor immediately.")
        recs.append("🔴 Do not skip meals — maintain strict meal timing.")

    if direction == "RISING":
        recs.append("📈 Trend is rising — your readings are getting worse over time.")
    elif direction == "IMPROVING":
        recs.append("📉 Trend is improving — your lifestyle changes are working!")
    else:
        recs.append("📊 Trend is stable — consistent but watch for increases.")

    return render_template("stats.html",
                           graph=graph_b64,
                           risk_score=risk_score,
                           trend=trend,
                           recs=recs,
                           stats=stats_data)
if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")

