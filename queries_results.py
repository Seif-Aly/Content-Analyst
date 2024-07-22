import os
import psycopg2
import csv
import logging

# Configure logging
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, 'queries_results.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s')

# Function to export query to SQL and CSV
def query_to_sql_csv(cursor, query, sql_filename, csv_filename, headers):
    try:
        cursor.execute(query)
        results = cursor.fetchall()

        # Results to CSV
        csv_file = os.path.join(script_dir, csv_filename)
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(results)

        # Results to SQL
        sql_file = os.path.join(script_dir, sql_filename)
        with open(sql_file, 'w', encoding='utf-8-sig') as file:
            file.write(query + ';\n')

    except Exception as e:
        logging.error(f"Error executing query: {query} : {e}")


try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="root",
        database="task_data"
    )
    cursor = conn.cursor()

    # Define the queries and their respective output filenames and headers
    queries = [
        {
            "query": '''
                SELECT domain, ip FROM domains
                WHERE ip IS NOT NULL AND (CAST(SUBSTRING(ip FROM LENGTH(ip) FOR 1) AS INTEGER) % 2) = 1
            ''',
            "csv_filename": "ip_end_with_odd_domains.csv",
            "sql_filename": "ip_end_with_odd_domains.sql",
            "headers": ["domain", "ip"]
        },
        {
            "query": '''
                SELECT domain, ns_record FROM domains
                WHERE domain LIKE '%.com' AND ns_record LIKE '%cloudflare.com%'
            ''',
            "csv_filename": "cloudflare_com_domains.csv",
            "sql_filename": "cloudflare_com_domains.sql",
            "headers": ["domain", "ns_record"]
        },
        {
            "query": '''
                SELECT domain, http_status_code, title_tag FROM domains
                WHERE http_status_code = 200 AND title_tag LIKE '%news%'
            ''',
            "csv_filename": "http_200_tag_with_news_domains.csv",
            "sql_filename": "http_200_tag_with_news_domains.sql",
            "headers": ["domain", "http_status_code", "title_tag"]
        }
    ]

    # Export each query to CSV and SQL
    for query_info in queries:
        query_to_sql_csv(cursor, query_info["query"], query_info["sql_filename"],
                         query_info["csv_filename"], query_info["headers"])

    conn.close()
    print("Results have been exported to SQL and CSV files")

except Exception as e:
    logging.error(f"Error connecting to the database : {e}")
