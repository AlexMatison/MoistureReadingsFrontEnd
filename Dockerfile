FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

RUN python setup.py develop

ENV FLASK_APP=MoistureReadingsFrontEnd/app.py

EXPOSE 5000

#CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0" ]
CMD [ "python", "MoistureReadingsFrontEnd/app.py" ]

#ENTRYPOINT ["python", "app.py"]