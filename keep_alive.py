import requests
import time
from datetime import datetime

# Configuration
URL = "https://mirai-alzheimer-screening.onrender.com/api/health"
INTERVAL = 300  # 5 minutes (300 seconds)

def ping_server():
    print(f"Starting keep-alive monitoring for: {URL}")
    print(f"Ping interval: {INTERVAL} seconds")
    print("-" * 50)

    while True:
        try:
            start_time = time.time()
            response = requests.get(URL, timeout=30)
            duration = round(time.time() - start_time, 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[{timestamp}] ✅ Success ({duration}s) | Status: {response.status_code} | Version: {data.get('version')}")
            else:
                print(f"[{timestamp}] ⚠️ Warning ({duration}s) | Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] ❌ Error: {e}")
        except Exception as e:
            print(f"[{timestamp}] ❌ Unexpected Error: {e}")
        
        # Wait for next interval
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        ping_server()
    except KeyboardInterrupt:
        print("\nKeep-alive script stopped by user.")
