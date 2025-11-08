from flask import Blueprint, jsonify, request
from services.reasoning_engine import reasoner
from services.analytics import analytics
from services.data_generator import data_generator
from datetime import datetime
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/kpis', methods=['GET'])
def get_kpis():
    """Get all KPIs with their current observations and ontology context"""
    try:
        kpis = reasoner.get_all_kpis()
        
        # Add additional context from data generator
        current_data = data_generator.generate_current_kpi_data()
        
        # Enrich KPI data with department information
        enriched_kpis = []
        for kpi in kpis:
            enriched_kpi = kpi.copy()
            enriched_kpi["department"] = "Emergency Department"  # Simplified for demo
            enriched_kpi["domain_name"] = "Operational Efficiency"  # Simplified
            enriched_kpi["goal_name"] = "Enhance Patient Experience"  # Simplified
            enriched_kpis.append(enriched_kpi)
        
        return jsonify({
            "success": True,
            "data": enriched_kpis,
            "count": len(enriched_kpis),
            "timestamp": current_data["timestamp"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve KPI data"
        }), 500

@api_bp.route('/api/reasoning', methods=['POST'])
def run_reasoning():
    """Run semantic reasoning and return insights"""
    try:
        # Get optional parameters
        params = request.get_json() or {}
        focus_area = params.get('focus_area', 'all')
        
        # Get KPI data
        kpis = reasoner.get_all_kpis()
        
        # Calculate correlations
        correlations = analytics.calculate_correlations(kpis)
        
        # Generate causal chains
        causal_chains = analytics.generate_causal_chains(kpis)
        
        # Generate insights
        insights = reasoner.generate_insights()
        
        # Add predictive insights
        predictive_insights = analytics.generate_predictive_insights(kpis)
        
        all_insights = insights + predictive_insights
        
        # Filter by focus area if specified
        if focus_area != 'all':
            all_insights = [insight for insight in all_insights 
                          if focus_area.lower() in insight.get('title', '').lower()]
        
        return jsonify({
            "success": True,
            "data": {
                "correlations": correlations,
                "causal_chains": causal_chains,
                "insights": all_insights,
                "reasoning_timestamp": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to run reasoning engine"
        }), 500

@api_bp.route('/api/graph', methods=['GET'])
def get_network_graph():
    """Return network graph data for visualization"""
    try:
        graph_data = reasoner.get_network_graph_data()
        
        # Add additional metadata
        for node in graph_data["nodes"]:
            node["department"] = "Emergency Department"  # Simplified
            node["domain_name"] = "Operational Efficiency"  # Simplified
            node["goal_name"] = "Enhance Patient Experience"  # Simplified
            
            # Add color based on status
            status_colors = {
                "excellent": "#059669",  # green
                "good": "#0891b2",       # teal
                "warning": "#f59e0b",    # amber
                "critical": "#dc2626"    # red
            }
            node["color"] = status_colors.get(node["status"], "#64748b")
            
            # Add size based on performance deviation
            performance_ratio = node["value"] / node["target"]
            if performance_ratio < 0.7 or performance_ratio > 1.3:
                node["size"] = 25  # Larger for significant deviations
            else:
                node["size"] = 15  # Normal size
        
        # Add edge weights
        for edge in graph_data["edges"]:
            edge["weight"] = 2 if edge["type"] == "dependsOn" else 1
            edge["color"] = "#2563eb" if edge["type"] == "influences" else "#ea580c"
        
        return jsonify({
            "success": True,
            "data": graph_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to generate network graph"
        }), 500

@api_bp.route('/api/simulate', methods=['POST'])
def run_simulation():
    """Run what-if simulation and return results"""
    try:
        simulation_data = request.get_json()
        
        if not simulation_data or 'changes' not in simulation_data:
            return jsonify({
                "success": False,
                "message": "Simulation changes are required"
            }), 400
        
        changes = simulation_data['changes']
        kpis = reasoner.get_all_kpis()
        
        # Run simulation
        simulation_results = analytics.simulate_scenario(changes, kpis)
        
        # Add explanatory text for major impacts
        for uri, impact in simulation_results['impacts'].items():
            if impact.get('influenced_kpis'):
                kpi_label = impact['kpi']['label']
                change_percent = impact['change_percent']
                
                if abs(change_percent) > 10:  # Significant change
                    affected_labels = [k['label'] for k in impact['influenced_kpis'][:3]]
                    impact['explanation'] = f"Changing {kpi_label} by {change_percent:.1f}% will affect {len(impact['influenced_kpis'])} related KPIs including {', '.join(affected_labels)}"
        
        return jsonify({
            "success": True,
            "data": simulation_results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to run simulation"
        }), 500

@api_bp.route('/api/insights', methods=['GET'])
def get_insights():
    """Get real-time insights and recommendations"""
    try:
        # Get current KPI data
        kpis = reasoner.get_all_kpis()
        
        # Generate insights from reasoner
        insights = reasoner.generate_insights()
        
        # Add predictive insights
        predictive_insights = analytics.generate_predictive_insights(kpis)
        
        all_insights = insights + predictive_insights
        
        # Sort by severity
        severity_order = {"high": 3, "medium": 2, "low": 1}
        all_insights.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 0), reverse=True)
        
        # Add timestamp and source
        for insight in all_insights:
            insight["timestamp"] = datetime.now().isoformat()
            insight["source"] = "ontology_reasoning"
        
        return jsonify({
            "success": True,
            "data": {
                "insights": all_insights,
                "count": len(all_insights),
                "last_updated": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to generate insights"
        }), 500

@api_bp.route('/api/departments', methods=['GET'])
def get_departments():
    """Get all departments with their KPIs"""
    try:
        current_data = data_generator.generate_current_kpi_data()
        
        # Add department metadata
        for dept in current_data["departments"]:
            dept["id"] = dept["name"].lower().replace(" ", "_")
            dept["status"] = "operational"
            dept["staff_count"] = random.randint(20, 200)  # Simulated staff count
            dept["bed_count"] = random.randint(10, 50) if "emergency" in dept["name"].lower() or "surgery" in dept["name"].lower() else 0
            
            # Calculate department overall performance
            if dept["kpis"]:
                avg_performance = sum(kpi["performance_ratio"] for kpi in dept["kpis"]) / len(dept["kpis"])
                dept["overall_performance"] = round(avg_performance, 1)
                
                if avg_performance >= 90:
                    dept["performance_status"] = "excellent"
                elif avg_performance >= 75:
                    dept["performance_status"] = "good"
                elif avg_performance >= 60:
                    dept["performance_status"] = "warning"
                else:
                    dept["performance_status"] = "critical"
        
        return jsonify({
            "success": True,
            "data": current_data["departments"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve department data"
        }), 500

@api_bp.route('/api/historical', methods=['GET'])
def get_historical_data():
    """Get historical KPI data for trend analysis"""
    try:
        days = request.args.get('days', 30, type=int)
        historical_data = data_generator.generate_historical_data(days)
        
        return jsonify({
            "success": True,
            "data": historical_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve historical data"
        }), 500

@api_bp.route('/api/strategic-goals', methods=['GET'])
def get_strategic_goals():
    """Get strategic goals with progress tracking"""
    try:
        strategic_goals = data_generator.generate_strategic_goals()
        
        # Add progress calculation based on contributing KPIs
        for goal in strategic_goals:
            contributing_kpis = goal.get("contributing_kpis", [])
            if contributing_kpis:
                # Simulate progress based on KPI performance
                goal["calculated_progress"] = goal["progress"] + random.uniform(-5, 5)
                goal["calculated_progress"] = max(0, min(100, goal["calculated_progress"]))
            
            # Add risk assessment
            if goal["progress"] < 70:
                goal["risk_level"] = "high"
            elif goal["progress"] < 85:
                goal["risk_level"] = "medium"
            else:
                goal["risk_level"] = "low"
        
        return jsonify({
            "success": True,
            "data": strategic_goals
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve strategic goals"
        }), 500

@api_bp.route('/api/kpi/<kpi_id>/update', methods=['POST'])
def update_kpi_value(kpi_id):
    """Update a specific KPI value"""
    try:
        update_data = request.get_json()
        
        if not update_data or 'value' not in update_data:
            return jsonify({
                "success": False,
                "message": "New value is required"
            }), 400
        
        new_value = float(update_data['value'])
        
        # Update in reasoner (simplified - in real implementation would update RDF)
        success = reasoner.update_kpi_value(f"http://hospital-kpi.org/ontology#{kpi_id}", new_value)
        
        if success:
            return jsonify({
                "success": True,
                "message": f"KPI {kpi_id} updated successfully",
                "new_value": new_value
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Failed to update KPI {kpi_id}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to update KPI value"
        }), 500

@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "reasoning_engine": "active",
            "analytics_engine": "active",
            "data_generator": "active"
        }
    })

# Error handler for API
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Resource not found",
        "message": "The requested API endpoint does not exist"
    }), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An unexpected error occurred while processing your request"
    }), 500

from datetime import datetime