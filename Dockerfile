FROM python:latest
WORKDIR /code
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]