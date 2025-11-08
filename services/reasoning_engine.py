import os
import traceback
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, Literal, XSD
from rdflib.plugins.sparql import prepareQuery
from datetime import datetime
from typing import Dict, List, Any


class HospitalKPIReasoner:
    """
    Ontology reasoning and KPI analysis engine.
    Loads RDF/OWL data, runs SPARQL queries, and generates insights.
    """

    def __init__(self, ontology_path: str, data_path: str):
        print("\n🔍 === HOSPITAL KPI REASONER STARTUP DEBUG ===")

        ontology_full = os.path.join(os.getcwd(), ontology_path)
        data_full = os.path.join(os.getcwd(), data_path)

        print(f"🧩 Working directory: {os.getcwd()}")
        print(f"📂 Ontology path arg: {ontology_path}")
        print(f"📂 Data path arg: {data_path}")
        print(f"📍 Ontology full path: {ontology_full}")
        print(f"📍 Data full path: {data_full}")

        print(f"✅ Ontology file exists? {os.path.exists(ontology_full)}")
        print(f"✅ Data file exists? {os.path.exists(data_full)}")

        self.graph = Graph()

        try:
            # Bind namespace
            self.hospital = Namespace("http://hospital-kpi.org/ontology#")
            self.graph.bind("hospital", self.hospital)

            # Load ontology (OWL)
            print("🧠 Parsing ontology file...")
            self.graph.parse(ontology_full, format="xml")
            print("✅ Ontology parsed successfully!")

            # Load data (TTL)
            print("🧠 Parsing data file...")
            self.graph.parse(data_full, format="turtle")
            print("✅ Data parsed successfully!")

            print(f"📊 Total triples loaded: {len(self.graph)}")

            for i, (s, p, o) in enumerate(self.graph):
                print(f"   • {s} {p} {o}")
                if i >= 5:
                    break

            print("🔍 === DEBUG COMPLETE ===\n")

        except Exception as e:
            print("❌ ERROR during ontology/data parsing!")
            traceback.print_exc()
            raise e

    # ---------------------------------------------------------
    #  Retrieve all KPIs
    # ---------------------------------------------------------
    def get_all_kpis(self) -> List[Dict[str, Any]]:
        print("⚙️ Running get_all_kpis() ...")
        try:
            query = prepareQuery("""
                SELECT ?kpi ?label ?domain ?goal ?target ?unit ?obs ?value ?status ?timestamp
                WHERE {
                    ?kpi a hospital:KPI ;
                         rdfs:label ?label ;
                         hospital:targetValue ?target ;
                         hospital:unit ?unit ;
                         hospital:belongsToDomain ?domain ;
                         hospital:contributesToGoal ?goal ;
                         hospital:hasObservation ?obs .
                    ?obs hospital:hasValue ?value ;
                         hospital:status ?status ;
                         hospital:timestamp ?timestamp .
                }
            """, initNs={"hospital": self.hospital})

            results = []
            for row in self.graph.query(query):
                results.append({
                    "uri": str(row.kpi),
                    "label": str(row.label),
                    "domain": str(row.domain),
                    "goal": str(row.goal),
                    "target": float(row.target),
                    "unit": str(row.unit),
                    "observation": {
                        "uri": str(row.obs),
                        "value": float(row.value),
                        "status": str(row.status),
                        "timestamp": str(row.timestamp)
                    }
                })

            print(f"✅ Retrieved {len(results)} KPIs")
            return results

        except Exception as e:
            print("❌ ERROR in get_all_kpis():", e)
            traceback.print_exc()
            return []

    # ---------------------------------------------------------
    #  Retrieve KPI relationships
    # ---------------------------------------------------------
    def get_kpi_relationships(self) -> List[Dict[str, Any]]:
        print("⚙️ Running get_kpi_relationships() ...")
        try:
            query = prepareQuery("""
                SELECT ?kpi1 ?kpi2 ?relationship
                WHERE {
                    { ?kpi1 hospital:influences ?kpi2 . BIND("influences" as ?relationship) }
                    UNION
                    { ?kpi1 hospital:dependsOn ?kpi2 . BIND("dependsOn" as ?relationship) }
                }
            """, initNs={"hospital": self.hospital})

            results = []
            for row in self.graph.query(query):
                results.append({
                    "source": str(row.kpi1),
                    "target": str(row.kpi2),
                    "relationship": str(row.relationship)
                })

            print(f"✅ Retrieved {len(results)} relationships")
            return results

        except Exception as e:
            print("❌ ERROR in get_kpi_relationships():", e)
            traceback.print_exc()
            return []

    # ---------------------------------------------------------
    #  Generate semantic insights
    # ---------------------------------------------------------
    def generate_insights(self) -> List[Dict[str, Any]]:
        print("⚙️ Running generate_insights() ...")
        insights = []

        try:
            kpis = self.get_all_kpis()
            relationships = self.get_kpi_relationships()

            critical_kpis = [k for k in kpis if k["observation"]["status"] == "critical"]
            warning_kpis = [k for k in kpis if k["observation"]["status"] == "warning"]

            if critical_kpis:
                insights.append({
                    "type": "critical",
                    "title": "Critical Performance Issues",
                    "message": f"{len(critical_kpis)} KPIs require immediate attention",
                    "kpis": [k["label"] for k in critical_kpis]
                })

            if warning_kpis:
                insights.append({
                    "type": "warning",
                    "title": "Performance Warnings",
                    "message": f"{len(warning_kpis)} KPIs are below target",
                    "kpis": [k["label"] for k in warning_kpis]
                })

            for rel in relationships:
                s = next((k for k in kpis if k["uri"] == rel["source"]), None)
                t = next((k for k in kpis if k["uri"] == rel["target"]), None)
                if s and t:
                    if (s["observation"]["status"] in ["critical", "warning"] and
                        t["observation"]["status"] in ["critical", "warning"]):
                        insights.append({
                            "type": "causal",
                            "title": "Causal Relationship Detected",
                            "message": f"{s['label']} may be affecting {t['label']}",
                            "relationship": rel["relationship"]
                        })

            print(f"✅ Generated {len(insights)} insights")
            return insights

        except Exception as e:
            print("❌ ERROR in generate_insights():", e)
            traceback.print_exc()
            return []

    # ---------------------------------------------------------
    #  Graph data for visualization
    # ---------------------------------------------------------
    def get_network_graph_data(self) -> Dict[str, Any]:
        print("⚙️ Running get_network_graph_data() ...")
        try:
            kpis = self.get_all_kpis()
            relationships = self.get_kpi_relationships()

            nodes = [{
                "id": k["uri"],
                "label": k["label"],
                "domain": k["domain"],
                "goal": k["goal"],
                "value": k["observation"]["value"],
                "target": k["target"],
                "status": k["observation"]["status"],
                "unit": k["unit"]
            } for k in kpis]

            edges = [{
                "source": r["source"],
                "target": r["target"],
                "type": r["relationship"]
            } for r in relationships]

            print(f"✅ Graph built with {len(nodes)} nodes and {len(edges)} edges")
            return {"nodes": nodes, "edges": edges}

        except Exception as e:
            print("❌ ERROR in get_network_graph_data():", e)
            traceback.print_exc()
            return {"nodes": [], "edges": []}


# ---------------------------------------------------------
# Initialize global reasoner instance
# ---------------------------------------------------------
print("🧠 Initializing Hospital KPI Reasoner global instance...")
reasoner = HospitalKPIReasoner("ontology/hospital_kpi.owl", "ontology/kpi_data.ttl")
print("✅ Hospital KPI Reasoner ready.")
