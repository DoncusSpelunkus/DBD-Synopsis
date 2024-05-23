# DBD-Synopsis

Synopsis for our Databases for Developers course

ENDPOINTS:
    <http://localhost:8080/getSessionSpecificWithUser>
        - Body {
            "userId": 500,
            "sessionId": 1
        }

    <http://localhost:8080/getLifetimeByDate>
        - Body {
            "start_date": "2020-12-07",
            "end_date": "2021-11-04"
        }
