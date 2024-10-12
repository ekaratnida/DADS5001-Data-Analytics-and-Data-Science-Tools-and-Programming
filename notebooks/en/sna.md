# Lecture note: https://gephi.org/tutorials/gephi-tutorial-quick_start.pdf

**Title: Introduction to Social Network Analysis Using Python and Datasets**

**Objective:** Learn how to conduct Social Network Analysis (SNA) using Python and datasets. This tutorial will cover the basic concepts of SNA, introduce tools and libraries for non-technical learners, and guide you through practical coding exercises.

### **What is Social Network Analysis (SNA)?**

**Social Network Analysis (SNA)** is a technique used to understand the relationships between entities, such as individuals, organizations, or groups, by analyzing the network structure. It focuses on how entities are connected, the strength of these relationships, and the patterns of interactions. SNA is especially powerful for analyzing social, business, and communication networks. It helps identify influential actors, detect communities, and understand the dynamics within a network.

**Applications of SNA**:
1. **Sociology**: Studying social groups, influence patterns, and community structures.
2. **Marketing**: Identifying key influencers for product promotions and understanding consumer interactions.
3. **Political Science**: Analyzing political connections and coalitions.
4. **Healthcare**: Tracing the spread of diseases through contact networks.
5. **Business**: Studying supply chains, partnerships, and organizational structures.

**Social Network Analysis (SNA)** is a method for studying relationships between entities, such as individuals, organizations, or groups. It focuses on understanding how relationships form and evolve, and how they impact the overall network. SNA is widely used in sociology, marketing, and political science to study social structures and patterns of interactions.

**Key Concepts in SNA**:
1. **Nodes**: The entities (e.g., people, organizations) in the network.
2. **Edges**: The connections or relationships between nodes.
3. **Centrality**: Metrics like **degree**, **betweenness**, and **closeness** that measure the importance of nodes within a network.
4. **Communities**: Groups of nodes that are more closely connected to each other than to other nodes.

### **Python Tools for Social Network Analysis**

We will use Python libraries such as **NetworkX** and **Matplotlib** to conduct social network analysis.

- **NetworkX**: A popular Python library for creating, visualizing, and analyzing networks.
- **Matplotlib**: A plotting library used to visualize graphs and network metrics.

#### **Other Tools for Non-Technical Learners**

For non-technical students, there are also user-friendly tools available for conducting basic social network analysis without coding:

1. **Gephi**: An open-source visualization and exploration tool for networks, featuring drag-and-drop features to visualize networks.
2. **Pajek**: Software for large network analysis that comes with an easy-to-use graphical interface.
3. **NodeXL**: A Microsoft Excel plugin that allows users to perform basic social network analysis using familiar spreadsheet features.

### **Step 1: Setting Up Python Environment**

**Prerequisites**:

1. **Python Installed**: Make sure Python 3.8+ is installed.
2. **Install Required Libraries**:
   ```bash
   pip install networkx matplotlib pandas
   ```

### **Step 2: Loading and Visualizing a Dataset**

We will use various datasets representing different domains such as business, social activity, sports, and entertainment to help you understand different kinds of social networks:

1. **Business Network**: Represents relationships between companies, suppliers, and clients.
   ```python
   business_data = {
       'Company1': ['Company A', 'Company A', 'Company B', 'Company C'],
       'Company2': ['Company B', 'Company C', 'Company D', 'Company D']
   }
   business_df = pd.DataFrame(business_data)
   G_business = nx.from_pandas_edgelist(business_df, 'Company1', 'Company2')
   nx.draw(G_business, with_labels=True, node_color='lightgreen', node_size=2000, font_size=15, font_weight='bold')
   plt.title('Business Network Graph')
   plt.show()
   ```

2. **Social Activity Network**: Represents friendships and interactions between individuals.
   ```python
   social_data = {
       'Person1': ['Alice', 'Alice', 'Bob', 'Charlie'],
       'Person2': ['Bob', 'Charlie', 'David', 'Eve']
   }
   social_df = pd.DataFrame(social_data)
   G_social = nx.from_pandas_edgelist(social_df, 'Person1', 'Person2')
   nx.draw(G_social, with_labels=True, node_color='skyblue', node_size=2000, font_size=15, font_weight='bold')
   plt.title('Social Activity Network Graph')
   plt.show()
   ```

3. **Sports Network**: Represents the relationships between players in a team or competitions between teams.
   ```python
   sports_data = {
       'Team1': ['Team A', 'Team A', 'Team B'],
       'Team2': ['Team B', 'Team C', 'Team C']
   }
   sports_df = pd.DataFrame(sports_data)
   G_sports = nx.from_pandas_edgelist(sports_df, 'Team1', 'Team2')
   nx.draw(G_sports, with_labels=True, node_color='orange', node_size=2000, font_size=15, font_weight='bold')
   plt.title('Sports Network Graph')
   plt.show()
   ```

4. **Entertainment Network**: Represents relationships between artists, collaborations, or movies watched by the same audience.
   ```python
   entertainment_data = {
       'Artist1': ['Artist X', 'Artist X', 'Artist Y'],
       'Artist2': ['Artist Y', 'Artist Z', 'Artist Z']
   }
   entertainment_df = pd.DataFrame(entertainment_data)
   G_entertainment = nx.from_pandas_edgelist(entertainment_df, 'Artist1', 'Artist2')
   nx.draw(G_entertainment, with_labels=True, node_color='pink', node_size=2000, font_size=15, font_weight='bold')
   plt.title('Entertainment Network Graph')
   plt.show()
   ```

For simplicity, we will create small datasets to represent relationships in each domain.

```python
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Sample dataset representing relationships
data = {
    'Person1': ['Alice', 'Alice', 'Bob', 'Bob', 'Charlie', 'David'],
    'Person2': ['Bob', 'Charlie', 'Charlie', 'David', 'David', 'Eve']
}
df = pd.DataFrame(data)

# Create a graph using NetworkX
G = nx.from_pandas_edgelist(df, 'Person1', 'Person2')

# Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, font_size=15, font_weight='bold')
plt.title('Social Network Graph')
plt.show()
```

### **Explanation of Code**

1. **Create Dataset**: We create a small dataset with relationships between individuals.
2. **NetworkX Graph**: We use `from_pandas_edgelist()` to create a graph from the dataset.
3. **Visualize Graph**: The graph is visualized using `Matplotlib`.

### **Step 3: Calculating Network Metrics and Plotting Results**

To understand the network's structure, we can calculate various centrality metrics and plot the results to visualize important nodes in the network.

#### **Degree Centrality**
Degree centrality measures the number of connections a node has. Higher degree centrality indicates that the node is well connected.

```python
# Degree Centrality
degree_centrality = nx.degree_centrality(G)
print("Degree Centrality:")
for node, centrality in degree_centrality.items():
    print(f"{node}: {centrality:.2f}")

# Plotting Degree Centrality
plt.figure(figsize=(8, 6))
node_sizes = [10000 * degree_centrality[node] for node in G.nodes()]
nx.draw(G, with_labels=True, node_color='skyblue', node_size=node_sizes, font_size=15, font_weight='bold')
plt.title('Network Graph with Degree Centrality Highlighted')
plt.show()
```

#### **Betweenness Centrality**
Betweenness centrality measures the extent to which a node lies on paths between other nodes, which indicates its role as a bridge or connector within the network.

```python
# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
print("
Betweenness Centrality:")
for node, centrality in betweenness_centrality.items():
    print(f"{node}: {centrality:.2f}")

# Plotting Betweenness Centrality
plt.figure(figsize=(8, 6))
node_sizes = [10000 * betweenness_centrality[node] for node in G.nodes()]
nx.draw(G, with_labels=True, node_color='lightcoral', node_size=node_sizes, font_size=15, font_weight='bold')
plt.title('Network Graph with Betweenness Centrality Highlighted')
plt.show()
```

### **Explanation of Metrics**
- **Degree Centrality**: Indicates how many direct connections each node has, showing its level of influence in the network.
- **Betweenness Centrality**: Measures how often a node appears on the shortest path between other nodes, highlighting nodes that serve as critical bridges or connectors.

To understand the network's structure, we can calculate various centrality metrics.

```python
# Degree Centrality
degree_centrality = nx.degree_centrality(G)
print("Degree Centrality:")
for node, centrality in degree_centrality.items():
    print(f"{node}: {centrality:.2f}")

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
print("\nBetweenness Centrality:")
for node, centrality in betweenness_centrality.items():
    print(f"{node}: {centrality:.2f}")
```

### **Explanation of Metrics**

- **Degree Centrality**: The number of direct connections each node has.
- **Betweenness Centrality**: How often a node appears on the shortest path between other nodes, indicating its role as a bridge.

### **Step 4: Identifying Communities**

We can use NetworkX to identify communities within the network.

```python
from networkx.algorithms.community import greedy_modularity_communities

# Detect communities
communities = list(greedy_modularity_communities(G))

# Print community members
print("
Communities:")
for i, community in enumerate(communities):
    print(f"Community {i + 1}: {', '.join(community)}")
```

### **Step 5: Analyzing Larger Datasets**

To perform social network analysis on a larger dataset, we can use publicly available datasets such as the Facebook Social Circles dataset or generate synthetic data to simulate large social networks. Below, we create a dataset with 100 nodes to represent a larger network.

#### **Loading a Larger Dataset**

```python
import numpy as np

# Generating a synthetic larger dataset
np.random.seed(42)
num_nodes = 100
edges = []

# Create random connections between nodes
for i in range(300):
    person1 = f'Person_{np.random.randint(1, num_nodes + 1)}'
    person2 = f'Person_{np.random.randint(1, num_nodes + 1)}'
    if person1 != person2:  # Avoid self-loops
        edges.append((person1, person2))

# Convert edges to a DataFrame
large_df = pd.DataFrame(edges, columns=['Person1', 'Person2'])

# Create a graph using NetworkX
G_large = nx.from_pandas_edgelist(large_df, 'Person1', 'Person2')

# Draw a small subset of the graph for visualization purposes
plt.figure(figsize=(10, 8))
subgraph_nodes = list(G_large.nodes)[:30]  # Draw only 30 nodes for clarity
subgraph = G_large.subgraph(subgraph_nodes)
nx.draw(subgraph, with_labels=True, node_color='skyblue', node_size=800, font_size=8, font_weight='bold')
plt.title('Subset of Larger Social Network Graph')
plt.show()
```

#### **Calculating Metrics for a Larger Dataset**

##### **Degree Centrality for Large Dataset**
```python
# Degree Centrality for large dataset
degree_centrality_large = nx.degree_centrality(G_large)
sorted_degree_centrality = sorted(degree_centrality_large.items(), key=lambda x: x[1], reverse=True)

print("Top 10 Nodes by Degree Centrality:")
for node, centrality in sorted_degree_centrality[:10]:
    print(f"{node}: {centrality:.2f}")

# Plotting Degree Centrality Distribution
plt.figure(figsize=(10, 6))
plt.hist(degree_centrality_large.values(), bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Degree Centrality')
plt.ylabel('Frequency')
plt.title('Degree Centrality Distribution for Larger Network')
plt.show()
```

##### **Betweenness Centrality for Large Dataset**
```python
# Betweenness Centrality for large dataset
betweenness_centrality_large = nx.betweenness_centrality(G_large)
sorted_betweenness_centrality = sorted(betweenness_centrality_large.items(), key=lambda x: x[1], reverse=True)

print("
Top 10 Nodes by Betweenness Centrality:")
for node, centrality in sorted_betweenness_centrality[:10]:
    print(f"{node}: {centrality:.2f}")

# Plotting Betweenness Centrality Distribution
plt.figure(figsize=(10, 6))
plt.hist(betweenness_centrality_large.values(), bins=20, color='lightcoral', edgecolor='black')
plt.xlabel('Betweenness Centrality')
plt.ylabel('Frequency')
plt.title('Betweenness Centrality Distribution for Larger Network')
plt.show()
```

### **Accessing Real Datasets Online**

To analyze real-world social networks, you can access datasets from the following resources:

1. **Kaggle**: [Kaggle Datasets](https://www.kaggle.com/datasets) - Offers a variety of datasets, including social network data.
2. **SNAP (Stanford Large Network Dataset Collection)**: [SNAP Datasets](https://snap.stanford.edu/data/) - Provides large-scale network datasets such as Facebook and Twitter.
3. **Network Repository**: [Network Repository](http://networkrepository.com/) - Contains graph/network datasets from various domains.
4. **Google Dataset Search**: [Google Dataset Search](https://datasetsearch.research.google.com/) - A search engine for finding datasets.
5. **Public APIs for Real-Time Data**: Use public APIs like **Twitter API** and **Reddit API** to gather real-time social network data.

You can load these datasets in Python using pandas and perform analysis as demonstrated earlier.


1. **Set Up Python Environment**: Install Python and necessary libraries.
2. **Create and Visualize Graph**: Use NetworkX to create a social network graph and visualize it with Matplotlib.
3. **Calculate Network Metrics**: Compute metrics like degree and betweenness centrality to understand the structure of the network.
4. **Identify Communities**: Detect communities within the network using modularity-based approaches.

### **Next Steps**

- **Advanced Analysis**: Use other network metrics like closeness centrality and eigenvector centrality for deeper analysis.
- **Gephi Tutorial**: Introduce students to Gephi for non-coding network visualization.
- **Real-world Datasets**: Work with larger datasets, such as social media data or collaboration networks.

This tutorial provides an introduction to Social Network Analysis using Python and NetworkX, with additional suggestions for tools suitable for non-technical learners. Feel free to adapt the examples to fit your audience's level of comfort with coding!

