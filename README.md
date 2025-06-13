# ❤️ HeartHive - Fundraising Web App

HeartHive is a Django-based web application that allows users to create, manage, and donate to fundraising campaigns. It supports role-based authentication for **Donors** and **Fundraisers**, campaign approvals by **Admins**, and secure payment processing with **Stripe**.

> 🐳 Fully Dockerized for easy development and deployment!

---

## 🚀 Features

- 👥 User Authentication (Sign Up / Login / Logout)
- 🧑‍💼 Role-based system (Donor, Fundraiser, Admin)
- 📢 Campaign Creation & Management
- 💳 Stripe Payment Integration
- 📊 Fundraiser & Donor Dashboards
- 📧 Email & In-App Notifications
- 🛡️ Admin Panel with Campaign Approval
- 📦 Dockerized Setup (for local development)

---

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (Development)
- **Payments**: Stripe API
- **Containerization**: Docker, Docker Compose

---


### 1. Clone the Repo

```bash
git clone https://github.com/kashifnoor1/HeartHive.git
cd HeartHive

python -m venv venv
source venv/bin/activate  # for Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


## 🐳 Docker Setup

docker-compose up --build





