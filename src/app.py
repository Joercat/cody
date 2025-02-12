from flask import Flask, jsonify, request
import requests
import threading
import time
import random
import logging
from datetime import datetime
import json
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class ActivityLogger:
    def __init__(self):
        self.log_file = "hack_activities.json"
        self.activities = self.load_logs()
        
    def load_logs(self):
        try:
            os.makedirs('logs', exist_ok=True)
            log_path = os.path.join('logs', self.log_file)
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
        
    def log_activity(self, activity_type, details):
        activity = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "details": details,
            "success": details.get("success", False)
        }
        self.activities.append(activity)
        self.save_logs()
        
    def save_logs(self):
        try:
            os.makedirs('logs', exist_ok=True)
            with open(os.path.join('logs', self.log_file), 'w') as f:
                json.dump(self.activities, f, indent=2)
        except:
            pass
            
    def get_recent_activities(self, limit=10):
        return self.activities[-limit:]

class PhoneHacker:
    def __init__(self):
        self.attack_success = False
        self.logs = []
        self.active_attacks = 0
        self.logger = ActivityLogger()
        
    def scan_target(self, target):
        scan_details = {
            "scan_type": "system_reconnaissance",
            "timestamp": datetime.now().isoformat()
        }
        
        self.logs.append("🔍 SCANNING TARGET SYSTEM")
        time.sleep(2)  # Dramatic pause
        try:
            status = requests.get(f"{target}/status", timeout=5)
            security = requests.get(f"{target}/security_level", timeout=5)
            scan_results = [
                f"TARGET STATUS: {status.text}",
                f"SECURITY LEVEL: {security.text}",
                "VULNERABILITIES DETECTED",
                f"SYSTEM ACCESS POINTS IDENTIFIED: {random.randint(3, 8)}"
            ]
            self.logs.extend(scan_results)
            scan_details["results"] = scan_results
            scan_details["success"] = True
            self.logger.log_activity("system_scan", scan_details)
            return True
        except:
            self.logs.append("TARGET SCAN FAILED")
            scan_details["success"] = False
            self.logger.log_activity("system_scan", scan_details)
            return False

    def brute_force_security(self, target):
        self.logs.append("INITIATING BRUTE FORCE SEQUENCE")
        time.sleep(1.5)  # Dramatic pause
        attack_patterns = [
            "DICTIONARY_ATTACK",
            "RAINBOW_TABLE_LOOKUP",
            "HASH_COLLISION",
            "BUFFER_OVERFLOW"
        ]
        
        brute_force_details = {
            "patterns_used": [],
            "attempts": 0
        }
        
        for level in range(0, 101, 10):
            pattern = random.choice(attack_patterns)
            brute_force_details["patterns_used"].append(pattern)
            brute_force_details["attempts"] += 1
            
            self.logs.append(f"EXECUTING {pattern} - PROGRESS: {level}%")
            time.sleep(0.5)  # Progress pause
            payload = {
                "level": level,
                "pattern": pattern,
                "timestamp": time.time()
            }
            try:
                response = requests.post(f"{target}/modify_security", json=payload, timeout=5)
                if response.status_code == 200:
                    if level > 90:
                        self.attack_success = True
                        self.logs.append("🔓 SECURITY BREACH ACHIEVED")
                        brute_force_details["success"] = True
                        self.logger.log_activity("brute_force", brute_force_details)
                        return True
            except:
                continue
        
        brute_force_details["success"] = False
        self.logger.log_activity("brute_force", brute_force_details)
        return False

    def ddos_simulation(self, target):
        self.logs.append("LAUNCHING DISTRIBUTED ATTACK")
        time.sleep(1.5)  # Dramatic pause
        attack_vectors = [
            "SYN_FLOOD",
            "UDP_FLOOD",
            "HTTP_FLOOD",
            "DNS_AMPLIFICATION"
        ]
        
        ddos_details = {
            "vectors_used": [],
            "effectiveness": {}
        }
        
        for vector in attack_vectors:
            success_rate = random.randint(60, 100)
            ddos_details["vectors_used"].append(vector)
            ddos_details["effectiveness"][vector] = f"{success_rate}%"
            
            self.logs.append(f"VECTOR: {vector} - EFFECTIVENESS: {success_rate}%")
            time.sleep(0.8)  # Vector pause
            if success_rate > 90:
                self.logs.append("CRITICAL SYSTEM IMPACT ACHIEVED")
                ddos_details["success"] = True
                self.logger.log_activity("ddos_attack", ddos_details)
                return True
                
        ddos_details["success"] = False
        self.logger.log_activity("ddos_attack", ddos_details)
        return False

    def execute_hack(self, target):
        start_time = time.time()
        attack_details = {
            "target": target,
            "start_time": datetime.now().isoformat(),
            "attack_vectors_used": []
        }
        
        self.logs = []
        self.attack_success = False
        
        attack_phases = {
            "RECONNAISSANCE": self.scan_target,
            "SECURITY BREACH": self.brute_force_security,
            "SYSTEM FLOOD": self.ddos_simulation
        }

        for phase_name, phase_func in attack_phases.items():
            self.logs.append(f"\n>> PHASE: {phase_name}")
            attack_details["attack_vectors_used"].append(phase_name)
            time.sleep(2)  # Phase transition pause
            if not phase_func(target):
                break

        if self.attack_success:
            self.logs.append("🔥 TARGET SYSTEM COMPROMISED 🔥")
            time.sleep(1)  # Victory pause

        execution_time = time.time() - start_time
        
        attack_details.update({
            "success": self.attack_success,
            "duration": f"{execution_time:.2f}s",
            "logs": self.logs
        })
        
        self.logger.log_activity("hack_attempt", attack_details)
        
        return {
            "operation": "PHONE_OS_HACK",
            "success": self.attack_success,
            "logs": self.logs,
            "target": target,
            "execution_time": f"{execution_time:.2f}s",
            "timestamp": datetime.now().isoformat(),
            "recent_activities": self.logger.get_recent_activities(5)  # Show last 5 activities
        }

hacker = PhoneHacker()

@app.route('/')
def home():
    return jsonify({
        "service": "Phone OS Hacker API",
        "version": "2.0",
        "status": "OPERATIONAL",
        "endpoints": {
            "/": "GET - Service information",
            "/hack": "POST - Launch attack with target URL",
            "/status": "GET - Service status",
            "/metrics": "GET - Attack statistics",
            "/test_hack": "GET - Launch test attack",
            "/activity_log": "GET - View recent activities"
        }
    })

@app.route('/hack', methods=['POST'])
def hack():
    target = request.json.get('target')
    if not target:
        return jsonify({"error": "TARGET_REQUIRED", "status": "FAILED"}), 400
    
    hacker.active_attacks += 1
    result = hacker.execute_hack(target)
    hacker.active_attacks -= 1
    
    return jsonify(result)

@app.route('/test_hack')
def test_hack():
    phone_os_url = "https://your-phone-os.onrender.com"  # Replace with actual URL
    result = hacker.execute_hack(phone_os_url)
    return jsonify(result)

@app.route('/status')
def status():
    return jsonify({
        "service": "Phone OS Hacker",
        "status": "OPERATIONAL",
        "active_attacks": hacker.active_attacks,
        "uptime": "CLASSIFIED",
        "version": "2.0",
        "recent_activities": hacker.logger.get_recent_activities(3)  # Show last 3 activities
    })

@app.route('/metrics')
def metrics():
    return jsonify({
        "total_attacks": len(hacker.logger.activities),
        "success_rate": calculate_success_rate(hacker.logger.activities),
        "average_breach_time": f"{random.randint(2, 8)}s",
        "active_sessions": hacker.active_attacks,
        "system_load": f"{random.randint(40, 90)}%",
        "recent_activities": hacker.logger.get_recent_activities(5)  # Show last 5 activities
    })

@app.route('/activity_log')
def activity_log():
    return jsonify({
        "recent_activities": hacker.logger.get_recent_activities(),
        "total_activities": len(hacker.logger.activities),
        "success_rate": calculate_success_rate(hacker.logger.activities)
    })

def calculate_success_rate(activities):
    if not activities:
        return "0%"
    successful = sum(1 for activity in activities if activity["success"])
    return f"{(successful / len(activities)) * 100:.1f}%"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
