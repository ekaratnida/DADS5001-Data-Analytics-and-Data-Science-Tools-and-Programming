**Title: Integrating Apache Pinot with Python: A Comprehensive Tutorial**

**Objective:** Learn how to use Apache Pinot for real-time data analytics with Python. This tutorial will cover the theory behind Apache Pinot and demonstrate how to integrate it with Python for performing data analytics.

### **What is Apache Pinot?**

**Apache Pinot** is a real-time distributed analytics data store that enables ultra-fast, scalable, and efficient OLAP (Online Analytical Processing) on large volumes of data. Originally developed at LinkedIn, it powers real-time analytics for various applications, such as monitoring, user-facing analytics, and dashboarding. Pinot is especially useful when data freshness and low-latency querying are crucial.

**Key Features of Apache Pinot**:
1. **Real-time Analytics**: It supports both real-time and batch data ingestion.
2. **Low Latency**: Provides millisecond-level response time, even with large datasets.
3. **Scalability**: Can scale horizontally, supporting complex aggregation and filtering operations.
4. **Columnar Data Store**: Optimized for efficient storage and retrieval of columnar data, which benefits OLAP queries.

### **Architecture Overview**

Apache Pinot's architecture consists of several key components:
1. **Controller**: Coordinates the cluster and manages table configurations.
2. **Broker**: Routes queries to the appropriate server to return results to the client.
3. **Server**: Stores data segments and serves queries.
4. **Minion**: Handles background tasks like data compaction.
5. **Real-time and Offline Ingestion**: Supports data ingestion from streaming sources (e.g., Apache Kafka) and batch sources (e.g., Hadoop, S3).

### **Python and Apache Pinot Integration**

Python is widely used in the data analytics ecosystem, and by integrating Python with Apache Pinot, you can create robust data analysis pipelines to work with real-time data.

We will use the **Pinot REST API** to communicate between Python and Apache Pinot. Python's `requests` library will allow us to send HTTP requests to query and interact with Pinot.

### **Prerequisites**

1. **Python Installed**: Ensure Python 3.8+ is installed.
2. **Apache Pinot Setup**: You need a running instance of Apache Pinot. You can use Docker to set it up quickly:
   ```bash
   docker run -p 9000:9000 -p 8099:8099 apachepinot/pinot:latest
   ```
3. **Install Required Libraries**:
   ```bash
   pip install requests pandas
   ```

### **Step 1: Setting Up Apache Pinot**

First, make sure you have Apache Pinot running. You can either run it locally using Docker or set up a Pinot cluster. Once Pinot is running, you can access the web UI at `http://localhost:9000`.

### **Step 2: Ingest Sample Data into Apache Pinot**

You need to ingest data into Apache Pinot to query it. Here, we use a sample dataset containing movie ratings.

1. **Create a Schema**:
   ```json
   {
     "schemaName": "moviesSchema",
     "dimensionFieldSpecs": [
       {"name": "movieId", "dataType": "INT"},
       {"name": "title", "dataType": "STRING"},
       {"name": "genres", "dataType": "STRING"}
     ],
     "metricFieldSpecs": [
       {"name": "rating", "dataType": "FLOAT"}
     ]
   }
   ```
   You can use the Pinot UI or REST API to create this schema.

2. **Create a Table**:
   Define a real-time table that specifies Kafka as the ingestion source or an offline table for batch data.

3. **Insert Data into the Table**:
   Data can be inserted into Pinot using either real-time ingestion (e.g., from Kafka) or batch ingestion (e.g., from CSV files).

   - **Real-Time Ingestion Using Kafka**:
     - First, create a Kafka topic (e.g., `movies-topic`) and produce messages to this topic using Python.
     
     ```python
     from kafka import KafkaProducer
     import json

     producer = KafkaProducer(bootstrap_servers='kafka-broker:9092',
                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))

     data = {
         "movieId": 1,
         "title": "Inception",
         "genres": "Action, Sci-Fi",
         "rating": 4.8
     }
     producer.send('movies-topic', value=data)
     producer.flush()
     ```
     - Pinot will automatically consume data from Kafka and insert it into the table if properly configured.

   - **Batch Ingestion Using Files**:
     - Prepare a CSV file (e.g., `movies.csv`) with the data you want to ingest.
     - Use Pinot's `Add Table` command to ingest the batch data:
     
     ```bash
     bin/pinot-admin.sh AddTable \
       -tableConfigFile /path/to/moviesTableConfig.json \
       -schemaFile /path/to/moviesSchema.json
     ```

     - You can also use Python to upload data:
     
     ```python
     import requests

     upload_url = "http://localhost:9000/tables/batch"
     files = {
         'file': ('movies.csv', open('movies.csv', 'rb')),
     }
     response = requests.post(upload_url, files=files)
     print(response.status_code, response.text)
     ```

### **Step 3: Querying Pinot with Python**

Now that you have data in Pinot, you can use Python to interact with it. We will use the Pinot REST API to send queries.

```python
import requests
import pandas as pd

# Define the Pinot broker URL
PINOT_BROKER_URL = "http://localhost:8099/query"

# Define a sample query to get movie ratings
query = {
    "sql": "SELECT movieId, title, AVG(rating) as avgRating FROM moviesTable GROUP BY movieId, title LIMIT 10"
}

# Send the query to Pinot
response = requests.post(PINOT_BROKER_URL, json=query)

# Check the response status
if response.status_code == 200:
    # Convert the response to a Pandas DataFrame
    result = response.json()
    columns = result['resultTable']['dataSchema']['columnNames']
    rows = result['resultTable']['rows']
    df = pd.DataFrame(rows, columns=columns)
    print(df)
else:
    print(f"Error: {response.status_code}, {response.text}")
```

### **Explanation of Code**

1. **Broker URL**: The Pinot Broker is responsible for receiving queries and returning results. We send our SQL query to the broker using the `/query` endpoint.
2. **Query Definition**: The query is defined in JSON format, which includes the SQL statement.
3. **HTTP Request**: We use Python's `requests.post()` method to send the query to Pinot.
4. **Response Handling**: If the response is successful, the JSON data is converted into a Pandas DataFrame for easier analysis and visualization.

### **Step 4: Performing Analytics**

You can further perform various types of analytics using Python and Pinot, such as:

- **Aggregation**: Use SQL queries to aggregate data in Pinot and visualize it in Python using libraries like `matplotlib`.
- **Data Visualization**: You can plot the results using `matplotlib` or `seaborn`.

**Example - Plotting Average Movie Ratings**:
```python
import matplotlib.pyplot as plt

# Assuming df contains the results from Pinot
plt.figure(figsize=(10, 6))
plt.bar(df['title'], df['avgRating'])
plt.xlabel('Movie Title')
plt.ylabel('Average Rating')
plt.title('Average Movie Ratings')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### **Summary**

1. **Setup Apache Pinot**: Set up a local Pinot instance and ingest data.
2. **Integrate with Python**: Use the Pinot REST API to interact with Pinot from Python.
3. **Query and Analyze Data**: Perform SQL queries and visualize the results using Python.

### **Next Steps**

- **Real-Time Data Streams**: Integrate Pinot with streaming data sources like Kafka to analyze data in real-time.
- **Advanced Queries**: Learn more about the advanced querying capabilities of Pinot, such as text search and complex aggregations.
- **Scaling Pinot**: Explore how to scale Apache Pinot for production workloads.

This tutorial provides a solid foundation for working with Apache Pinot and Python for real-time data analytics. Feel free to experiment with different datasets and build custom visualizations!

