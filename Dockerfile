# Step 1: Base image
FROM python:3.10

# Step 2: Set work directory inside container
WORKDIR /app

# Step 3: Copy code into container
COPY . /app

# Step 4: Upgrade pip & install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

# Step 5: Collect static files (optional for production)
# RUN python manage.py collectstatic --noinput

# Step 6: Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
