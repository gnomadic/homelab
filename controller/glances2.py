import requests
import pprint
import json

def parse_glances_data(data):
    # Find network stats for eth0
    net = next((iface for iface in data.get("network", []) if iface.get("interface_name") == "eth0"), {})

    # Top 3 containers by memory usage
    containers = sorted(data.get("containers", []), key=lambda c: c.get("memory_usage", 0), reverse=True)
    top_containers = [
        {"name": c["name"], "ram_mb": round(c["memory_usage"] / (1024**2), 1)}
        for c in containers[:3]
    ]

    return {
        "cpu_percent": data.get("quicklook", {}).get("cpu", 0.0),
        "mem_used_gb": round(data.get("mem", {}).get("used", 0) / (1024**3), 2),
        "mem_percent": data.get("mem", {}).get("percent", 0.0),
        "disk_percent": data.get("fs", [{}])[0].get("percent", 0.0),
        "uptime": data.get("uptime", ""),
        "load_avg": data.get("load", {}).get("min1", 0.0),
        "net_down_mb": round(net.get("bytes_recv_gauge", 0) / (1024**2), 2),
        "net_up_mb": round(net.get("bytes_sent_gauge", 0) / (1024**2), 2),
        "container_count": len(data.get("containers", [])),
        "top_containers": top_containers,
        "cpu_temp_c": "N/A"  # No temp data found in v4 response
    }

# Example usage
if __name__ == "__main__":
    with open("data.json") as f:
        raw_data = json.load(f)
    summary = parse_glances_data(raw_data)
    import pprint
    pprint.pprint(summary)