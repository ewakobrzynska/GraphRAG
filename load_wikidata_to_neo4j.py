from neo4j import GraphDatabase

URI = "neo4j+s://5fdbd7a7.databases.neo4j.io"
AUTH = ("neo4j", "qprn5T7m96j2vd6Jeq2XKRIyvBzzZiC902qLSjWZOIs")

def load_data_to_neo4j(data):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session() as session:
            for item in data:
                artifact_name = item["artifact"]
                location_name = item["location"]
                era_name = item["era"]
                
                session.run("""
                MERGE (a:Artifact {name: $artifact_name})
                MERGE (l:Location {name: $location_name})
                MERGE (e:Era {name: $era_name})
                MERGE (a)-[:LOCATED_IN]->(l)
                MERGE (a)-[:BELONGS_TO]->(e)
                """, {
                    "artifact_name": artifact_name,
                    "location_name": location_name,
                    "era_name": era_name
                })

load_data_to_neo4j(wikidata_data)
