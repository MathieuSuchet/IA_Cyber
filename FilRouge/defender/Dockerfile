FROM debian:12-slim

RUN apt-get update && apt-get install -y \
    suricata iptables python3 python3-pip python3-venv git && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir \
    scikit-learn pandas joblib tailer \
    numpy matplotlib tqdm streamlit && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /opt/workspace

ENTRYPOINT sh -c "\
    iptables -I FORWARD -j NFQUEUE --queue-num 0 && \
    suricata -i eth0 --af-packet -q 0 -l /var/log/suricata & \
    echo 'Attente de /var/log/suricata/eve.json...' && \
    while [ ! -f /var/log/suricata/eve.json ]; do sleep 1; done && \
    tail -f /var/log/suricata/eve.json"

