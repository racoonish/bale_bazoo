FROM python:3.11-slim

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000
# Run the application:
COPY app.py .
CMD exec python app.py
