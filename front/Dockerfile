FROM python:3.12.3-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Copy all necessary files into the container.
WORKDIR /rpslweb
COPY front/ ./front

# Move to app folder and install requirements.
WORKDIR /rpslweb/front
RUN pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]