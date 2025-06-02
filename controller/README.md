# HomeLab Controller

## Requirements
1.  Raspberry pi zero w 2 with OS setup
2.  Inky wHAT - Large e-Ink Display configured and working
3.  (Glances)[https://github.com/nicolargo/glances] running on your home server with web access enabled


## Setup


update every ten minutes cron:

`*/10 * * * *  ~/.virtualenvs/pimoroni/bin/python3 ~/homelab/controller/status.py`
