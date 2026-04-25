FROM python:3.10.20-trixie

WORKDIR /app

COPY app .

RUN pip install --no-cache-dir pipenv

RUN pipenv install --system --deploy

CMD ["uvicorn", "auth_service:app", "--host", "0.0.0.0", "--port", "60680"]
