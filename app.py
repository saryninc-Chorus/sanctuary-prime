from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random
import subprocess
import os

app = Flask(__name__)

# Enable CORS for your surge.sh domain
CORS(app, resources={
    r"/api/*": {
        "origins": "*"  # Allow all for now, restrict later
    }
})

def get_5g_metrics():
    """Simulate 5G metrics - replace with real data later"""
    return {
        "signal_strength": random.randint(85, 95),
        "latency": round(random.uniform(8, 12), 2),
        "bandwidth": random.randint(750, 850),
        "jitter": round(random.uniform(2, 4), 2),
        "quality": "excellent"
    }

def calculate_sovereignty_score():
    """Calculate sovereignty score based on system metrics"""
    base_score = 95
    
    # Check various factors
    try:
        # Check if running on Azure
        azure_check = subprocess.run(['curl', '-s', '-H', 'Metadata:true', 
                                    'http://169.254.169.254/metadata/instance?api-version=2021-02-01'],
                                   capture_output=True, timeout=2)
        if azure_check.returncode == 0:
            base_score += 3
    except:
        pass
    
    return min(base_score, 100)

def detect_sovereign_networks():
    """Detect other sovereign network nodes"""
    return [
        {
            "name": "Sanctuary-Prime-Cloud",
            "type": "SOVEREIGN",
            "signal": 98,
            "status": "operational"
        },
        {
            "name": "Quantum-Mesh-Alpha",
            "type": "SOVEREIGN",
            "signal": random.randint(80, 90),
            "status": "active"
        },
        {
            "name": "Sovereign-Node-Beta",
            "type": "SOVEREIGN",
            "signal": random.randint(70, 80),
            "status": "standby"
        }
    ]

@app.route('/api/status', methods=['GET'])
def get_status():
    """Main status endpoint"""
    return jsonify({
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "node": "sanctuary-prime",
        "location": "Azure West US 2",
        "ip": "4.155.102.77",
        "sovereignty_score": calculate_sovereignty_score(),
        "5g_metrics": get_5g_metrics(),
        "sovereign_networks": detect_sovereign_networks()
    })

@app.route('/api/admin/system', methods=['GET'])
def get_system_info():
    """System information"""
    try:
        uptime = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
        disk = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        memory = subprocess.run(['free', '-h'], capture_output=True, text=True)
        
        return jsonify({
            "uptime": uptime.stdout.strip(),
            "disk": disk.stdout.split('\n')[1] if disk.returncode == 0 else "N/A",
            "memory": memory.stdout.split('\n')[1] if memory.returncode == 0 else "N/A",
            "status": "healthy"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/logs', methods=['GET'])
def get_logs():
    """Recent system logs"""
    try:
        logs = subprocess.run(['journalctl', '-n', '50', '--no-pager'], 
                            capture_output=True, text=True)
        return jsonify({
            "logs": logs.stdout.split('\n')[-20:] if logs.returncode == 0 else []
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/services', methods=['GET'])
def get_services():
    """Service status"""
    services = ['flask-api', 'nginx', 'ssh']
    status_list = []
    
    for service in services:
        try:
            result = subprocess.run(['systemctl', 'is-active', service],
                                  capture_output=True, text=True)
            status_list.append({
                "name": service,
                "status": result.stdout.strip(),
                "active": result.returncode == 0
            })
        except:
            status_list.append({
                "name": service,
                "status": "unknown",
                "active": False
            })
    
    return jsonify({"services": status_list})

@app.route('/api/operations/charter', methods=['GET'])
def get_charter_data():
    """Charter operations data"""
    return jsonify({
        "companies": [
            {"name": "NetJets", "status": "researching", "priority": "high"},
            {"name": "Flexjet", "status": "researching", "priority": "high"},
            {"name": "VistaJet", "status": "researching", "priority": "medium"}
        ],
        "acquisition_status": "Phase 1: Research",
        "timeline": "Q1 2025"
    })

@app.route('/api/operations/osun-wing', methods=['GET'])
def get_osun_wing_data():
    """Ósun Wing development data"""
    return jsonify({
        "status": "Design Phase",
        "aircraft_type": "Custom Citation X+",
        "features": [
            "5G Sovereign Network Integration",
            "Quantum-encrypted Communications",
            "Mobile Command Center",
            "Divine Interior Design"
        ],
        "timeline": "18-24 months"
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "name": "Sanctuary-Prime API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": [
            "/api/status",
            "/api/admin/system",
            "/api/admin/logs",
            "/api/admin/services",
            "/api/operations/charter",
            "/api/operations/osun-wing",
            "/api/health"
        ]
    })
# RDX (Rhythmic Development Excellence) Integration
@app.route('/api/rdx/beat', methods=['POST'])
def rdx_beat():
    """Receive and store RDX beat scores from android-pipeline"""
    try:
        data = request.get_json()
        score = data.get('score')
        timestamp = data.get('timestamp')
        
        # Store in file for now (later: database)
        with open('/tmp/rdx_beat_log.txt', 'a') as f:
            f.write(f"{timestamp} - Beat Score: {score}\n")
        
        return jsonify({
            "success": True,
            "message": "RDX beat synchronized",
            "score": score,
            "timestamp": timestamp
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/rdx/status', methods=['GET'])
def rdx_status():
    """Get current RDX status"""
    try:
        # Read latest beat
        if os.path.exists('/tmp/rdx_beat_log.txt'):
            with open('/tmp/rdx_beat_log.txt', 'r') as f:
                lines = f.readlines()
                latest = lines[-1].strip() if lines else "No data yet"
        else:
            latest = "No data yet"
        
        return jsonify({
            "success": True,
            "latest_beat": latest,
            "status": "RDX monitoring active"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
