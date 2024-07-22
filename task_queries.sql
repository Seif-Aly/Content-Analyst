-- Query 1: Domains with IP ending in an odd number
SELECT domain, ip FROM domains
WHERE ip IS NOT NULL AND (CAST(SUBSTR(ip, LENGTH(ip), 1) AS INTEGER) % 2) = 1;

-- Query 2: Domains with TLD .com and Name Server *.cloudflare.com
SELECT domain, ns_record FROM domains
WHERE domain LIKE '%.com' AND ns_record LIKE '%cloudflare.com%';

-- Query 3: Domains with HTTP status code 200 and "news" in <title>
SELECT domain, http_status_code, title_tag FROM domains
WHERE http_status_code = 200 AND title_tag LIKE '%news%';
