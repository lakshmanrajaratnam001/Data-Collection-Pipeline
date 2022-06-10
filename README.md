# Data-Collection-Pipeline
In this lab, you'll implement an industry grade data collection pipeline that runs scalably in the cloud.

Documentation for milestone 2

I have chosen to scrape data from Myprotein. Fitness is one of my passions, so I have chosen to scrape important detail of protein products. 

Documentation from milestone 3 

I decided to create a crawler that visits each product link and extracts the required information. I created different methods to scrape data from my chosen website, however they were created them in a way that works for multiple websites. I did not use XPATHS that are too specific as a slight change can break the scraper. Instead I used class names as I beleived it was more robust.Methods created includes navigating webpage (scroll, accept cookies and click next page), getting all the links and visiting them)

Documentation for milestone 4 

I have created unittests for each of the methods present in the Scraper class. These test the functionality of the method, and to see if it is performing as expected. Using the unittest module, I used assertions to see if actual value was True, comparing it with an expected value. All of the unittests are run from a separate file which imports the Scraper to access the methods. 

Documentation for milestone 5

Cloud services used include aws ec2 and rds instances. Raw dictionary file was stored locally as well as in an s3 bucket using boto3. Connecting to postgreSQL was acheived using sqlalchemy and psycopg2. 

Documentation for milestones 7

I used docker to containers my scraper and build an image. Firstly, I created a Dockerfile which contained information including downloading chrome and chrome driver, updating chromdwriver, installing requirements and the file I wished to run in docker. The python requirements were pulled from an existing docker image (python 3.8-slim-buster). Once the docker image was built, I pushed it to docker hub and pulled the image on my EC2 instance. To avoid rescraping data, I implemented code which checks the Postgres database for existing product item numbers. If the product item number is found in the database, then product information will not be scraped and the next product will attempt to be scraped. If the product item number is not found in the database then data for product would be scraped. 

Documentation for milestones 8 and 9 
The metrics of the ec2 scraper can be viewed on the Grafana dashboard. The metrics are measured using prometheus and they can be seen for the docker containers and local OS. Metrics include container states, daemon network actions and OS CPU actions. Github secrets contains the relavent information, including Dockerhub credentials used to build a new docker image. Github actions enable the Docker image to be built and and pushed to my Dockerhub account

