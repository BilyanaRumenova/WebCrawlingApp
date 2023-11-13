# WebCrawlingApp

A web service built with FastAPI responsible for collecting website screenshots (using playwright).

## Getting set up
### Option 1: Running locally
1. Ensure Python 3.x is installed.
2. Create a Virtual Environment and activate it
3. Install necessary libraries using: ```pip install -r requirements.txt```.
4. Run the app: ```uvicorn main:app --host 0.0.0.0 --port 8000```
5. Access the web application in a browser at http://localhost:8000
6. Open your web browser and navigate to http://localhost:8000 to access the web application.

### Option 2: Running with Docker
1. Ensure Docker is installed
2. Build the Docker Image: ```docker build -t {service_name} .```
3. Run the Docker Container: ```docker run -p 8000:8000 {servie_name}```

## Usage
Endpoints:
- GET /isalive - used for checking the server's health.
- POST /screenshots -  used for the starting of the process of web page crawling and shooting of the web pages. The route requires 2 parameters: “start url” and “number of links to follow”. Start url is the homepage from which the crawling will start and also needs to take a screenshot. 
- GET /screenshots/{id} - used to return collected screenshots for the provided id


### Examples
1. Check server health:
    ```curl http://localhost:8000/isalive```
2. Capture screenshots. The response will contain a unique ID that you can use to retrieve the screenshots.:
    ```curl -X POST -d '{"start_url": "https://example.com", "number_of_links_to_follow": 2}' http://127.0.0.1:8000/screenshots```

3. Retrieve screenshots:
 ```curl http://localhost:8000/screenshots/{id}```


