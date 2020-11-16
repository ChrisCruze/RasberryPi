FROM python:3.4
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
COPY static static
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]