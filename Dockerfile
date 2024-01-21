FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /code/app

EXPOSE 80

CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]