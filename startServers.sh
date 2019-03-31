#!/bin/bash

# UDP Ports to listen on
PORTS_UDP=( {1260..1263} )

# TCP Ports to listen on
PORTS_UDP=( {1260..1263} )

# UDP port for counterpart to listen on
# (comment out to disable)
PORT_CP=1257

# Foreign counterpart's address and port
# (comment out to disable)
#FCP_ADDR=10.0.0.5
#FCP_PORT=1257

# --------------------------------------------------------------

if [ -f kill.sh ]; then
    ./kill.sh
fi

if [ -z "${FCP_ADDR}" ]; then
    FCP_ADDR="0.0.0.0"
fi
if [ -z "${FCP_PORT}" ]; then
    FCP_PORT=0
fi

pids=()

for port in "${PORTS_UDP[@]}"; do
    python3 server.py udp ${port} 0.0.0.0 0 ${FCP_ADDR} ${FCP_PORT} &> log/udp${port}.out &
    pids+=("$!")
done

for port in "${PORTS_TCP[@]}"; do
    python3 server.py tcp ${port} 0.0.0.0 0 ${FCP_ADDR} ${FCP_PORT} &> log/tcp${port}.out &
    pids+=("$!")
done

if [ "${PORT_CP}" ]; do
    python3 counterpart.py 1257 &> cp57.out &
    pids+=("$!")
done

temp=""
for pid in "${pids[@]}"; do
    temp+="kill ${pid}; "
done
temp+="rm kill.sh"
echo ${temp} > kill.sh
chmod +x kill.sh
