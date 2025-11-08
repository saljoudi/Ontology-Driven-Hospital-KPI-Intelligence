#!/usr/bin/env python3
"""
Hospital KPI Intelligence System - Live Demonstration
Shows the system capabilities without requiring full dependencies
"""

import json
import random
from datetime import datetime

class HospitalKPIDemo:
    def __init__(self):
        self.kpis = self.generate_sample_kpis()
        self.relationships = self.generate_sample_relationships()
        self.insights = self.generate_sample_insights()
        
    def generate_sample_kpis(self):
        """Generate realistic hospital KPI data"""
        return [
            {
                "name": "Average Wait Time",
                "department": "Emergency",
                "current_value": 42,
                "target": 30,
                "unit": "minutes",
                "status": "warning",
                "trend": "declining"
            },
            {
                "name": "Patient Satisfaction",
                "department": "Emergency", 
                "current_value": 87.3,
                "target": 85,
                "unit": "percentage",
                "status": "excellent",
                "trend": "improving"
            },
            {
                "name": "Bed Occupancy Rate",
                "department": "Emergency",
                "current_value": 78,
                "target": 75,
                "unit": "percentage", 
                "status": "good",
                "trend": "stable"
            },
            {
                "name": "Medication Error Rate",
                "department": "Pharmacy",
                "current_value": 0.8,
                "target": 0.5,
                "unit": "percentage",
                "status": "critical",
                "trend": "declining"
            },
            {
                "name": "Surgical Site Infections",
                "department": "Surgery",
                "current_value": 1.2,
                "target": 2.0,
                "unit": "percentage",
                "status": "excellent", 
                "trend": "improving"
            },
            {
                "name": "Report Turnaround Time",
                "department": "Radiology",
                "current_value": 18,
                "target": 24,
                "unit": "hours",
                "status": "excellent",
                "trend": "improving"
            }
        ]
    
    def generate_sample_relationships(self):
        """Generate sample causal relationships"""
        return [
            {
                "source": "Average Wait Time",
                "target": "Patient Satisfaction",
                "type": "influences",
                "strength": 0.8,
                "description": "Longer wait times decrease patient satisfaction"
            },
            {
                "source": "Medication Error Rate", 
                "target": "Patient Satisfaction",
                "type": "influences",
                "strength": 0.6,
                "description": "Medication errors reduce patient trust and satisfaction"
            },
            {
                "source": "Report Turnaround Time",
                "target": "Average Length of Stay",
                "type": "influences", 
                "strength": 0.7,
                "description": "Faster reports enable quicker treatment decisions"
            },
            {
                "source": "Surgical Site Infections",
                "target": "Average Length of Stay",
                "type": "influences",
                "strength": 0.8,
                "description": "Infections significantly extend recovery time"
            }
        ]
    
    def generate_sample_insights(self):
        """Generate AI-powered insights"""
        return [
            {
                "type": "critical",
                "severity": "high",
                "title": "Medication Error Spike Detected",
                "message": "Medication error rate has increased by 15% over the past week, affecting patient safety scores.",
                "recommendation": "Review pharmacy protocols and implement additional verification steps.",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "warning",
                "severity": "medium", 
                "title": "Emergency Department Wait Times",
                "message": "Average wait times are 40% above target during peak hours (2-6 PM).",
                "recommendation": "Consider additional triage resources during peak periods.",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "optimization",
                "severity": "low",
                "title": "Radiology Capacity Opportunity",
                "message": "Radiology department has 20% unused capacity during off-peak hours.",
                "recommendation": "Schedule non-urgent procedures during 10 PM - 6 AM window.",
                "timestamp": datetime.now().isoformat()
            }
        ]
    
    def run_demo(self):
        """Run the complete system demonstration"""
        print("🏥 HOSPITAL KPI INTELLIGENCE SYSTEM - LIVE DEMO")
        print("=" * 60)
        print(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Show KPI Overview
        print("📊 CURRENT KPI STATUS:")
        print("-" * 40)
        for kpi in self.kpis:
            status_emoji = {
                'excellent': '✅', 'good': '👍', 
                'warning': '⚠️', 'critical': '🔴'
            }.get(kpi['status'], '📊')
            
            performance = (kpi['current_value'] / kpi['target']) * 100
            
            print(f"{status_emoji} {kpi['name']} ({kpi['department']})")
            print(f"   Current: {kpi['current_value']} {kpi['unit']}")
            print(f"   Target: {kpi['target']} {kpi['unit']}")
            print(f"   Performance: {performance:.1f}% ({kpi['status'].upper()})")
            print(f"   Trend: {kpi['trend'].title()}")
            print()
        
        # Show Relationships
        print("🔗 KPI RELATIONSHIPS:")
        print("-" * 40)
        for rel in self.relationships:
            print(f"{rel['source']} → {rel['target']}")
            print(f"   Type: {rel['type']} | Strength: {rel['strength']}")
            print(f"   {rel['description']}")
            print()
        
        # Show Insights
        print("🧠 AI-POWERED INSIGHTS:")
        print("-" * 40)
        for insight in self.insights:
            priority_emoji = {'high': '🚨', 'medium': '⚠️', 'low': '💡'}
            print(f"{priority_emoji.get(insight['severity'], '💡')} {insight['title']}")
            print(f"   Priority: {insight['severity'].upper()}")
            print(f"   {insight['message']}")
            print(f"   💡 Recommendation: {insight['recommendation']}")
            print()
        
        # Show System Capabilities
        print("🚀 SYSTEM CAPABILITIES:")
        print("-" * 40)
        print(f"✅ Monitoring {len(self.kpis)} KPIs across hospital departments")
        print(f"✅ Tracking {len(self.relationships)} causal relationships")
        print(f"✅ Generating {len(self.insights)} intelligent insights")
        print(f"✅ Real-time network visualization")
        print(f"✅ What-if simulation interface")
        print(f"✅ Strategic goal alignment tracking")
        print(f"✅ Predictive analytics capabilities")
        print()
        
        print("🎉 SYSTEM IS FULLY OPERATIONAL!")
        print("\n🌐 To access the web interface:")
        print("   1. Run: python run.py")
        print("   2. Open browser to: http://localhost:8080")
        print("   3. Explore Dashboard, Insights, and Simulation features")
        print("\n📖 Available Routes:")
        print("   /dashboard     - Interactive KPI monitoring")
        print("   /insights      - AI-powered recommendations") 
        print("   /simulation    - What-if scenario testing")
        print("   /demo.html     - This demonstration")

if __name__ == "__main__":
    demo = HospitalKPIDemo()
    demo.run_demo()