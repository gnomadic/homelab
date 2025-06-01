import requests
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto

GLANCES_URL = "http://192.168.0.42:61208/api/4/all"

# === Configuration ===
WIDTH, HEIGHT = 400, 300
PADDING = 10
BAR_WIDTH = 220
BAR_HEIGHT = 14
BAR_COLOR = 0  # black
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT = ImageFont.truetype(FONT_PATH, 16)
SMALL = ImageFont.truetype(FONT_PATH, 14)

def fetch_data():
    try:
        res = requests.get(GLANCES_URL, timeout=5)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return {"error": str(e)}
    
    net = next((n for n in data.get("network", []) if n.get("interface_name") == "eth0"), {})

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
        "top_containers": top_containers
    }

def draw_bar(draw, x, y, label, value, max_value=100, suffix="%", width=BAR_WIDTH):
    draw.text((x, y), f"{label}: ", font=FONT, fill=0)
    bar_x = x + 70
    fill_width = int(min(value / max_value, 1.0) * width)
    draw.rectangle([bar_x, y + 4, bar_x + width, y + BAR_HEIGHT], outline=0, fill=None)
    draw.rectangle([bar_x, y + 4, bar_x + fill_width, y + BAR_HEIGHT], fill=BAR_COLOR)
    draw.text((bar_x + width + 5, y), f"{value:.1f}{suffix}", font=FONT, fill=0)

def render_display(stats):
    inky = auto()
    img = Image.new("P", (WIDTH, HEIGHT), 1)
    draw = ImageDraw.Draw(img)

    y = PADDING

    draw.text((PADDING, y), "SYSTEM STATUS", font=FONT, fill=0)
    y += 24

    draw_bar(draw, PADDING, y, "CPU", stats["cpu_percent"])
    y += 22
    draw_bar(draw, PADDING, y, "RAM", stats["mem_percent"])
    y += 22
    draw_bar(draw, PADDING, y, "DISK", stats["disk_percent"])
    y += 28

    draw.text((PADDING, y), f"Load: {stats['load_avg']:.2f}   Uptime: {stats['uptime']}", font=SMALL, fill=0)
    y += 20
    draw.text((PADDING, y), f"Docker: {stats['container_count']} containers", font=SMALL, fill=0)
    y += 18
    draw.text((PADDING, y), f"↑ {stats['net_up_mb']} MB   ↓ {stats['net_down_mb']} MB", font=SMALL, fill=0)
    y += 30

    draw.text((PADDING, y), "TOP CONTAINERS (RAM):", font=FONT, fill=0)
    y += 22
    for container in stats["top_containers"]:
        name = container["name"][:8].ljust(8)
        ram = container["ram_mb"]
        bar_length = int(min(ram / 4000, 1.0) * BAR_WIDTH)
        draw.text((PADDING, y), f"{name}", font=SMALL, fill=0)
        draw.rectangle([PADDING + 80, y + 4, PADDING + 80 + bar_length, y + BAR_HEIGHT], fill=0)
        draw.text((PADDING + 80 + BAR_WIDTH + 5, y), f"{ram}MB", font=SMALL, fill=0)
        y += 20

    inky.set_image(img)
    inky.show()

if __name__ == "__main__":
    stats = fetch_data()
    if "error" not in stats:
        render_display(stats)
    else:
        print("ERROR:", stats["error"])