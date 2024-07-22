
                SELECT domain, ns_record FROM domains
                WHERE domain LIKE '%.com' AND ns_record LIKE '%cloudflare.com%'
            ;
