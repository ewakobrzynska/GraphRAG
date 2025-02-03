from neo4j import GraphDatabase

URI = "neo4j+s://5fdbd7a7.databases.neo4j.io"
AUTH = ("neo4j", "qprn5T7m96j2vd6Jeq2XKRIyvBzzZiC902qLSjWZOIs")

def connect_to_db():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            driver.verify_connectivity()
            print("Connected to Neo4j")
        except Exception as e:
            print(f"Failed to connect: {e}")

if __name__ == "__main__":
    connect_to_db()


