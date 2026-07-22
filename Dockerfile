FROM python:3.12-slim

WORKDIR /app

#installing dependencies 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

#copy the contents of host app/ 

COPY app/ .

EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]