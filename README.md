# ecom_project

A Django REST Framework backend for a small ecommerce platform. It provides API endpoints for user accounts, product catalog management, carts, and order checkout. The project uses SQLite by default and issues JSON Web Tokens (JWTs) for API authentication.

## Contents

- [Features](#features)
- [Technology](#technology)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [Database migrations](#database-migrations)
- [Run the development server](#run-the-development-server)
- [API documentation and endpoints](#api-documentation-and-endpoints)
- [Typical API workflow](#typical-api-workflow)
- [Tests and useful commands](#tests-and-useful-commands)
- [Configuration and current limitations](#configuration-and-current-limitations)

## Features

- Custom user model with email-based login, registration, profile, password change, and JWT token endpoints.
- Product and category models, product detail and listing endpoints, and admin-only product changes.
- Per-user shopping carts with add, view, modify, and delete endpoints.
- Checkout that validates cart contents and stock, creates an order and order items, decrements stock, and clears the cart.
- Order history, order detail, admin order listing and status updates, and customer cancellation before shipment.
- Django admin, Django REST Framework filtering and pagination, and OpenAPI documentation through Swagger UI and ReDoc.

## Technology

- Python (use a version supported by the pinned Django release; Python 3.12 or newer is recommended)
- Django 6.1.2
- Django REST Framework
- Django REST Framework Simple JWT
- django-filter
- drf-spectacular
- SQLite (the default database)

Exact Python package versions are listed in [`requirements.txt`](requirements.txt).

## Project structure

```text
ecom_project/
├── apps/
│   ├── cart/       # Cart and cart-item models, serializers, and endpoints
│   ├── order/      # Orders, order items, checkout, and cancellation
│   ├── products/   # Products, categories, filtering, and catalog endpoints
│   ├── user/       # Custom user model and account/authentication endpoints
│   └── urls.py     # API app route aggregation
├── config/
│   ├── settings.py # Django settings, installed apps, database, JWT, and API defaults
│   └── urls.py     # Admin, API, schema, Swagger, and ReDoc routes
├── manage.py       # Django command-line entry point
├── requirements.txt
└── db.sqlite3      # Local database (created when migrations are applied)
```

Each app has its own `models.py`, `serializers.py`, `views.py`, `urls.py`, and `migrations/` directory. The database schema is described by the checked-in migrations.

## Getting started

Run these commands from the directory containing `manage.py`.

### 1. Install Python

Install Python 3.12 or newer and make sure the Python launcher (`py`) or `python` command is available in your terminal.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
```

If PowerShell blocks activation, either adjust the execution policy for your user or use Command Prompt:

```bat
.\env\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install project requirements

With the virtual environment active:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` pins the project dependencies, including Django, Django REST Framework, JWT authentication, filtering, and API schema tooling.

### 4. Apply database migrations

```bash
python manage.py migrate
```

This creates the local SQLite database (`db.sqlite3`) if it does not exist and applies migrations for Django's built-in apps and the project's user, products, cart, and order apps.

### 5. (Optional) Create an administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to create an account that can access the Django admin and admin-only API operations.

### 6. Start the development server

```bash
python manage.py runserver
```

The server is available at <http://127.0.0.1:8000/>. Stop it with `Ctrl+C`.

## Database migrations

Migrations track model/schema changes over time. The existing app migrations are committed, so a new checkout normally needs only:

```bash
python manage.py migrate
```

When you change a model, generate a migration for the affected app (or all apps), then apply it:

```bash
python manage.py makemigrations
python manage.py migrate
```

To generate a migration for one app only:

```bash
python manage.py makemigrations products
python manage.py migrate
```

The app labels are `user`, `products`, `cart`, and `order`. To inspect migration status:

```bash
python manage.py showmigrations
```

Commit new migration files along with the model changes. Do not edit an already-applied migration as a substitute for creating a new one.

## Run the development server

After activating the virtual environment and applying migrations, run:

```bash
python manage.py runserver
```

To use a different local port:

```bash
python manage.py runserver 8001
```

The local configuration allows requests to `localhost` and `127.0.0.1`. This is Django's development server and is not intended for production deployment.

## API documentation and endpoints

The root URL configuration provides:

| URL | Description |
| --- | --- |
| `/admin/` | Django administration site |
| `/api/schema/` | OpenAPI schema |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |

All application API routes are under `/api/`. The paths below are relative to that prefix. Keep the capitalization and trailing slashes as shown; URL paths are case-sensitive on many deployments.

### Accounts — `/api/user/`

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/user/registration/` | Register; provide `username`, `email`, `password`, and `password_confirm`. Returns access and refresh JWTs. |
| `POST` | `/api/user/login/` | Authenticate with `email` and `password`; returns access and refresh JWTs. |
| `GET` | `/api/user/Profile/` | Get the authenticated user's profile. |
| `GET` | `/api/user/users/` | List users (administrator only). |
| `POST` | `/api/user/change_password` | Change the authenticated user's password. |
| `POST` | `/api/user/Logout/` | Blacklist a refresh token; send it as `refresh` in the request body. |
| `POST` | `/api/user/refresh/` | Obtain a new access token from a refresh token. |

### Products — `/api/products/`

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/products/list_create/` | List products; requires authentication. |
| `POST` | `/api/products/list_create/` | Create a product (administrator only). |
| `GET` | `/api/products/retrieve_update_dest/<product-id>/` | Retrieve a product; requires authentication. |
| `PUT`, `PATCH`, `DELETE` | `/api/products/retrieve_update_dest/<product-id>/` | Update or delete a product (administrator only). |

The product list uses page-number pagination with a default page size of 10. The product filter set defines filters for SKU, name, category slug, minimum price (`minprice`), and maximum price (`maxprice`); use the generated schema to check the currently exposed query parameters.

### Cart — `/api/cart/`

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/cart/list_view_cart/` | View the authenticated user's cart. |
| `POST` | `/api/cart/add_in_cart/` | Add a product and quantity to the cart. |
| `PUT`, `PATCH` | `/api/cart/cart_item_modify/<cart-item-id>` | Modify a cart item. |
| `DELETE` | `/api/cart/Cart_items_delete/<cart-item-id>` | Delete a cart item. |

### Orders — `/api/order/`

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/order/check-out/` | Create an order from the authenticated user's cart. |
| `GET` | `/api/order/order_history/` | List the authenticated user's orders. |
| `GET` | `/api/order/view_individual_order/<order-id>` | Retrieve one of the authenticated user's orders. |
| `GET` | `/api/order/order_all` | List all orders (administrator only). |
| `PUT`, `PATCH` | `/api/order/update_order/<order-id>` | Update order status (administrator only). |
| `PUT`, `PATCH` | `/api/order/cancelled/<order-id>` | Cancel an eligible order owned by the authenticated user. |

## Typical API workflow

1. Register at `/api/user/registration/` or log in at `/api/user/login/`.
2. Send the returned access token on protected requests:

   ```http
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

3. Browse products and add product IDs and quantities to the cart.
4. Review the cart, then submit checkout with a shipping address. Checkout checks that the cart is non-empty, products are active, quantities are positive, and enough stock remains. On success it creates an order and order items, decrements stock, and removes the cart items.
5. Use order history and order detail to check the result. A user can cancel their own order while its status is `pending` or `confirmed`; cancellation restores item stock.
6. When the access token expires, use `/api/user/refresh/` with the refresh token. Logout blacklists a submitted refresh token.

For exact request and response fields, consult Swagger UI at <http://127.0.0.1:8000/api/docs/> after starting the server.

## Tests and useful commands

Run the Django checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

The app test modules are present, but currently contain only Django's empty `TestCase` scaffold; add tests as the API behavior is developed.

Other useful commands:

```bash
python manage.py shell
python manage.py showmigrations
python manage.py makemigrations --check
```

## Configuration and current limitations

- The default database is SQLite at the project root. The local database file is ignored by Git; each developer creates it by applying migrations.
- JWT access tokens are configured to last 200 minutes and refresh tokens 7 days.
- The checkout currently calculates a zero shipping fee, stores currency as `NPR`, and creates an order without initiating an external payment.
- The order app has payment model choices for eSewa and Khalti, but there is no payment gateway integration exposed in the current checkout flow.
- Product creation and changes, user listing, and the all-orders list are administrator-only. Registration, profile access, carts, checkout, and customer order operations require authentication as shown in the endpoint tables.
- `config/settings.py` currently contains a development secret key and `DEBUG = True`. Before deploying, use a private environment-provided secret key, turn off debug mode, configure allowed hosts and production database settings, and follow Django's deployment checklist.
