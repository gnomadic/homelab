import requests
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from pathlib import Path

# === Configuration ===
GLANCES_URL = "http://192.168.0.42:61208/api/4/all"
WIDTH, HEIGHT = 400, 300
PADDING = 10
BAR_WIDTH = 220
BAR_HEIGHT = 14
BAR_COLOR = 0  # black

# === Font Setup ===
FONT_PATH = "/usr/share/fonts/opentype/cantarell/Cantarell-Regular.otf"
BOLD_FONT_PATH = "/usr/share/fonts/opentype/cantarell/Cantarell-Bold.otf"

FONT = ImageFont.truetype(FONT_PATH, 16)
SMALL = ImageFont.truetype(FONT_PATH, 14)
TITLE = ImageFont.truetype(BOLD_FONT_PATH, 20)

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

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height

def draw_circle(draw, x, y, label, value, max_value=100, radius=35, suffix="%"):
    pct = min(max(value / max_value, 0.0), 1.0)
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.arc(bbox, start=0, end=359, fill=0)
    draw.pieslice(bbox, start=-90, end=359 , fill=1)
    draw.pieslice(bbox, start=-90, end=-90 + int(360 * pct), fill=2)

    offset = radius * 0.7
    smallerbbox = [x - offset, y - offset, x + offset, y + offset]
    draw.pieslice(smallerbbox, start=-90, end=-90, fill=1)


    val_text = f"{int(value)}{suffix}"
    w, h = text_size(draw, val_text, FONT)
    draw.text((x - w // 2, y - h // 2), val_text, font=SMALL, fill=0)

    w, h = text_size(draw, label, FONT)
    draw.text((x - w // 2, y + radius + 5), label, font=TITLE, fill=0)

def render_display(stats):
    inky = auto()
    img = Image.new("P", (WIDTH, HEIGHT), 1)
    draw = ImageDraw.Draw(img)

    # Title in top left
    title = "HOMEBASE"
    w, h = text_size(draw, title, FONT)
    draw.text((PADDING, PADDING), title, font=SMALL, fill=0)


    # Uptime in top right
    uptime = stats["uptime"]
    w, h = text_size(draw, uptime, FONT)
    draw.text((WIDTH - PADDING - w, PADDING), uptime, font=SMALL, fill=0)

    # Circle positions
    circle_y = 90
    draw_circle(draw, 90, circle_y, "CPU", stats["cpu_percent"])
    draw_circle(draw, 200, circle_y, "RAM", stats["mem_percent"])
    draw_circle(draw, 310, circle_y, "DISK", stats["disk_percent"])

    # Divider line
    draw.line((PADDING, 160, WIDTH - PADDING, 160), fill=0)

    # Top containers
    y = 170
    draw.text((PADDING, y), "TOP CONTAINERS (RAM MB)", font=SMALL, fill=0)
    y += 20

    for container in stats["top_containers"]:
        name = container["name"][:10].ljust(10)
        ram = container["ram_mb"]
        bar_len = int(min(ram / 4000, 1.0) * BAR_WIDTH)

        draw.text((PADDING, y), name, font=SMALL, fill=0)
        
        draw.rectangle([PADDING + 80, y, PADDING + 80 + BAR_WIDTH, y + BAR_HEIGHT ], fill=0)
        draw.rectangle([PADDING + 80 + 1, y + 1, PADDING + 80 + BAR_WIDTH - 1, y + BAR_HEIGHT - 1 ], fill=1)

        draw.rectangle([PADDING + 80 + 1, y + 1, PADDING + 80 + bar_len - 1, y + BAR_HEIGHT - 1], fill=2)
        draw.text((PADDING + 80 + BAR_WIDTH + 5, y), f"{ram} MB", font=SMALL, fill=0)
        y += 22

    inky.set_image(img)
    inky.show()

if __name__ == "__main__":
    stats = fetch_data()
    if "error" not in stats:
        render_display(stats)
    else:
        print("ERROR:", stats["error"])