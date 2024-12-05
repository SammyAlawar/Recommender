# start by pulling the python image
FROM python:3.8-alpine
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
# switch working directory
WORKDIR /app
# install the dependencies and packages in the requirements file
RUN python --version
FROM python:3.9-slim
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
# copy every content from the local file to the image
COPY . /app
CMD ["python3", "app.py"]