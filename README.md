# 🛒 Django E-Commerce API

A fully functional E-Commerce backend built using Django and Django REST Framework.  
Features include user authentication (JWT), product and category management, cart operations, order placement, admin-only controls, Redis caching, pagination, filtering, and email notifications.

---

## 📂 Project Structure

```bash
E_commerce/
├── users/              # User management (Register, Login, JWT, Profile)
├── products/           # Product and Category CRUD
├── orders/             # Cart and Orders
├── templates/          # Email templates (HTML)
├── utils/              # Email sending helpers
├── postman/            # Postman Collection
├── media/              # Uploaded media files
├── .env                # environment variables
├── requirements.txt    # Python dependencies
└── README.md           # You're here
```

---

## 🚀 Features

- JWT Authentication
- Role-based access (admin vs user)
- Product + Category CRUD (admin only)
- Add to Cart / Update Quantity / Remove Item
- Place Order
- Order History (for user)
- Order Management (for admin)
- Redis Caching for products & categories
- Pagination + Filtering on large data
- Email Notifications for:
  - OTP Verification
  - Order Confirmation
  - Order Status Updates

---

## 🧱 Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default)
- Redis (for caching)
- Django Channels (optional for WebSocket support)
- HTML email templates

---

## 📥 Clone the Repository

```bash
git clone https://github.com/roshan-sk/ECommerce-App.git
cd ECommerce-App
```

---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Rename `.env` to `.env` and update:

```env
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

---

### 4. Run Redis Server

Make sure Redis is running on port 6379.

---

### 5. Apply Migrations & Seed Data

```bash
python manage.py makemigrations
python manage.py migrate

# Optional: create superuser
python manage.py createsuperuser

# Seed categories and products
To seed GoTo products/management/commands/seed_products.py uncomment the code
run in the terminal or bash python manage.py seed_products
```

---

### 6. Run Server

```bash
python manage.py runserver
```

📍 App runs at: http://127.0.0.1:8000/

---

## 🧪 Testing with Postman

### Import Collection:

- Open Postman
- Click **Import**
- Load: `postman/Ecommerce.postman_collection.json`

---

## 🔒 Authentication

- Use `/api/auth/register/` and `/api/auth/login/` to obtain JWT tokens.
- Add this in your request headers:

```
Authorization: Bearer <your-token>
```

---

## 📦 API Endpoints

| Method | Endpoint                    | Description                        |
|--------|-----------------------------|------------------------------------|
| POST   | /api/auth/register/         | Register user                      |
| POST   | /api/auth/login/            | Login & get JWT                    |
| GET    | /api/products/              | List products (paginated)         |
| POST   | /api/products/              | Create product (admin)            |
| GET    | /api/categories/            | List categories (cached)          |
| POST   | /api/cart/add/<id>/         | Add product to cart               |
| PUT    | /api/cart/update/<id>/      | Update product quantity           |
| GET    | /api/cart/                  | Get cart items                    |
| POST   | /api/orders/                | Place an order                    |
| GET    | /api/orders/history/        | Get user’s order history          |
| GET    | /api/orders/admin/          | Admin: all orders                 |
| PUT    | /api/orders/update/<id>/    | Admin: update order status        |
| GET    | /api/orders/<id>/           | Get order details                 |

---

## 📧 Email Notifications

Sent for:
- OTP Verification
- Resend OTP
- Order Placed
- Order Status Changed

Email HTML templates are located in the `/templates/` folder.

---

## 💾 Redis Caching

Used for:
- Product List
- Category List

Cache timeout: 1 hour  
Cache is invalidated on create/update/delete.

---

## 🛠 Future Improvements

- PostgreSQL integration
- Admin dashboard (frontend)
- WebSocket support for real-time order tracking
- Razorpay/Stripe payment integration

---

## 📬 Contact

Built with ❤️ by ROSHAN SHAIK
email : roshansk032@gmail.com
