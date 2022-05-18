# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt