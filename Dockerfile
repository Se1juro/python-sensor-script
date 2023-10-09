FROM python:3.8.10

WORKDIR /app

COPY . .

RUN pip install pymongo
RUN pip install numpy
RUN pip install scikit-learn

CMD ["python3", "main.py"]
