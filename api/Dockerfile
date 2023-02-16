FROM python:3.11.2-slim-buster

COPY ./requirements.txt /api/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

WORKDIR /api

COPY ./app /api/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "--reload-dir", "/api", "app.main:app"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]