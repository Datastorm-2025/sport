FROM 222.255.250.24:8001/teamid/pytorch@sha256:a7103283ea7113e10ae5d014bd2342acebda0bc53164b2f7b1dd6eb7a766bdb6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV INPUT_PATH=/input
ENV OUTPUT_PATH=/output

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /input /output

ENTRYPOINT ["python", "predict.py"]