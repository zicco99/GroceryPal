FROM python:3.5
ADD . .
RUN pip3 install -r requirements.txt
ENV FLASK_APP=main.py
EXPOSE 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
