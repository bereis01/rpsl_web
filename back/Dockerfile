FROM python:3.12.3-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Copy all necessary files into the container.
WORKDIR /rpslweb
COPY shared/ ./shared
COPY back/ ./back
COPY data/ ./data

# Move to app folder and install requirements.
WORKDIR /rpslweb/back
RUN pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]