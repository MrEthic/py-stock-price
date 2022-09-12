FROM python:3.10.2-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/MrEthic/py-stock-price.git .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "src/🏠_Home.py", "--server.port=8501", "--server.address=0.0.0.0"]