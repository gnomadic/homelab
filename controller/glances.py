import requests
import pprint
import json


GLANCES_URL = "http://192.168.0.42:61208/api/4/all"

def fetch_glances_stats():
    try:
        response = requests.get(GLANCES_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": str(e)}

    # Minimal, readable status summary
    return data
    # return {
    #     "hostname": data.get("system", {}).get("hostname"),
    #     "uptime_sec": data.get("uptime", {}).get("seconds"),
    #     "cpu_percent": data.get("cpu", {}).get("total"),
    #     "mem_used": round(data.get("mem", {}).get("used", 0) / (1024**3), 2),
    #     "mem_total": round(data.get("mem", {}).get("total", 0) / (1024**3), 2),
    #     "disk_percent": data.get("fs", [{}])[0].get("percent", 0),
    #     "disk_mount": data.get("fs", [{}])[0].get("mnt", "/"),
    #     "load": data.get("load", {}).get("min1"),
    #     "network_rx": round(data.get("net", [{}])[0].get("rx", 0) / (1024**2), 2),
    #     "network_tx": round(data.get("net", [{}])[0].get("tx", 0) / (1024**2), 2),
    #     "docker_containers": len(data.get("docker", [])),
    # }

if __name__ == "__main__":
    data = fetch_glances_stats()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # from pprint import pprint
    # pprint(fetch_glances_stats())
