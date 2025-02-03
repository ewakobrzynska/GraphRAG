from SPARQLWrapper import SPARQLWrapper, JSON
import json
from neo4j import GraphDatabase

URI = "neo4j+s://5fdbd7a7.databases.neo4j.io"
AUTH = ("neo4j", "qprn5T7m96j2vd6Jeq2XKRIyvBzzZiC902qLSjWZOIs")

def fetch_wikidata_data():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
        SELECT ?artifactLabel ?locationLabel ?eraLabel WHERE {
          ?artifact wdt:P31 wd:Q220659;   
                   wdt:P276 ?location;   
                   wdt:P2348 ?era.       
          SERVICE wikibase:label {       
            bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
          }
        }
        LIMIT 50
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    data = []
    for result in results["results"]["bindings"]:
        data.append({
            "artifact": result["artifactLabel"]["value"],
            "location": result["locationLabel"]["value"],
            "era": result["eraLabel"]["value"]
        })
    return data

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

wikidata_data = fetch_wikidata_data()

with open("wikidata_data.json", "w") as f:
    json.dump(wikidata_data, f, indent=2)

load_data_to_neo4j(wikidata_data)

print(wikidata_data)
