import rdflib
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class HospitalKPIReasoner:
    def __init__(self, ontology_path: str, data_path: str):
        self.graph = Graph()
        self.hospital = Namespace("http://hospital-kpi.org/ontology#")
        
        # Load ontology and data
        self.graph.parse(ontology_path, format="xml")
        self.graph.parse(data_path, format="turtle")
        
        # Initialize namespaces
        self.graph.bind("hospital", self.hospital)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)
        
    def get_all_kpis(self) -> List[Dict[str, Any]]:
        """Get all KPIs with their current observations"""
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
        return results
    
    def get_kpi_relationships(self) -> List[Dict[str, Any]]:
        """Get all KPI relationships (influences and dependsOn)"""
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
        return results
    
    def get_department_kpis(self, department_uri: str) -> List[Dict[str, Any]]:
        """Get all KPIs for a specific department"""
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
        """, initNs={"hospital": self.hospital})
        
        results = []
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
        return results
    
    def calculate_kpi_impact(self, kpi_uri: str, new_value: float) -> Dict[str, Any]:
        """Calculate the impact of changing a KPI value"""
        # Get current KPI data
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
        """, initNs={"hospital": self.hospital})
        
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
            return {"error": "KPI not found"}
        
        # Calculate impact on influenced KPIs
        influenced_kpis = self._get_influenced_kpis(kpi_uri)
        impact_analysis = {
            "kpi": kpi_data,
            "new_value": new_value,
            "change_percent": ((new_value - kpi_data["current_value"]) / kpi_data["current_value"]) * 100,
            "influenced_kpis": []
        }
        
        for influenced_kpi in influenced_kpis:
            # Simple linear impact model (can be enhanced with more sophisticated models)
            impact_factor = 0.1  # 10% influence by default
            projected_change = (new_value - kpi_data["current_value"]) * impact_factor
            
            impact_analysis["influenced_kpis"].append({
                "uri": influenced_kpi["uri"],
                "label": influenced_kpi["label"],
                "current_value": influenced_kpi["current_value"],
                "projected_change": projected_change,
                "projected_value": influenced_kpi["current_value"] + projected_change
            })
        
        return impact_analysis
    
    def _get_influenced_kpis(self, kpi_uri: str) -> List[Dict[str, Any]]:
        """Get KPIs that are influenced by the given KPI"""
        query = prepareQuery("""
            SELECT ?influenced_kpi ?label ?current_value
            WHERE {
                ?kpi hospital:influences ?influenced_kpi .
                ?influenced_kpi rdfs:label ?label ;
                                hospital:hasObservation ?obs .
                ?obs hospital:hasValue ?current_value .
                FILTER(?kpi = ?kpi_uri)
            }
        """, initNs={"hospital": self.hospital})
        
        results = []
        for row in self.graph.query(query, initBindings={'kpi_uri': URIRef(kpi_uri)}):
            results.append({
                "uri": str(row.influenced_kpi),
                "label": str(row.label),
                "current_value": float(row.current_value)
            })
        return results
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """Generate intelligent insights based on current KPI states"""
        kpis = self.get_all_kpis()
        insights = []
        
        # Find critical KPIs
        critical_kpis = [kpi for kpi in kpis if kpi["observation"]["status"] == "critical"]
        warning_kpis = [kpi for kpi in kpis if kpi["observation"]["status"] == "warning"]
        
        # Generate insights based on status patterns
        if critical_kpis:
            insights.append({
                "type": "critical",
                "title": "Critical Performance Issues",
                "message": f"{len(critical_kpis)} KPIs require immediate attention",
                "kpis": [kpi["label"] for kpi in critical_kpis],
                "recommendation": "Review operational processes and implement immediate corrective measures"
            })
        
        if warning_kpis:
            insights.append({
                "type": "warning",
                "title": "Performance Warnings",
                "message": f"{len(warning_kpis)} KPIs are below target",
                "kpis": [kpi["label"] for kpi in warning_kpis],
                "recommendation": "Monitor closely and consider preventive actions"
            })
        
        # Analyze relationships for causal insights
        relationships = self.get_kpi_relationships()
        
        # Find potential causal chains
        for rel in relationships:
            source_kpi = next((kpi for kpi in kpis if kpi["uri"] == rel["source"]), None)
            target_kpi = next((kpi for kpi in kpis if kpi["uri"] == rel["target"]), None)
            
            if source_kpi and target_kpi:
                if (source_kpi["observation"]["status"] in ["critical", "warning"] and 
                    target_kpi["observation"]["status"] in ["critical", "warning"]):
                    insights.append({
                        "type": "causal",
                        "title": "Causal Relationship Detected",
                        "message": f"{source_kpi['label']} may be affecting {target_kpi['label']}",
                        "relationship": rel["relationship"],
                        "recommendation": f"Address {source_kpi['label']} to improve {target_kpi['label']}"
                    })
        
        return insights
    
    def get_network_graph_data(self) -> Dict[str, Any]:
        """Get data formatted for network visualization"""
        kpis = self.get_all_kpis()
        relationships = self.get_kpi_relationships()
        
        # Create nodes
        nodes = []
        for kpi in kpis:
            nodes.append({
                "id": kpi["uri"],
                "label": kpi["label"],
                "domain": kpi["domain"],
                "goal": kpi["goal"],
                "value": kpi["observation"]["value"],
                "target": kpi["target"],
                "status": kpi["observation"]["status"],
                "unit": kpi["unit"]
            })
        
        # Create edges
        edges = []
        for rel in relationships:
            edges.append({
                "source": rel["source"],
                "target": rel["target"],
                "type": rel["relationship"]
            })
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def update_kpi_value(self, kpi_uri: str, new_value: float) -> bool:
        """Update a KPI value and create a new observation"""
        try:
            # Create new observation
            new_obs_uri = f"{kpi_uri}_obs_{int(datetime.now().timestamp())}"
            new_obs = URIRef(new_obs_uri)
            
            # Determine status based on target value
            query = prepareQuery("""
                SELECT ?target
                WHERE {
                    ?kpi hospital:targetValue ?target .
                    FILTER(?kpi = ?kpi_uri)
                }
            """, initNs={"hospital": self.hospital})
            
            target_value = None
            for row in self.graph.query(query, initBindings={'kpi_uri': URIRef(kpi_uri)}):
                target_value = float(row.target)
                break
            
            if target_value is None:
                return False
            
            # Calculate performance ratio to determine status
            performance_ratio = (new_value / target_value) * 100
            
            if performance_ratio >= 95:
                status = "excellent"
            elif performance_ratio >= 80:
                status = "good"
            elif performance_ratio >= 60:
                status = "warning"
            else:
                status = "critical"
            
            # Add new observation to graph
            self.graph.add((new_obs, RDF.type, self.hospital.PerformanceObservation))
            self.graph.add((new_obs, self.hospital.hasValue, Literal(new_value, datatype=XSD.float)))
            self.graph.add((new_obs, self.hospital.status, Literal(status)))
            self.graph.add((new_obs, self.hospital.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
            
            # Link observation to KPI
            self.graph.add((URIRef(kpi_uri), self.hospital.hasObservation, new_obs))
            
            return True
        except Exception as e:
            print(f"Error updating KPI value: {e}")
            return False

# Initialize reasoner instance
reasoner = HospitalKPIReasoner("ontology/hospital_kpi.owl", "ontology/kpi_data.ttl")