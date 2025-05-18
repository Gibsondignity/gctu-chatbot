# Use an official Python runtime
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Only copy requirements first (so Docker can cache this step unless it changes)
COPY requirements.txt /code/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get install -y libpq-dev gcc

# Now copy the rest of your code (won’t affect pip install caching)
COPY . /code/

# Optional: Don't run migrations during build — do it at runtime
# CMD handles that better.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
