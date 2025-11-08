from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os
import json
from datetime import datetime, timedelta
import threading
import time

# Import our modules
from api.routes import api_bp
from services.reasoning_engine import reasoner
from services.analytics import analytics
from services.data_generator import data_generator

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hospital-kpi-secret-key-2025'
app.config['STATIC_FOLDER'] = 'static'

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Register API blueprint
app.register_blueprint(api_bp)

# Global variables for real-time updates
update_thread = None
update_active = False

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/insights')
def insights():
    """Insights panel page"""
    return render_template('insights.html')

@app.route('/simulation')
def simulation():
    """What-if simulation page"""
    return render_template('simulation.html')

@app.route('/dashboard')
def dashboard():
    """Alternative dashboard route"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'data': 'Connected to Hospital KPI Intelligence System'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('request_update')
def handle_update_request():
    """Handle manual update request"""
    try:
        # Get fresh data
        kpis = reasoner.get_all_kpis()
        insights = reasoner.generate_insights()
        graph_data = reasoner.get_network_graph_data()
        
        # Emit updates
        emit('kpi_update', {
            'kpis': kpis,
            'timestamp': datetime.now().isoformat()
        })
        
        emit('insights_update', {
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        })
        
        emit('graph_update', {
            'graph_data': graph_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        emit('error', {'message': str(e)})

def background_update_task():
    """Background task to send periodic updates"""
    global update_active
    
    while update_active:
        try:
            # Get fresh data
            kpis = reasoner.get_all_kpis()
            insights = reasoner.generate_insights()
            graph_data = reasoner.get_network_graph_data()
            
            # Broadcast to all connected clients
            socketio.emit('kpi_update', {
                'kpis': kpis,
                'timestamp': datetime.now().isoformat()
            })
            
            socketio.emit('insights_update', {
                'insights': insights,
                'timestamp': datetime.now().isoformat()
            })
            
            socketio.emit('graph_update', {
                'graph_data': graph_data,
                'timestamp': datetime.now().isoformat()
            })
            
            # Wait 10 seconds before next update
            time.sleep(10)
            
        except Exception as e:
            print(f"Background update error: {e}")
            socketio.emit('error', {'message': str(e)})
            time.sleep(10)

@socketio.on('start_realtime')
def start_realtime_updates():
    """Start real-time updates"""
    global update_thread, update_active
    
    if not update_active:
        update_active = True
        update_thread = threading.Thread(target=background_update_task)
        update_thread.daemon = True
        update_thread.start()
        
        emit('realtime_started', {'message': 'Real-time updates started'})

@socketio.on('stop_realtime')
def stop_realtime_updates():
    """Stop real-time updates"""
    global update_active
    
    update_active = False
    emit('realtime_stopped', {'message': 'Real-time updates stopped'})

# Template context processors
@app.context_processor
def inject_global_data():
    """Add global data to all templates"""
    return {
        'app_name': 'Hospital KPI Intelligence System',
        'current_year': datetime.now().year,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found",
                         error_description="The requested page does not exist."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error",
                         error_description="An unexpected error occurred. Please try again later."), 500

# CLI commands
@app.cli.command()
def init_data():
    """Initialize sample data"""
    print("Initializing Hospital KPI data...")
    
    # Generate sample data
    current_data = data_generator.generate_current_kpi_data()
    relationships = data_generator.generate_relationships()
    strategic_goals = data_generator.generate_strategic_goals()
    
    # Save to files for reference
    with open('sample_data.json', 'w') as f:
        json.dump({
            'current_data': current_data,
            'relationships': relationships,
            'strategic_goals': strategic_goals
        }, f, indent=2)
    
    print("Sample data generated and saved to sample_data.json")

@app.cli.command()
def test_reasoning():
    """Test the reasoning engine"""
    print("Testing reasoning engine...")
    
    try:
        kpis = reasoner.get_all_kpis()
        insights = reasoner.generate_insights()
        
        print(f"Found {len(kpis)} KPIs")
        print(f"Generated {len(insights)} insights")
        
        for insight in insights[:3]:  # Show first 3 insights
            print(f"- {insight['title']}: {insight['message']}")
            
    except Exception as e:
        print(f"Error: {e}")

# Health check endpoint
@app.route('/health')
def health_check():
    """Application health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'realtime_active': update_active
    })
# Configuration
if __name__ == '__main__':
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    port = int(os.environ.get('PORT', 8080))

    print("🚀 Starting Hospital KPI Intelligence System...")
    print(f"🩺 Flask-SocketIO active on port {port}")
    print(f"📡 Connected reasoner triples: {len(reasoner.graph)}")

    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)

# # Configuration
# if __name__ == '__main__':
#     # Create necessary directories
#     os.makedirs('static/css', exist_ok=True)
#     os.makedirs('static/js', exist_ok=True)
#     os.makedirs('templates', exist_ok=True)
    
#     # Determine port from environment or use default
#     port = int(os.environ.get('PORT', 8080))
    
#     # Run the application
#     print(f"Starting Hospital KPI Intelligence WebApp on port {port}")
#     print(f"Access the application at: http://localhost:{port}")
    
#     socketio.run(app, 
#                 host='0.0.0.0', 
#                 port=port, 
#                 debug=False,
#                 allow_unsafe_werkzeug=True)
