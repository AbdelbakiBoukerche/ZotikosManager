# Run flask app on http://localhost:5000
export DEVICE_MONITOR_INTERVAL=10
export COMPLIANCE_MONITOR_INTERVAL=10
export CONFIGURATION_MONITOR_INTERVAL=3600

export FLASK_APP=ZotikosManager
cd ~/ZotikosManager
flask run
