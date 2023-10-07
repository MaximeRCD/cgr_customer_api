#
FROM python:3.10

#
WORKDIR /client_api


#
COPY ./requirements.txt /client_api/requirements.txt
COPY ./routers/* /client_api/routers/
COPY ./models/* /client_api/models/
COPY ./services/* /client_api/services/
COPY ./database.py  /client_api/
COPY ./main.py /client_api/

#
RUN pip install --no-cache-dir --upgrade -r /client_api/requirements.txt

#
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]