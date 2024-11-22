FROM prefecthq/prefect:3.1.2-python3.11
# For Debian/Ubuntu based images
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /opt/prefect/workflow/requirements.txt
RUN python -m pip install -r /opt/prefect/workflow/requirements.txt
COPY . /opt/prefect/workflow/
WORKDIR /opt/prefect/workflow/
