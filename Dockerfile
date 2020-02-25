FROM python:3.7

COPY requirements.txt /tmp/
RUN pip install \
  --no-cache-dir \
  -r /tmp/requirements.txt

#RUN useradd appuser
#WORKDIR /home/appuser
#RUN chown appuser:appuser  /home/appuser
#USER appuser

COPY . .
ENTRYPOINT [ "python" ]
CMD [ "main.py"]
