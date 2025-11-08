import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np

class KPIDataGenerator:
    def __init__(self):
        self.departments = [
            "Emergency Department",
            "Radiology Department", 
            "Surgery Department",
            "Pharmacy Department",
            "Laboratory Services",
            "Intensive Care Unit",
            "Cardiology Department",
            "Oncology Department"
        ]
        
        self.kpi_templates = {
            "Emergency Department": [
                {"name": "Average Wait Time", "unit": "minutes", "target": 30, "min": 15, "max": 90},
                {"name": "Patient Satisfaction", "unit": "percentage", "target": 85, "min": 60, "max": 95},
                {"name": "Triage Accuracy", "unit": "percentage", "target": 95, "min": 85, "max": 98},
                {"name": "Bed Occupancy Rate", "unit": "percentage", "target": 75, "min": 60, "max": 95}
            ],
            "Radiology Department": [
                {"name": "Report Turnaround Time", "unit": "hours", "target": 24, "min": 12, "max": 48},
                {"name": "Image Quality Score", "unit": "percentage", "target": 90, "min": 80, "max": 98},
                {"name": "Equipment Utilization", "unit": "percentage", "target": 80, "min": 60, "max": 95},
                {"name": "Radiation Dose", "unit": "mSv", "target": 10, "min": 5, "max": 25}
            ],
            "Surgery Department": [
                {"name": "Surgical Site Infections", "unit": "percentage", "target": 2, "min": 0.5, "max": 5},
                {"name": "Operating Room Utilization", "unit": "percentage", "target": 75, "min": 60, "max": 90},
                {"name": "Average Length of Stay", "unit": "days", "target": 4.5, "min": 3, "max": 8},
                {"name": "Mortality Rate", "unit": "percentage", "target": 1.5, "min": 0.5, "max": 4}
            ],
            "Pharmacy Department": [
                {"name": "Medication Error Rate", "unit": "percentage", "target": 0.5, "min": 0.1, "max": 2},
                {"name": "Prescription Accuracy", "unit": "percentage", "target": 98, "min": 95, "max": 99.5},
                {"name": "Inventory Turnover", "unit": "times/year", "target": 12, "min": 8, "max": 20},
                {"name": "Drug Interaction Alerts", "unit": "percentage", "target": 1, "min": 0.2, "max": 3}
            ],
            "Laboratory Services": [
                {"name": "Test Turnaround Time", "unit": "hours", "target": 4, "min": 2, "max": 8},
                {"name": "Sample Rejection Rate", "unit": "percentage", "target": 2, "min": 0.5, "max": 5},
                {"name": "Quality Control Pass Rate", "unit": "percentage", "target": 98, "min": 95, "max": 100},
                {"name": "Equipment Downtime", "unit": "percentage", "target": 5, "min": 1, "max": 15}
            ],
            "Intensive Care Unit": [
                {"name": "Central Line Infections", "unit": "per 1000 days", "target": 1, "min": 0, "max": 3},
                {"name": "Ventilator Associated Pneumonia", "unit": "per 1000 days", "target": 2, "min": 0, "max": 5},
                {"name": "ICU Mortality Rate", "unit": "percentage", "target": 8, "min": 5, "max": 15},
                {"name": "Length of ICU Stay", "unit": "days", "target": 3.5, "min": 2, "max": 7}
            ],
            "Cardiology Department": [
                {"name": "Door to Balloon Time", "unit": "minutes", "target": 90, "min": 60, "max": 120},
                {"name": "Cardiac Catheterization", "unit": "percentage", "target": 95, "min": 90, "max": 98},
                {"name": "Readmission Rate", "unit": "percentage", "target": 12, "min": 8, "max": 20},
                {"name": "Ejection Fraction Improvement", "unit": "percentage", "target": 15, "min": 10, "max": 25}
            ],
            "Oncology Department": [
                {"name": "Chemotherapy Administration", "unit": "percentage", "target": 95, "min": 90, "max": 98},
                {"name": "Treatment Response Rate", "unit": "percentage", "target": 70, "min": 60, "max": 85},
                {"name": "Adverse Event Rate", "unit": "percentage", "target": 15, "min": 10, "max": 25},
                {"name": "Clinical Trial Enrollment", "unit": "percentage", "target": 20, "min": 15, "max": 30}
            ]
        }
        
        self.performance_domains = [
            "Operational Efficiency",
            "Patient Safety", 
            "Quality of Care",
            "Financial Performance",
            "Staff Satisfaction",
            "Patient Experience"
        ]
        
        self.strategic_goals = [
            "Enhance Patient Experience",
            "Achieve Operational Excellence",
            "Ensure Clinical Quality",
            "Optimize Financial Performance",
            "Develop Staff Excellence",
            "Advance Medical Innovation"
        ]
    
    def generate_current_kpi_data(self) -> Dict[str, Any]:
        """Generate current KPI data for all departments"""
        current_data = {
            "timestamp": datetime.now().isoformat(),
            "hospital": "General Hospital",
            "departments": []
        }
        
        for dept_name in self.departments[:4]:  # Limit to first 4 departments for demo
            department_data = {
                "name": dept_name,
                "kpis": []
            }
            
            if dept_name in self.kpi_templates:
                for kpi_template in self.kpi_templates[dept_name]:
                    # Generate realistic current value based on target
                    target = kpi_template["target"]
                    min_val = kpi_template["min"]
                    max_val = kpi_template["max"]
                    
                    # Generate value with some variance around target
                    variance = (max_val - min_val) * 0.1  # 10% variance
                    current_value = np.random.normal(target, variance)
                    current_value = max(min_val, min(max_val, current_value))
                    
                    # Determine status based on performance
                    performance_ratio = (current_value / target) * 100
                    
                    if kpi_template["unit"] in ["percentage", "per 1000 days"]:
                        # For positive metrics (higher is better)
                        if performance_ratio >= 95:
                            status = "excellent"
                        elif performance_ratio >= 80:
                            status = "good"
                        elif performance_ratio >= 60:
                            status = "warning"
                        else:
                            status = "critical"
                    else:
                        # For negative metrics (lower is better)
                        if performance_ratio <= 105:
                            status = "excellent"
                        elif performance_ratio <= 125:
                            status = "good"
                        elif performance_ratio <= 150:
                            status = "warning"
                        else:
                            status = "critical"
                    
                    kpi_data = {
                        "name": kpi_template["name"],
                        "current_value": round(current_value, 2),
                        "target_value": target,
                        "unit": kpi_template["unit"],
                        "status": status,
                        "performance_ratio": round(performance_ratio, 1),
                        "trend": self._generate_trend(),
                        "last_updated": datetime.now().isoformat()
                    }
                    
                    department_data["kpis"].append(kpi_data)
            
            current_data["departments"].append(department_data)
        
        return current_data
    
    def _generate_trend(self) -> str:
        """Generate a random trend direction"""
        trends = ["improving", "stable", "declining", "fluctuating"]
        weights = [0.3, 0.3, 0.2, 0.2]  # More likely to be improving or stable
        return random.choices(trends, weights=weights)[0]
    
    def generate_historical_data(self, days: int = 30) -> Dict[str, Any]:
        """Generate historical KPI data for trend analysis"""
        historical_data = {
            "period": f"{days} days",
            "daily_data": []
        }
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            day_data = {
                "date": date.isoformat(),
                "departments": {}
            }
            
            for dept_name in self.departments[:4]:
                if dept_name in self.kpi_templates:
                    day_data["departments"][dept_name] = []
                    
                    for kpi_template in self.kpi_templates[dept_name]:
                        # Generate historical value with trend
                        base_value = kpi_template["target"]
                        trend_factor = 1 + (random.uniform(-0.1, 0.1) * (i / days))
                        noise = random.uniform(-0.05, 0.05)
                        
                        historical_value = base_value * trend_factor * (1 + noise)
                        historical_value = max(kpi_template["min"], 
                                             min(kpi_template["max"], historical_value))
                        
                        day_data["departments"][dept_name].append({
                            "name": kpi_template["name"],
                            "value": round(historical_value, 2)
                        })
            
            historical_data["daily_data"].append(day_data)
        
        return historical_data
    
    def generate_relationships(self) -> List[Dict[str, Any]]:
        """Generate causal relationships between KPIs"""
        relationships = []
        
        # Define key relationships based on healthcare logic
        key_relationships = [
            {
                "source": "Average Wait Time",
                "target": "Patient Satisfaction",
                "type": "influences",
                "strength": 0.8,
                "description": "Longer wait times decrease patient satisfaction"
            },
            {
                "source": "Triage Accuracy",
                "target": "Average Wait Time",
                "type": "influences", 
                "strength": 0.6,
                "description": "Better triage reduces unnecessary delays"
            },
            {
                "source": "Report Turnaround Time",
                "target": "Average Length of Stay",
                "type": "influences",
                "strength": 0.7,
                "description": "Faster reports enable quicker treatment decisions"
            },
            {
                "source": "Medication Error Rate",
                "target": "Average Length of Stay",
                "type": "influences",
                "strength": 0.5,
                "description": "Medication errors can extend hospital stays"
            },
            {
                "source": "Surgical Site Infections",
                "target": "Average Length of Stay",
                "type": "influences",
                "strength": 0.8,
                "description": "Infections significantly extend recovery time"
            },
            {
                "source": "Average Length of Stay",
                "target": "Bed Occupancy Rate",
                "type": "influences",
                "strength": 0.6,
                "description": "Longer stays increase bed occupancy"
            },
            {
                "source": "Image Quality Score",
                "target": "Diagnostic Accuracy",
                "type": "influences",
                "strength": 0.9,
                "description": "Better images lead to more accurate diagnoses"
            },
            {
                "source": "Prescription Accuracy",
                "target": "Medication Error Rate",
                "type": "influences",
                "strength": 0.7,
                "description": "Accurate prescriptions reduce medication errors"
            }
        ]
        
        # Add some random relationships for complexity
        for _ in range(12):  # Add 12 more relationships
            source_dept = random.choice(self.departments[:4])
            target_dept = random.choice(self.departments[:4])
            
            if source_dept in self.kpi_templates and target_dept in self.kpi_templates:
                source_kpi = random.choice(self.kpi_templates[source_dept])
                target_kpi = random.choice(self.kpi_templates[target_dept])
                
                if source_kpi != target_kpi:  # Avoid self-relationships
                    relationships.append({
                        "source": source_kpi["name"],
                        "target": target_kpi["name"],
                        "type": random.choice(["influences", "dependsOn"]),
                        "strength": round(random.uniform(0.1, 0.6), 2),
                        "description": f"Relationship between {source_kpi['name']} and {target_kpi['name']}"
                    })
        
        # Add key relationships (avoiding duplicates)
        for key_rel in key_relationships:
            if not any(rel["source"] == key_rel["source"] and 
                      rel["target"] == key_rel["target"] for rel in relationships):
                relationships.append(key_rel)
        
        return relationships
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """Generate intelligent insights based on generated data"""
        insights = [
            {
                "type": "performance",
                "severity": "medium",
                "title": "Emergency Department Wait Times",
                "message": "Average wait times have increased by 15% over the past week, potentially impacting patient satisfaction scores.",
                "recommendation": "Consider additional triage resources during peak hours",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "causal",
                "severity": "high", 
                "title": "Medication Error Cascade",
                "message": "Increased medication errors in Pharmacy are extending patient stays across multiple departments.",
                "recommendation": "Implement additional medication verification protocols",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "optimization",
                "severity": "low",
                "title": "Radiology Equipment Utilization",
                "message": "Equipment utilization is optimal, but there's opportunity to improve turnaround times during off-peak hours.",
                "recommendation": "Consider scheduling optimization for better resource allocation",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return insights
    
    def generate_strategic_goals(self) -> List[Dict[str, Any]]:
        """Generate strategic goals with progress tracking"""
        goals = []
        
        for goal_name in self.strategic_goals[:4]:  # Limit to 4 goals
            progress = random.uniform(65, 95)  # Realistic progress range
            
            goal = {
                "name": goal_name,
                "progress": round(progress, 1),
                "status": "on_track" if progress >= 80 else "needs_attention",
                "target_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "contributing_kpis": self._get_contributing_kpis(goal_name),
                "milestones": self._generate_milestones()
            }
            
            goals.append(goal)
        
        return goals
    
    def _get_contributing_kpis(self, goal_name: str) -> List[str]:
        """Get KPIs that contribute to a strategic goal"""
        # Map goals to relevant KPIs
        goal_kpi_mapping = {
            "Enhance Patient Experience": [
                "Patient Satisfaction", "Average Wait Time", "Triage Accuracy"
            ],
            "Achieve Operational Excellence": [
                "Average Length of Stay", "Bed Occupancy Rate", "Equipment Utilization"
            ],
            "Ensure Clinical Quality": [
                "Surgical Site Infections", "Medication Error Rate", "Mortality Rate"
            ],
            "Optimize Financial Performance": [
                "Equipment Utilization", "Inventory Turnover", "Operating Room Utilization"
            ]
        }
        
        return goal_kpi_mapping.get(goal_name, [])
    
    def _generate_milestones(self) -> List[Dict[str, Any]]:
        """Generate milestone data for strategic goals"""
        milestones = [
            {
                "name": "Q1 Review",
                "target_date": (datetime.now() + timedelta(days=90)).isoformat(),
                "status": random.choice(["completed", "in_progress", "pending"]),
                "progress": random.randint(0, 100)
            },
            {
                "name": "Mid-year Assessment", 
                "target_date": (datetime.now() + timedelta(days=180)).isoformat(),
                "status": random.choice(["in_progress", "pending"]),
                "progress": random.randint(0, 75)
            },
            {
                "name": "Annual Review",
                "target_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "status": "pending",
                "progress": 0
            }
        ]
        
        return milestones

# Initialize data generator
data_generator = KPIDataGenerator()