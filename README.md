## django-ecommerce-backend
This is the backend component of an E-commerce application built with Django.

# Prerequisites
1. Docker
2. Docker Compose
# Installation
1. Clone the repository:
2. cd django-ecommerce-backend
3. Set up environment variables:

```
DEBUG=True
SECRET_KEY=django-insecure-fpl8sz@o4#c-+o5*i8o8ar=p+9j)k3+#m!3v11y2y+d8u-sp6$

DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=host.docker.internal
DB_PORT=5430

STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
```

Open the .env file and provide the required values for environment variables such as database credentials and Stripe API keys.
You need to create stripe account to get API Keys.

# Build Docker containers:

```docker compose up --build```

This command will build and start the Docker containers required for the project.

# Usage
Accessing the API: The API can be accessed at http://localhost:8000/api/.







