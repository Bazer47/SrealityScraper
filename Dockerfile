FROM python:latest
WORKDIR /code
COPY . .
RUN pip install -r requirements_prod.txt
EXPOSE 5000
CMD ["python", "app.py"]