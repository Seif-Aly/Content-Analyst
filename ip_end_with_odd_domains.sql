
                SELECT domain, ip FROM domains
                WHERE ip IS NOT NULL AND (CAST(SUBSTRING(ip FROM LENGTH(ip) FOR 1) AS INTEGER) % 2) = 1
            ;
