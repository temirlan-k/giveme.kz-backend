FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
CMD ["uvicorn" ,"app.main:app" ,"--host" ,"0.0.0.0" ,"--port" ,"5001" ,"--reload"]