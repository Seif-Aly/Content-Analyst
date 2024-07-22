import os
import requests
import socket
import dns.resolver
from bs4 import BeautifulSoup
import psycopg2
import csv
import logging

# Configure logging
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, 'script.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s')

# Function to get the IP address
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        logging.error(f"ERROR getting IP for domain: {domain}")
        return None

# Function to get the NS record
def get_ns_record(domain):
    try:
        result = dns.resolver.resolve(domain, 'NS')
        return [str(rdata) for rdata in result]
    except Exception as e:
        logging.error(f"ERROR getting NS record for domain: {domain} : {e}")
        return None

# Function to get the HTTP status code and <title> tag
def get_http_and_title(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        response.encoding = 'utf-8-sig'
        status_code = response.status_code
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.title.string if soup.title else ''
        return status_code, title_tag
    except Exception as e:
        logging.error(f"ERROR getting HTTP info for domain: {domain} : {e}")
        return None, None

# Function to process a single domain
def process_domain(domain):
    ip = get_ip(domain)
    ns_record = get_ns_record(domain)
    http_status_code, title_tag = get_http_and_title(domain)
    return domain, ip, ns_record, http_status_code, title_tag


# Read domains from the text file in same directory
file_path = os.path.join(script_dir, 'List.txt')
with open(file_path, 'r') as file:
    domains = [line.strip() for line in file.readlines()]

# Process domains
all_data = []
for domain in domains:
    data = process_domain(domain)
    all_data.append(data)

try:
    # Connection to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="root",
        database="task_data"
    )
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute('DROP TABLE IF EXISTS domains')

    # Create the table of data
    cursor.execute('''
        CREATE TABLE domains (
            domain TEXT,
            ip TEXT,
            ns_record TEXT,
            http_status_code INTEGER,
            title_tag TEXT
        )
    ''')

    # Insert result data to table
    for data in all_data:
        try:
            cursor.execute('''
                INSERT INTO domains (domain, ip, ns_record, http_status_code, title_tag)
                VALUES (%s, %s, %s, %s, %s)
            ''', (data[0], data[1], ','.join(data[2]) if data[2] else '', data[3], data[4]))
        except Exception as e:
            logging.error(f"Error inserting data for domain {data[0]} : {e}")

    conn.commit()
    print(f"SQL table created and data successfully inserted")

    # Additionally exporting to CSV
    csv_file = os.path.join(script_dir, 'domains_data.csv')
    # utf-8-sig for other languages characters
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['domain', 'ip', 'ns_record',
                        'http_status_code', 'title_tag'])
        for data in all_data:
            writer.writerow(data)

    conn.close()
    print(f"Data has been exported to {csv_file}")

except Exception as e:
    logging.error(f"Error connecting to the database or creating table : {e}")  
