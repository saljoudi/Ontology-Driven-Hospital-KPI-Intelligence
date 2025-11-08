# 🏥 Hospital KPI Intelligence WebApp

An ontology-driven hospital performance intelligence system that uses semantic reasoning to connect and analyze departmental KPIs, demonstrating how each department's performance influences overall hospital goals.

## 🚀 Features

### Core Functionality
- **Ontology-Based KPI Modeling**: Complete OWL/RDF ontology with hospital departments, KPIs, and relationships
- **Semantic Reasoning**: Automated inference of KPI status, goal risks, and operational stress patterns
- **Interactive Network Visualization**: Dynamic D3.js network showing KPI dependencies and causal relationships
- **What-If Simulation**: Real-time scenario testing with slider controls and impact propagation
- **Real-Time Insights**: AI-powered recommendations and predictive analytics
- **Strategic Goal Alignment**: Hierarchical mapping from strategic goals to operational KPIs

### Technical Highlights
- **Flask + SocketIO**: Real-time web application with live updates
- **RDFLib**: Semantic web technology for ontology processing and reasoning
- **ECharts + D3.js**: Interactive data visualizations and network graphs
- **Responsive Design**: Modern UI with Tailwind CSS and smooth animations
- **RESTful API**: Comprehensive API endpoints for all functionality

## 🏗️ Architecture

### System Components

1. **Ontology Layer** (`ontology/`)
   - `hospital_kpi.owl`: OWL ontology with classes, properties, and SWRL rules
   - `kpi_data.ttl`: Sample RDF data with realistic hospital KPIs

2. **Business Logic** (`services/`)
   - `reasoning_engine.py`: Semantic reasoning with RDFLib
   - `analytics.py`: KPI correlation analysis and predictive modeling
   - `data_generator.py`: Synthetic data generation for testing

3. **API Layer** (`api/`)
   - `routes.py`: REST API endpoints for all functionality

4. **Web Application** (`app.py`)
   - Flask application with SocketIO for real-time updates
   - Template rendering and static file serving

5. **Frontend** (`static/` + `templates/`)
   - Interactive dashboards with network visualization
   - What-if simulation interface
   - Real-time insights and recommendations

## 📊 KPI Categories

### Departments
- Emergency Department
- Radiology Department
- Surgery Department
- Pharmacy Department

### Performance Domains
- Operational Efficiency
- Patient Safety
- Quality of Care
- Financial Performance

### Strategic Goals
- Enhance Patient Experience
- Achieve Operational Excellence
- Ensure Clinical Quality
- Optimize Financial Performance

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run.py
   ```

3. **Access the Application**
   - Dashboard: http://localhost:8080
   - Insights: http://localhost:8080/insights
   - Simulation: http://localhost:8080/simulation

### Production Deployment

#### Option 1: Docker
```bash
docker build -t hospital-kpi-intelligence .
docker run -p 8080:8080 hospital-kpi-intelligence
```

#### Option 2: Render
- Connect GitHub repository to Render
- Use `render.yaml` configuration
- Deploy automatically

#### Option 3: Heroku
```bash
heroku create your-app-name
heroku config:set PORT=8080
git push heroku main
```

## 📖 Usage Guide

### Dashboard
- **KPI Cards**: View real-time performance with color-coded status
- **Network Graph**: Explore relationships between KPIs
- **Insights Panel**: Get AI-powered recommendations
- **Strategic Goals**: Track progress toward organizational objectives

### Insights
- **Filter Controls**: Focus on specific insight types
- **Trend Analysis**: Historical performance patterns
- **Causal Analysis**: Understand relationship chains
- **Predictive Analytics**: Future performance forecasting

### What-If Simulation
- **Adjust KPIs**: Use sliders to change values
- **Run Scenarios**: See immediate impact on related KPIs
- **Compare Results**: Before/after visualization
- **Save Scenarios**: Store and reload simulation setups

## 🔧 API Endpoints

### Core Endpoints
- `GET /api/kpis` - Get all KPIs with current values
- `POST /api/reasoning` - Run semantic reasoning
- `GET /api/graph` - Get network graph data
- `POST /api/simulate` - Run what-if simulation

### Additional Endpoints
- `GET /api/insights` - Get real-time insights
- `GET /api/departments` - Get department data
- `GET /api/historical` - Get historical trends
- `GET /api/strategic-goals` - Get strategic goals

## 🧪 Testing

### Unit Tests
```bash
# Test ontology loading
python -c "from services.reasoning_engine import reasoner; print('✅ Reasoning engine loaded')"

# Test analytics
python -c "from services.analytics import analytics; print('✅ Analytics engine loaded')"

# Test data generator
python -c "from services.data_generator import data_generator; print('✅ Data generator loaded')"
```

### Integration Tests
```bash
# Test Flask app
python -c "from app import app; print('✅ Flask app loaded')"

# Test full functionality
python run.py
```

## 🎯 Key Benefits

### Semantic Intelligence
- **Context-Aware**: KPIs are understood in their operational context
- **Relationship Mapping**: Automatic discovery of causal relationships
- **Predictive Power**: Forward-looking insights based on patterns

### Decision Support
- **What-If Analysis**: Test changes before implementation
- **Risk Assessment**: Identify potential cascade effects
- **Optimization**: Find improvement opportunities

### Operational Excellence
- **Real-Time Monitoring**: Live updates and alerts
- **Strategic Alignment**: Connect daily operations to goals
- **Continuous Learning**: System improves with more data

## 🔬 Technical Details

### Ontology Structure
```turtle
# Classes
hospital:Hospital
hospital:Department  
hospital:KPI
hospital:PerformanceDomain
hospital:StrategicGoal
hospital:PerformanceObservation
hospital:CausalLink

# Properties
hospital:hasKPI
hospital:belongsToDomain
hospital:contributesToGoal
hospital:influences
hospital:dependsOn
hospital:hasValue
hospital:targetValue
```

### Reasoning Rules
- **Status Inference**: Automatic KPI status based on target comparison
- **Goal Risk Assessment**: Strategic goal impact from KPI performance
- **Operational Stress**: Multi-KPI pattern recognition

### Visualization Features
- **Network Graph**: Force-directed layout with relationship strength
- **Interactive Controls**: Zoom, pan, node selection
- **Real-Time Updates**: Smooth animations for data changes
- **Responsive Design**: Mobile-friendly interface

## 📈 Performance

### Scalability
- **Efficient Reasoning**: Optimized RDFLib queries
- **Caching**: Smart caching of computed results
- **Async Processing**: Non-blocking real-time updates

### Data Quality
- **Validation**: Input validation and error handling
- **Consistency**: Ontology ensures data consistency
- **Traceability**: Full audit trail of changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **RDFLib Team**: For the excellent semantic web library
- **Flask Community**: For the lightweight web framework
- **D3.js/ECharts**: For powerful visualization capabilities
- **Tailwind CSS**: For the utility-first CSS framework

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the API endpoints for integration guidance

---

**🏥 Transforming Healthcare Through Semantic Analytics**