FROM ubuntu:22.04

RUN dpkg --add-architecture i386 && \
    apt update && \
    apt install -y wine64 wine32 wget python3 python3-pip

WORKDIR /src

COPY . .

RUN wget https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe

RUN wine python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

RUN wine python -m pip install pygame pyinstaller

RUN wine pyinstaller --onefile --windowed --name Reed main.py
