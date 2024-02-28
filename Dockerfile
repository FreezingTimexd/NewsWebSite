FROM python:3.11.6
WORKDIR /app/
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uvicorn
ADD . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]