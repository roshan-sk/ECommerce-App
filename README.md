🛒 E-Commerce API
This is a Django Rest Framework (DRF)-based backend API for an E-Commerce application. It supports features like user authentication, product management, cart, orders, filtering, pagination, caching (Redis), and email notifications.

📁 Base URL
http://localhost:8000/


🔐 Authentication
JWT-based authentication.

Login and signup return access and refresh tokens.

Add the token to the Authorization header for protected routes:
Authorization: Bearer <your_token>

📦 API Endpoints (Grouped)
🔑 Auth APIs

Method	Endpoint	                               Description
POST	/api/auth/signup/	                       Register a new user
POST	/api/auth/signin/	                       Login and get JWT tokens
POST	/api/auth/forgot-password/                 Send password reset email
PUT	    /api/auth/reset-password/<uidb64>/<token>/ Reset password with token
GET	    /api/auth/profile/	                       Get logged-in user profile

👥 Admin APIs
Method	Endpoint	                               Description
GET	    /api/users/all/	                           Get all users (admin only) with filtering & pagination
GET	    /api/orders/all/	                       Get all orders (admin only) with filtering & pagination
PUT	    /api/orders/update-status/<order_id>/	   Update order status (admin only)

🛍️ Category APIs
Method	Endpoint	           Description
GET	    /api/categories/	   List all categories (cached)
POST	/api/categories/	   Create category (admin only)
PUT	    /api/categories/<id>/  Update category (admin only)
DELETE	/api/categories/<id>/  Delete category (admin only)

📦 Product APIs
Method	Endpoint	          Description
GET	    /api/products/	      List all products (cached, paginated, filters supported)
POST	/api/products/	      Create product (admin only)
PUT	    /api/products/<id>/	  Update product (admin only)
DELETE	/api/products/<id>/	  Delete product (admin only)

🔎 Product filters:

?category=<id>

?price_min=100&price_max=500

?in_stock=true

🛒 Cart APIs
Method	Endpoint	                  Description
GET	   /api/cart/	                  Get current user's cart (paginated)
POST   /api/cart/add/<product_id>/	  Add a product to the cart
PUT	   /api/cart/update/<product_id>/ Update product quantity in cart

📑 Order APIs
Method	Endpoint	             Description
POST	/api/orders/place/	     Place an order (from cart)
GET	    /api/orders/history/	 Get your order history (paginated & filter by status)
GET	    /api/orders/<order_id>/	 Get a single order detail (own or admin)

🔎 Filtering & Pagination
Pagination query param: ?page=1

Product filters:

?category=<category_id>

?price_min=100&price_max=500

?in_stock=true

Order filters:

?status=pending,shipped

🧠 Caching (Redis)
Redis is used to cache:

GET /api/products/

GET /api/categories/

Timeout: 1 hour

Cache is invalidated on product/category create/update/delete

📧 Email Notifications
Emails are sent via Django’s send_mail for:

OTP verification

Order confirmation

Order status update

Templates are located in:
utils/email_templates/
🛠️ Setup & Installation
Clone the repo

Install dependencies:

nginx
Copy
Edit
pip install -r requirements.txt
Create .env and configure DB, Redis, and Email settings

Run migrations:

python manage.py migrate
Start Redis server

Run Django server:
python manage.py runserver