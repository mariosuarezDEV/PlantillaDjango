FROM python:3.12-bullseye

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# daphne -b 0.0.0.0 -p 8000 proyecto.asgi:application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "proyecto.asgi:application"]