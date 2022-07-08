#!/bin/sh
socks_ports=$(seq 9100 2 9108)

for port in $socks_ports; do
    # Writing torrc
    echo "SocksPort tor:${port}" > torrc.${port}
    echo "DataDirectory ${port}" >> torrc.${port}

    mkdir ${port} # TOR DataDirectory

    # At least one TOR in foreground
    if [ $port -eq 9108 ]; then
        tor -f torrc.${port}
    else
        tor -f torrc.${port} &
    fi
done
