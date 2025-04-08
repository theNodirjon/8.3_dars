# Django OTP Authentication API

Bu loyiha **Django** va **Twilio** orqali **OTP (One Time Password) autentifikatsiyasi** ni amalga oshiradi. Foydalanuvchilar telefon raqami orqali ro'yxatdan o'tishi va tizimga kirishi uchun **SMS orqali OTP kod yuboriladi**.

---

## 📌 Loyiha imkoniyatlari
- 📞 Telefon raqam orqali ro'yxatdan o'tish
- 🔑 OTP kod yuborish (Twilio orqali SMS)
- ✅ OTP kodni tasdiqlash
- 🔐 Maxsus foydalanuvchi modeli (Custom User Model)

---

## 🚀 O'rnatish

### 1. **Loyihani klonlash**
```bash
git clone https://github.com/theNodirjon/8.3_dars.git
cd otp_project
```

### 2. **Virtual environment yaratish va faollashtirish**
```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux
type venv\Scripts\activate  # Windows
```

### 3. **Talab qilinadigan kutubxonalarni o'rnatish**
```bash
pip install -r requirements.txt
```

### 4. **Django sozlamalarini yangilash**
`settings.py` faylida quyidagi sozlamalarni kiriting:

```python
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'otp_app',  # OTP Authentication ilovasi
]
```

### 5. **Twilio hisobini sozlash**
`settings.py` fayliga quyidagilarni qo'shing:
```python
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+998**1234567"  # Twilio dan olingan raqam
```

### 6. **Ma'lumotlar bazasini yaratish**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. **Superuser yaratish (majburiy emas)**
```bash
python manage.py createsuperuser
```

### 8. **Serverni ishga tushirish**
```bash
python manage.py runserver
```

---

## 📡 API-lar ro'yxati

### 🔹 1. **OTP Yuborish**
**Endpoint:** `POST /api/send-otp/`

**Request Body:**
```json
{
    "phone": "+998901234567"
}
```

**Response:**
```json
{
    "message": "OTP sent successfully"
}
```

---

### 🔹 2. **OTP Tasdiqlash**
**Endpoint:** `POST /api/verify-otp/`

**Request Body:**
```json
{
    "phone": "+998901234567",
    "otp": "123456"
}
```

**Response:**
```json
{
    "message": "OTP verified successfully",
    "token": "your-auth-token"
}
```

---

## 📜 Muallif
- 👤 Maxsudov Nodirjon 
- 📧 maxsudovnodir2@gmail.com
- 🔗 Github: https://github.com/theNodirjon

**© 2025**

