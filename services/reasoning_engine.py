# ==============================================================
# 🧠 Ontology-Driven Hospital KPI Reasoning Engine
# Full Functional Version with Debug and Simulation Logic
# ==============================================================

import os
import traceback
import json
from datetime import datetime
from typing import Dict, List, Any
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, Literal, XSD
from rdflib.plugins.sparql import prepareQuery


class HospitalKPIReasoner:
    """
    Semantic reasoning engine for hospital KPI ontology.
    Provides KPI retrieval, causal analysis, and simulation-based insight generation.
    """

    def __init__(self, ontology_path: str, data_path: str):
        print("\n🧠 Initializing Hospital KPI Reasoner global instance...")
        print("\n🔍 === HOSPITAL KPI REASONER STARTUP DEBUG ===")

        self.ontology_path = ontology_path
        self.data_path = data_path

        ontology_full = os.path.join(os.getcwd(), ontology_path)
        data_full = os.path.join(os.getcwd(), data_path)

        print(f"🧩 Working directory: {os.getcwd()}")
        print(f"📂 Ontology path arg: {ontology_path}")
        print(f"📂 Data path arg: {data_path}")
        print(f"📍 Ontology full path: {ontology_full}")
        print(f"📍 Data full path: {data_full}")
        print(f"✅ Ontology file exists? {os.path.exists(ontology_full)}")
        print(f"✅ Data file exists? {os.path.exists(data_full)}")

        try:
            self.graph = Graph()
            self.hospital = Namespace("http://hospital-kpi.org/ontology#")

            # Load ontology
            print("🧠 Parsing ontology file...")
            self.graph.parse(ontology_full, format="xml")
            print("✅ Ontology parsed successfully!")

            # Load data
            print("🧠 Parsing data file...")
            self.graph.parse(data_full, format="turtle")
            print("✅ Data parsed successfully!")

            print(f"📊 Total triples loaded: {len(self.graph)}")
            for s, p, o in list(self.graph)[:6]:
                print(f"   • {s} {p} {o}")

            print("🔍 === DEBUG COMPLETE ===\n")
            print("✅ Hospital KPI Reasoner ready.\n")

        except Exception as e:
            print("❌ ERROR during ontology/data loading:")
            traceback.print_exc()
            raise e

    # ----------------------------------------------------------
    # Core KPI Queries
    # ----------------------------------------------------------

    def get_all_kpis(self) -> List[Dict[str, Any]]:
        """Retrieve all KPIs with their metadata and latest observations"""
        print("🔎 Querying all KPIs...")
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
        """, initNs={"hospital": self.hospital, "rdfs": RDFS})

        results = []
        try:
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
        except Exception as e:
            print("❌ SPARQL error in get_all_kpis:", e)
        return results

    def get_kpi_relationships(self) -> List[Dict[str, Any]]:
        """Retrieve all KPI-to-KPI relationships"""
        print("🔎 Querying KPI relationships...")
        query = prepareQuery("""
            SELECT ?kpi1 ?kpi2 ?relationship
            WHERE {
                { ?kpi1 hospital:influences ?kpi2 . BIND("influences" as ?relationship) }
                UNION
                { ?kpi1 hospital:dependsOn ?kpi2 . BIND("dependsOn" as ?relationship) }
            }
        """, initNs={"hospital": self.hospital})

        results = []
        try:
            for row in self.graph.query(query):
                results.append({
                    "source": str(row.kpi1),
                    "target": str(row.kpi2),
                    "relationship": str(row.relationship)
                })
            print(f"✅ Found {len(results)} KPI relationships")
        except Exception as e:
            print("❌ SPARQL error in get_kpi_relationships:", e)
        return results

    # ----------------------------------------------------------
    # Department Queries
    # ----------------------------------------------------------

    def get_department_kpis(self, department_uri: str) -> List[Dict[str, Any]]:
        """Return all KPIs linked to a department"""
        query = prepareQuery("""
            SELECT ?kpi ?label ?obs ?value ?status
            WHERE {
                ?dept a hospital:Department ;
                      hospital:hasKPI ?kpi .
                ?kpi rdfs:label ?label ;
                     hospital:hasObservation ?obs .
                ?obs hospital:hasValue ?value ;
                     hospital:status ?status .
                FILTER(?dept = ?department)
            }
        """, initNs={"hospital": self.hospital, "rdfs": RDFS})

        results = []
        try:
            for row in self.graph.query(query, initBindings={'department': URIRef(department_uri)}):
                results.append({
                    "uri": str(row.kpi),
                    "label": str(row.label),
                    "observation": {
                        "uri": str(row.obs),
                        "value": float(row.value),
                        "status": str(row.status)
                    }
                })
        except Exception as e:
            print("❌ Error fetching department KPIs:", e)
        return results

    # ----------------------------------------------------------
    # Simulation and Impact Reasoning
    # ----------------------------------------------------------

    def _get_influenced_kpis(self, kpi_uri: str) -> List[Dict[str, Any]]:
        """Internal helper: get KPIs influenced by a given KPI"""
        query = prepareQuery("""
            SELECT ?influenced_kpi ?label ?current_value
            WHERE {
                ?kpi hospital:influences ?influenced_kpi .
                ?influenced_kpi rdfs:label ?label ;
                                hospital:hasObservation ?obs .
                ?obs hospital:hasValue ?current_value .
                FILTER(?kpi = ?kpi_uri)
            }
        """, initNs={"hospital": self.hospital, "rdfs": RDFS})

        results = []
        try:
            for row in self.graph.query(query, initBindings={'kpi_uri': URIRef(kpi_uri)}):
                results.append({
                    "uri": str(row.influenced_kpi),
                    "label": str(row.label),
                    "current_value": float(row.current_value)
                })
        except Exception as e:
            print("❌ Error in _get_influenced_kpis:", e)
        return results

    def calculate_kpi_impact(self, kpi_uri: str, new_value: float) -> Dict[str, Any]:
        """Simulate how changing one KPI might impact others"""
        print(f"🧮 Simulating impact for KPI: {kpi_uri} new_value={new_value}")

        query = prepareQuery("""
            SELECT ?label ?target ?unit ?current_value
            WHERE {
                ?kpi rdfs:label ?label ;
                     hospital:targetValue ?target ;
                     hospital:unit ?unit ;
                     hospital:hasObservation ?obs .
                ?obs hospital:hasValue ?current_value .
                FILTER(?kpi = ?kpi_uri)
            }
        """, initNs={"hospital": self.hospital, "rdfs": RDFS})

        kpi_data = None
        for row in self.graph.query(query, initBindings={'kpi_uri': URIRef(kpi_uri)}):
            kpi_data = {
                "label": str(row.label),
                "target": float(row.target),
                "unit": str(row.unit),
                "current_value": float(row.current_value)
            }
            break

        if not kpi_data:
            print("⚠️ KPI not found")
            return {"error": "KPI not found"}

        # Calculate base change %
        change_pct = ((new_value - kpi_data["current_value"]) /
                      kpi_data["current_value"]) * 100

        influenced_kpis = self._get_influenced_kpis(kpi_uri)
        impact_analysis = {
            "kpi": kpi_data,
            "new_value": new_value,
            "change_percent": round(change_pct, 2),
            "influenced_kpis": []
        }

        for inf in influenced_kpis:
            projected_change = (new_value - kpi_data["current_value"]) * 0.1
            impact_analysis["influenced_kpis"].append({
                "uri": inf["uri"],
                "label": inf["label"],
                "current_value": inf["current_value"],
                "projected_change": round(projected_change, 2),
                "projected_value": round(inf["current_value"] + projected_change, 2)
            })

        print(f"✅ Impact simulation complete for {len(influenced_kpis)} influenced KPIs.")
        return impact_analysis

    # ----------------------------------------------------------
    # Insight Generation
    # ----------------------------------------------------------

    def generate_insights(self) -> List[Dict[str, Any]]:
        """Generate high-level performance insights"""
        print("🧠 Generating semantic insights...")
        kpis = self.get_all_kpis()
        relationships = self.get_kpi_relationships()

        insights = []
        critical = [k for k in kpis if k["observation"]["status"] == "critical"]
        warning = [k for k in kpis if k["observation"]["status"] == "warning"]

        if critical:
            insights.append({
                "type": "critical",
                "title": "Critical Performance Issues",
                "message": f"{len(critical)} KPIs in critical state.",
                "kpis": [k["label"] for k in critical],
                "recommendation": "Immediate corrective actions required."
            })

        if warning:
            insights.append({
                "type": "warning",
                "title": "Performance Warnings",
                "message": f"{len(warning)} KPIs below optimal threshold.",
                "kpis": [k["label"] for k in warning],
                "recommendation": "Monitor these KPIs closely."
            })

        # Causal relationship insights
        for rel in relationships:
            src = next((k for k in kpis if k["uri"] == rel["source"]), None)
            tgt = next((k for k in kpis if k["uri"] == rel["target"]), None)
            if src and tgt:
                if src["observation"]["status"] in ["critical", "warning"] and \
                   tgt["observation"]["status"] in ["critical", "warning"]:
                    insights.append({
                        "type": "causal",
                        "title": "Causal Chain Detected",
                        "message": f"{src['label']} may be affecting {tgt['label']}",
                        "relationship": rel["relationship"],
                        "recommendation": f"Address {src['label']} to improve {tgt['label']}."
                    })

        print(f"✅ Generated {len(insights)} insights")
        return insights

    # ----------------------------------------------------------
    # KPI Update and Real-Time Observation Creation
    # ----------------------------------------------------------

    def update_kpi_value(self, kpi_uri: str, new_value: float) -> bool:
        """Create new observation for a KPI"""
        try:
            print(f"✏️ Updating KPI {kpi_uri} with new value {new_value}")
            new_obs_uri = f"{kpi_uri}_obs_{int(datetime.now().timestamp())}"
            new_obs = URIRef(new_obs_uri)

            query = prepareQuery("""
                SELECT ?target
                WHERE { ?kpi hospital:targetValue ?target . FILTER(?kpi = ?kpi_uri) }
            """, initNs={"hospital": self.hospital})

            target_val = None
            for row in self.graph.query(query, initBindings={'kpi_uri': URIRef(kpi_uri)}):
                target_val = float(row.target)
                break

            if target_val is None:
                print("⚠️ KPI target not found.")
                return False

            ratio = (new_value / target_val) * 100
            if ratio >= 95:
                status = "excellent"
            elif ratio >= 80:
                status = "good"
            elif ratio >= 60:
                status = "warning"
            else:
                status = "critical"

            # Insert into graph
            self.graph.add((new_obs, RDF.type, self.hospital.PerformanceObservation))
            self.graph.add((new_obs, self.hospital.hasValue, Literal(new_value, datatype=XSD.float)))
            self.graph.add((new_obs, self.hospital.status, Literal(status)))
            self.graph.add((new_obs, self.hospital.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
            self.graph.add((URIRef(kpi_uri), self.hospital.hasObservation, new_obs))

            print(f"✅ KPI {kpi_uri} updated successfully (status={status})")
            return True

        except Exception as e:
            print("❌ Error updating KPI:", e)
            traceback.print_exc()
            return False

    # ----------------------------------------------------------
    # Graph Data for Visualization
    # ----------------------------------------------------------

    def get_network_graph_data(self) -> Dict[str, Any]:
        """Return KPI network graph structure for visualization"""
        print("🌐 Building KPI network graph data...")
        kpis = self.get_all_kpis()
        rels = self.get_kpi_relationships()

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

        edges = [{"source": r["source"], "target": r["target"], "type": r["relationship"]} for r in rels]

        print(f"✅ Network graph ready with {len(nodes)} nodes and {len(edges)} edges.")
        return {"nodes": nodes, "edges": edges}


# ==============================================================
# Initialize Singleton Instance
# ==============================================================

reasoner = HospitalKPIReasoner("ontology/hospital_kpi.owl", "ontology/kpi_data.ttl")
