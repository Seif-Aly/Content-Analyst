
                SELECT domain, http_status_code, title_tag FROM domains
                WHERE http_status_code = 200 AND title_tag LIKE '%news%'
            ;
