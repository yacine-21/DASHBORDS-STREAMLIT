FROM python:3.7
WORKDIR /app
COPY . .
RUN pip install streamlit
RUN pip install pandas
RUN pip install matplotlib
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "index.py"]
