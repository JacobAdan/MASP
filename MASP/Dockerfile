
FROM python:3.11

WORKDIR /misp-anomaly-signature-parser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /misp-anomaly-signature-parser /misp-anomaly-signature-parser

COPY /misp-anomaly-signature-parser/Definitions /usr/local/lib/python3.11/site-packages/pymisp/data/misp-objects/objects

CMD ["tail", "-f", "/dev/null"]