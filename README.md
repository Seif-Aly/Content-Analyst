# Content-Analyst

## Task criteria

From list of 1000 domains:
1) Create python script to get the following data: IP, NS record, http status code, tag <title>
2) Create structured database with all data
3) Write SQL queries to get:
  - all domains that have IP which ends with an odd number
  - all domains with TLD .com and Name Server *.cloudflare.com
  - all domains that have http status code 200 and have the word "news" in tag <title>

## Tools and Technologies
•	Python
•	PostgreSQL
•	Microsoft Excel
•	Requests library
•	Socket library
•	os library
•	dnspython library
•	BeautifulSoup library
•	psycopg2 library
•	csv library
•	logging library

## Data Collection
### 1)	Reading Domains:
Domains were read from a text file “domains.txt”
### 2)	Fetching Data:
IP Address: Obtained using the socket library.
NS Record: Fetched using the dnspython library.
HTTP Status Code and Title Tag: Retrieved using the requests library and parsed with BeautifulSoup.
### 3)	Error Handling:
Errors during data collection were logged using the logging library.

## Database Setup
1)	Install PostgreSQL
2)	Create a PostgreSQL User and Database
3)	Use the data inside python file to connect to database

## Python script results 
### From logs:
<img width="409" alt="image" src="https://github.com/user-attachments/assets/5cd3c61c-89cc-4bc8-ba9e-12077f8259d9">

### From Excel:
<img width="428" alt="image" src="https://github.com/user-attachments/assets/d576b41f-776c-45cb-84de-706d27d7aa3e">

### From pgAdmin:
<img width="428" alt="image" src="https://github.com/user-attachments/assets/34029240-694e-4a65-88cc-05a109adade0">

## SQL Queries Results
### From pgAdmin:
<img width="468" alt="image" src="https://github.com/user-attachments/assets/9e041494-f58b-4a27-b2e4-26539f018353">
<img width="468" alt="image" src="https://github.com/user-attachments/assets/50788c1b-3c8d-47d6-8c03-54b994672010">
<img width="468" alt="image" src="https://github.com/user-attachments/assets/1961037c-3624-4028-9e11-dc12b12b363b">

### From Excel:
<img width="358" alt="image" src="https://github.com/user-attachments/assets/39b73dc5-df63-43d1-b2de-c3f8228a0987">
<img width="359" alt="image" src="https://github.com/user-attachments/assets/bf7ec1f4-551b-4961-8b3c-b112929b12cf">
<img width="360" alt="image" src="https://github.com/user-attachments/assets/ab657182-c205-4447-aec3-9f47265b12bb">
