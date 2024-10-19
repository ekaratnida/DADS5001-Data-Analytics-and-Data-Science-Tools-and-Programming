import requests
import pandas as pd

# Define the Pinot broker URL
PINOT_BROKER_URL = "http://localhost:8099/query/sql"

# Define a sample query to get movie ratings
#query = {
#    "sql": "SELECT movieId, title, AVG(rating) as avgRating FROM moviesTable GROUP BY movieId, title LIMIT 10"
#}
query = {
    "sql":"select * from movie_table limit 10"
}

# Send the query to Pinot
response = requests.post(PINOT_BROKER_URL, json=query)

# Check the response status
if response.status_code == 200:
    # Convert the response to a Pandas DataFrame
    result = response.json()
    print(result)
    columns = result['resultTable']['dataSchema']['columnNames']
    rows = result['resultTable']['rows']
    df = pd.DataFrame(rows, columns=columns)
    print(df)
else:
    print(f"Error: {response.status_code}, {response.text}")