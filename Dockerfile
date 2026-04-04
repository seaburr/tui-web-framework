FROM python:3.12-alpine
WORKDIR /app

# No external dependencies — stdlib only.
COPY artemis-ui.css lib.py server.py ./
COPY apps/ apps/

EXPOSE 8080
CMD ["python3", "server.py"]
