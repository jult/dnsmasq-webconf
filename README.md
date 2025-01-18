# dnsmasq WebConf

Simple DHCP Configuration Web UI for dnsmasq

![Screenshot](https://user-images.githubusercontent.com/4126355/70373854-96a87080-192f-11ea-8c5e-673323248b6d.png)

## Installation for debian 12 / ubuntu

* install required python modules (and git):

```
# apt install python3-bottle python3-jinja2 git
```

* clone repository

```
# git clone https://github.com/jult/dnsmasq-webconf.git
```

## Usage

* start server

```
# python3 ./dnsmasq-webconf/app/index.py [port_number] [--hosts path_to_hosts_file] [--leases path_to_leases_file --config] [path_to_dnsmasq_config]
```
Example command:
python3 ~/index.py 888 --hosts /etc/hosts --leases /opt/dnsmasq/dhcp.leases --config /etc/dnsmasq.conf

* access with your browser: http://hostname:port_number
