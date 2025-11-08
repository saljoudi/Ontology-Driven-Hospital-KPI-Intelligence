import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import json
from services.reasoning_engine import reasoner

class KPIAnalytics:
    def __init__(self):
        self.correlation_matrix = {}
        self.causal_chains = {}
        self.historical_data = {}
        
    def calculate_correlations(self, kpi_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Calculate correlation coefficients between KPIs based on their relationships"""
        correlations = {}
        
        # Get KPI relationships from ontology
        relationships = reasoner.get_kpi_relationships()
        
        # Group KPIs by domain for domain-specific correlations
        domain_groups = {}
        for kpi in kpi_data:
            domain = kpi["domain"]
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(kpi)
        
        # Calculate correlations based on relationships
        for rel in relationships:
            source_kpi = rel["source"]
            target_kpi = rel["target"]
            relationship_type = rel["relationship"]
            
            # Assign correlation strength based on relationship type
            if relationship_type == "influences":
                correlation_strength = 0.7  # Strong positive correlation
            elif relationship_type == "dependsOn":
                correlation_strength = 0.8  # Very strong positive correlation
            else:
                correlation_strength = 0.5  # Moderate correlation
            
            # Store bidirectional correlation
            if source_kpi not in correlations:
                correlations[source_kpi] = {}
            if target_kpi not in correlations:
                correlations[target_kpi] = {}
                
            correlations[source_kpi][target_kpi] = correlation_strength
            correlations[target_kpi][source_kpi] = correlation_strength
        
        # Add domain-based correlations
        for domain, kpis in domain_groups.items():
            if len(kpis) > 1:
                for i, kpi1 in enumerate(kpis):
                    for j, kpi2 in enumerate(kpis[i+1:], i+1):
                        kpi1_uri = kpi1["uri"]
                        kpi2_uri = kpi2["uri"]
                        
                        if kpi1_uri not in correlations:
                            correlations[kpi1_uri] = {}
                        if kpi2_uri not in correlations:
                            correlations[kpi2_uri] = {}
                        
                        # Domain-based moderate correlation
                        correlations[kpi1_uri][kpi2_uri] = 0.4
                        correlations[kpi2_uri][kpi1_uri] = 0.4
        
        self.correlation_matrix = correlations
        return correlations
    
    def generate_causal_chains(self, kpi_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate causal chains showing how KPIs influence each other"""
        chains = []
        relationships = reasoner.get_kpi_relationships()
        
        # Build adjacency list for graph traversal
        graph = {}
        for rel in relationships:
            source = rel["source"]
            target = rel["target"]
            
            if source not in graph:
                graph[source] = []
            graph[source].append({
                "target": target,
                "type": rel["relationship"]
            })
        
        # Find all possible chains starting from each KPI
        for kpi in kpi_data:
            start_kpi = kpi["uri"]
            chains.extend(self._find_chains_from_source(graph, start_kpi, kpi_data))
        
        self.causal_chains = chains
        return chains
    
    def _find_chains_from_source(self, graph: Dict[str, List[Dict]], 
                                start: str, kpi_data: List[Dict[str, Any]], 
                                max_depth: int = 3) -> List[Dict[str, Any]]:
        """Find all causal chains starting from a given KPI"""
        chains = []
        
        def dfs(current: str, path: List[str], depth: int):
            if depth > max_depth or current not in graph:
                return
            
            for edge in graph[current]:
                next_kpi = edge["target"]
                new_path = path + [next_kpi]
                
                # Calculate chain impact
                chain_impact = self._calculate_chain_impact(new_path, kpi_data)
                
                chains.append({
                    "chain": new_path,
                    "relationships": [edge["type"] for edge in path_edges(new_path)],
                    "impact": chain_impact,
                    "length": len(new_path)
                })
                
                dfs(next_kpi, new_path, depth + 1)
        
        def path_edges(path: List[str]) -> List[Dict]:
            """Get edges for a path"""
            edges = []
            for i in range(len(path) - 1):
                if path[i] in graph:
                    for edge in graph[path[i]]:
                        if edge["target"] == path[i + 1]:
                            edges.append(edge)
                            break
            return edges
        
        dfs(start, [start], 1)
        return chains
    
    def _calculate_chain_impact(self, chain: List[str], kpi_data: List[Dict[str, Any]]) -> float:
        """Calculate the cumulative impact of a causal chain"""
        impact = 1.0
        
        for i in range(len(chain) - 1):
            source_uri = chain[i]
            target_uri = chain[i + 1]
            
            # Find current values
            source_kpi = next((kpi for kpi in kpi_data if kpi["uri"] == source_uri), None)
            target_kpi = next((kpi for kpi in kpi_data if kpi["uri"] == target_uri), None)
            
            if source_kpi and target_kpi:
                # Calculate performance ratio impact
                source_performance = source_kpi["observation"]["value"] / source_kpi["target"]
                target_performance = target_kpi["observation"]["value"] / target_kpi["target"]
                
                # Chain impact multiplies through the causal relationships
                impact *= abs(target_performance - source_performance) * 0.5
        
        return impact
    
    def generate_predictive_insights(self, kpi_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate predictive insights based on current trends and relationships"""
        insights = []
        
        # Analyze performance trends
        for kpi in kpi_data:
            current_value = kpi["observation"]["value"]
            target_value = kpi["target"]
            performance_ratio = (current_value / target_value) * 100
            
            if performance_ratio < 70:
                # Critical performance - high risk
                influenced_kpis = self._get_influenced_kpis(kpi["uri"], kpi_data)
                
                if influenced_kpis:
                    insights.append({
                        "type": "prediction",
                        "severity": "high",
                        "title": f"Risk Alert: {kpi['label']}",
                        "message": f"Poor performance in {kpi['label']} ({performance_ratio:.1f}% of target) may negatively impact {len(influenced_kpis)} related KPIs",
                        "affected_kpis": [ik["label"] for ik in influenced_kpis],
                        "recommendation": f"Immediate intervention required for {kpi['label']} to prevent cascade effects"
                    })
            
            elif performance_ratio > 120:
                # Overperformance - potential resource strain
                insights.append({
                    "type": "optimization",
                    "severity": "medium",
                    "title": f"Optimization Opportunity: {kpi['label']}",
                    "message": f"{kpi['label']} is performing {performance_ratio:.1f}% above target - consider resource reallocation",
                    "recommendation": "Review resource allocation for potential optimization"
                })
        
        # Analyze relationship patterns
        critical_chains = [chain for chain in self.causal_chains if chain["impact"] > 0.3]
        
        if critical_chains:
            worst_chain = max(critical_chains, key=lambda x: x["impact"])
            chain_labels = []
            for uri in worst_chain["chain"]:
                kpi = next((k for k in kpi_data if k["uri"] == uri), None)
                if kpi:
                    chain_labels.append(kpi["label"])
            
            insights.append({
                "type": "causal_chain",
                "severity": "high",
                "title": "Critical Causal Chain Identified",
                "message": f"High-impact causal chain detected: {' → '.join(chain_labels)}",
                "impact_score": worst_chain["impact"],
                "recommendation": "Focus intervention on the root cause of this causal chain"
            })
        
        return insights
    
    def _get_influenced_kpis(self, kpi_uri: str, kpi_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get KPIs that are influenced by the given KPI"""
        relationships = reasoner.get_kpi_relationships()
        influenced_uris = [rel["target"] for rel in relationships if rel["source"] == kpi_uri]
        
        return [kpi for kpi in kpi_data if kpi["uri"] in influenced_uris]
    
    def simulate_scenario(self, changes: Dict[str, float], kpi_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate the impact of multiple KPI changes"""
        simulation_results = {
            "original_values": {},
            "new_values": {},
            "impacts": {},
            "predicted_outcomes": []
        }
        
        # Store original values
        for kpi in kpi_data:
            simulation_results["original_values"][kpi["uri"]] = kpi["observation"]["value"]
        
        # Apply direct changes
        for kpi_uri, new_value in changes.items():
            simulation_results["new_values"][kpi_uri] = new_value
            
            # Calculate immediate impact
            impact_analysis = reasoner.calculate_kpi_impact(kpi_uri, new_value)
            simulation_results["impacts"][kpi_uri] = impact_analysis
        
        # Propagate changes through relationships
        propagation_results = self._propagate_changes(changes, kpi_data)
        simulation_results["predicted_outcomes"] = propagation_results
        
        # Calculate overall impact score
        total_impact = sum(abs(simulation_results["new_values"].get(uri, orig) - orig) 
                          for uri, orig in simulation_results["original_values"].items())
        
        simulation_results["overall_impact_score"] = total_impact / len(kpi_data)
        
        return simulation_results
    
    def _propagate_changes(self, changes: Dict[str, float], kpi_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Propagate changes through the KPI relationship network"""
        outcomes = []
        relationships = reasoner.get_kpi_relationships()
        
        # Create a dependency graph
        dependency_graph = {}
        for rel in relationships:
            source = rel["source"]
            target = rel["target"]
            
            if source not in dependency_graph:
                dependency_graph[source] = []
            dependency_graph[source].append({
                "target": target,
                "type": rel["relationship"]
            })
        
        # Propagate changes
        for changed_kpi, new_value in changes.items():
            self._propagate_single_change(changed_kpi, new_value, dependency_graph, 
                                        kpi_data, outcomes, set())
        
        return outcomes
    
    def _propagate_single_change(self, kpi_uri: str, new_value: float, 
                                dependency_graph: Dict[str, List[Dict]], 
                                kpi_data: List[Dict[str, Any]], 
                                outcomes: List[Dict[str, Any]], 
                                visited: set, depth: int = 0, max_depth: int = 3):
        """Recursively propagate a single KPI change through the network"""
        if depth > max_depth or kpi_uri in visited:
            return
        
        visited.add(kpi_uri)
        
        if kpi_uri in dependency_graph:
            for dependency in dependency_graph[kpi_uri]:
                target_kpi = dependency["target"]
                relationship_type = dependency["type"]
                
                # Calculate impact based on relationship type
                if relationship_type == "influences":
                    impact_factor = 0.3  # 30% influence
                elif relationship_type == "dependsOn":
                    impact_factor = 0.5  # 50% influence
                else:
                    impact_factor = 0.1  # 10% influence
                
                # Find original target value
                target_kpi_data = next((kpi for kpi in kpi_data if kpi["uri"] == target_kpi), None)
                if target_kpi_data:
                    original_value = target_kpi_data["observation"]["value"]
                    
                    # Calculate propagated change
                    change_amount = (new_value - original_value) * impact_factor
                    projected_value = original_value + change_amount
                    
                    outcomes.append({
                        "kpi_uri": target_kpi,
                        "kpi_label": target_kpi_data["label"],
                        "original_value": original_value,
                        "projected_value": projected_value,
                        "change_amount": change_amount,
                        "influenced_by": kpi_uri,
                        "relationship_type": relationship_type,
                        "depth": depth + 1
                    })
                    
                    # Continue propagation
                    self._propagate_single_change(target_kpi, projected_value, 
                                                dependency_graph, kpi_data, 
                                                outcomes, visited, depth + 1, max_depth)

# Initialize analytics instance
analytics = KPIAnalytics()