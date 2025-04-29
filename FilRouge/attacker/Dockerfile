FROM kalilinux/kali-rolling

# Install usual tools + libraries + hydra
RUN apt-get update && apt-get install -y python3 python3-pip net-tools nmap metasploit-framework hydra
RUN pip3 install --break-system-packages --no-cache-dir numpy pandas scikit-learn gym tqdm joblib requests
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["/bin/bash"]
