from neo4j import GraphDatabase

URI = "neo4j+s://5fdbd7a7.databases.neo4j.io"
AUTH = ("neo4j", "qprn5T7m96j2vd6Jeq2XKRIyvBzzZiC902qLSjWZOIs")

def load_data_to_neo4j(data):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session() as session:
            for item in data:
                artifact_name = item.get("title", ["Unknown Artifact"])[0]
                location = item.get("places", ["Unknown Location"])[0]
                era = item.get("year", "Unknown Era")
                
                session.run("""
                MERGE (a:Artifact {name: $artifact_name})
                MERGE (l:Location {name: $location})
                MERGE (e:Era {name: $era})
                MERGE (a)-[:LOCATED_IN]->(l)
                MERGE (a)-[:BELONGS_TO]->(e)
                """, {
                    "artifact_name": artifact_name,
                    "location": location,
                    "era": era
                })

import json
with open("europeana_data.json") as f:
    europeana_data = json.load(f)

load_data_to_neo4j(europeana_data)
