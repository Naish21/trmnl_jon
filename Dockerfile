FROM python:3.13.9-slim-trixie

COPY ./src /deploy/src
RUN mkdir -p /deploy/src/auxdata
COPY ./requirements.txt /deploy
WORKDIR /deploy

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

# docker build . --tag horario_week:v0.01
# docker run -d
#   -p 8080:8080
#   -v ./horario:/deploy/src/auxdata
#   -d horario_week:v0.01
#   --name horarios
#   horario_week:v0.01