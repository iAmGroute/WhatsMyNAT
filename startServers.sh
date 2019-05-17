#!/bin/bash

# UDP Ports to listen on
PORTS_UDP=( 80 443 123 {1260..1261} )

# TCP Ports to listen on
PORTS_TCP=( 80 443 123 {1260..1261} )

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

pids=()

for port in "${PORTS_UDP[@]}"; do
    if [ "${FCP_ADDR}" ] && [ "${FCP_PORT}" ]; then
        python3 server.py udp ${port} 0.0.0.0 0 ${FCP_ADDR} ${FCP_PORT} &> log/udp${port}.out &
    else
        python3 server.py udp ${port} 0.0.0.0 0 &> log/udp${port}.out &
    fi
    pids+=("$!")
done

for port in "${PORTS_TCP[@]}"; do
    if [ "${FCP_ADDR}" ] && [ "${FCP_PORT}" ]; then
        python3 server.py tcp ${port} 0.0.0.0 0 ${FCP_ADDR} ${FCP_PORT} &> log/tcp${port}.out &
    else
        python3 server.py tcp ${port} 0.0.0.0 0 &> log/tcp${port}.out &
    fi
    pids+=("$!")
done

if [ "${PORT_CP}" ]; then
    python3 counterpart.py ${PORT_CP} &> log/cp${PORT_CP}.out &
    pids+=("$!")
fi

temp=""
for pid in "${pids[@]}"; do
    temp+="kill ${pid}; "
done
temp+="rm kill.sh"
echo ${temp} > kill.sh
chmod +x kill.sh
