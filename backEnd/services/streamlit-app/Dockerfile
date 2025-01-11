FROM python:3.9-slim

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]

# FROM python:3.9-slim

# # Створення робочої директорії
# WORKDIR /app

# # Копіюємо файли проекту
# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# ENV PATH="/root/.local/bin:$PATH"

# EXPOSE 8501

# CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
