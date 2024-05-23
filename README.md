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

    <http://localhost:8080/getAllSessions>


Args:
    --norun (prevents main loop from executing)
    --rebuildDb (rebuils mongoDb) HAS THREE SUB ARGS
        --both (rebuilds both indexed and nonindexed db)
        --noindex (rebuilds only nonindexed db)
        --index (rebuilds only indexed db)
    --redis_test (runs tabulation with Redis active)
    --mongo_test (runs tabulation with only mongoDb)
    
