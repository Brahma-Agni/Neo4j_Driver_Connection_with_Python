import pickle
from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Harshal@2803"
database = "guiappdvs"

# Function to fetch data from Neo4j
def fetch_data_from_neo4j():
    driver = GraphDatabase.driver(uri, auth=(username, password))
    data = []
    
    try:
        with driver.session(database=database) as session:
            # Query to retrieve authors, papers, and categories
            query = """
            MATCH (a:Author)-[:AUTHORED]->(p:Paper)-[:BELONGS_TO]->(c:Category)
            RETURN a.name AS author_name, p.paper_id AS paper_id, p.name AS paper_name, 
                   p.year_of_publication AS year, c.type AS category
            """
            result = session.run(query)
            
            # Structure data in a list of dictionaries
            for record in result:
                author_name = record["author_name"]
                paper_id = record["paper_id"]
                paper_name = record["paper_name"]
                year = record["year"]
                category = record["category"]

                # Check if author already exists in data
                author_entry = next((item for item in data if item['author_name'] == author_name), None)
                if not author_entry:
                    author_entry = {'author_name': author_name, 'papers': []}
                    data.append(author_entry)
                
                # Add paper details to the author's entry
                author_entry['papers'].append({'paper_id': paper_id, 'name': paper_name, 'year': year, 'category': category})

    except Exception as e:
        print(f"Error fetching data from Neo4j: {e}")
    finally:
        driver.close()
    
    return data

# Save fetched data to a pickle file
def save_data_to_pickle(data):
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print("Data saved to data.pkl")

# Fetch and save data
data = fetch_data_from_neo4j()
save_data_to_pickle(data)
