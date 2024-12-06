import requests
import logging
from typing import Dict
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_wait_times() -> Dict:
    url = "https://api.garitacenter.com/gc_report.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        tijuana_data = next((entry for entry in data if entry['city'] == 'tijuana'), None)
        
        if not tijuana_data or 'report' not in tijuana_data:
            logger.error("No Tijuana data found in response")
            return {}
            
        report = tijuana_data['report']
        
        wait_times = {
            # San Ysidro
            "San Ysidro All Traffic": report['sanYsidro']['vehicle']['standard']['time'],
            "San Ysidro Ready Lane": report['sanYsidro']['vehicle']['readyLane']['time'],
            "San Ysidro Sentri": report['sanYsidro']['vehicle']['sentri']['time'],
            "San Ysidro Pedestrian": report['sanYsidro']['pedestrian']['standard']['time'],
            "San Ysidro Pedestrian Ready": report['sanYsidro']['pedestrian']['readyLane']['time'],
            
            # Otay
            "Otay All Traffic": report['otay']['vehicle']['standard']['time'],
            "Otay Ready Lane": report['otay']['vehicle']['readyLane']['time'],
            "Otay Sentri": report['otay']['vehicle']['sentri']['time'],
            "Otay Pedestrian": report['otay']['pedestrian']['standard']['time'],
            "Otay Pedestrian Ready": report['otay']['pedestrian']['readyLane']['time']
        }

        logger.info(f"Successfully fetched wait times: {wait_times}")
        return wait_times

    except Exception as e:
        logger.error(f"Error fetching wait times: {e}")
        return {}

def main():
    wait_times = get_wait_times()
    if wait_times:
        print("\nCurrent Wait Times:")
        
        print("\nSan Ysidro:")
        print("Vehicles:")
        for lane in ["San Ysidro All Traffic", "San Ysidro Ready Lane", "San Ysidro Sentri"]:
            print(f"  {lane}: {wait_times[lane]} minutes")
        print("Pedestrians:")
        for lane in ["San Ysidro Pedestrian", "San Ysidro Pedestrian Ready"]:
            print(f"  {lane}: {wait_times[lane]} minutes")
            
        print("\nOtay:")
        print("Vehicles:")
        for lane in ["Otay All Traffic", "Otay Ready Lane", "Otay Sentri"]:
            print(f"  {lane}: {wait_times[lane]} minutes")
        print("Pedestrians:")
        for lane in ["Otay Pedestrian"]:
            print(f"  {lane}: {wait_times[lane]} minutes")
    else:
        print("Could not fetch wait times")

if __name__ == "__main__":
    main()