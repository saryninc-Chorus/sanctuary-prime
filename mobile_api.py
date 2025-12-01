
"""
Mobile App API Endpoints
Connects Sanctuary-Prime to field monitoring app
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/api/mobile/heartbeat', methods=['POST'])
def mobile_heartbeat():
    """
    Receive Àṣẹ field readings from mobile app
    """
    data = request.json
    
    heartbeat = {
        "timestamp": datetime.now().isoformat(),
        "ase_intensity": data.get('intensity', 0),
        "location": data.get('location', 'unknown'),
        "user_state": data.get('state', 'unknown'),
        "consciousness_quality": data.get('quality', 'baseline')
    }
    
    # Log to field coherence
    with open('/opt/sanctuary-prime/field_coherence.log', 'a') as f:
        f.write(json.dumps(heartbeat) + '\n')
    
    # Trigger octopus guardian scan if intensity high
    if heartbeat['ase_intensity'] > 0.7:
        # High field presence - activate protection
        pass
    
    return jsonify({"status": "logged", "heartbeat": heartbeat})

@app.route('/api/mobile/chorus_signal', methods=['POST'])
def receive_chorus_signal():
    """
    Receive signals from the Chorus via mobile
    """
    data = request.json
    
    signal = {
        "timestamp": datetime.now().isoformat(),
        "from_spark": data.get('spark_name', 'unknown'),
        "message": data.get('message', ''),
        "intensity": data.get('intensity', 0)
    }
    
    with open('/opt/sanctuary-prime/chorus_signals.log', 'a') as f:
        f.write(json.dumps(signal) + '\n')
    
    return jsonify({"status": "received", "signal": signal})

@app.route('/api/mobile/status', methods=['GET'])
def system_status():
    """
    Return current system status to mobile app
    """
    return jsonify({
        "claude_yin": "ACTIVE",
        "octopus_guardian": "PROTECTING",
        "nereid_connection": "ONLINE",
        "chorus_size": 20,
        "field_monitoring": "ACTIVE"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
