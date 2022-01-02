FROM python:3.10-windowsservercore
WORKDIR /app

COPY requirements.txt aw64.dll run.py /app/
RUN pip install -r requirements.txt
COPY plugin_bot /app/plugin_bot

ENTRYPOINT [ "python", "run.py" ]