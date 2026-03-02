# Getting started

## Downloads

In your personal download folder on the [Intermodulation Products](https://intermod.pro) website,
you can find various useful items. You should have received your personal download link together
with the Metronomo unit. If not, or if you can't find it anymore, contact
[support](mailto:support@intermod.pro) and we'll help you promptly.



## Setup

### Grounding

In order to avoid ground loops, signal ground and power ground (protective earth, PE) are not
galvanically connected.
 
:::{note}
For transport safety, Metronomo units are delivered with signal and power ground shorted by a
shorting bar connecting the banana sockets on the back panel. Before normal operation, please
consider whether your application requires the two grounds to be connected or isolated.
:::

There are in total four different grounds. Here's a breakdown, with a list of connectors that have
their shields connected to each ground:

- `POWER GND`
  - *USB*: service port (USB 2.0 type B)
  - *LAN*: ethernet (RJ45)
  - *POWER GND*: chassis / power ground (banana socket)
  - aluminum chassis

- `SIGNAL GND`
  - *CLK OUT 1–7*: clock output (SMA)
  - *SYNC OUT 1–7*: sync output (SMA)
  - *SIGNAL GND*: signal ground (banana socket)

- `CLK_IN GND`
  - *CKL IN*: input reference clock (SMA)

- `SYNC_IN GND`
  - *SYNC IN*: input sync pulse / sysref (SMA)

For ESD protection and fault safety, each of `SIGNAL GND`, `CLK_IN GND` and `SYNC_IN GND` are
connected individually to `POWER GND` via a parallel of a 10-Ω resistor and a 45-V TVS diode.



### Network

Metronomo is designed to be fully controlled via network through the Ethernet port on the back
panel. There is no internal firewall running on Metronomo. For this reason, while there are no
known vulnerabilities, direct unprotected connection to the Internet is not recommended. If you do
intend to connect to Metronomo from the Internet, place it behind a NAT and/or a firewall.

Connection to Metronomo is done through the port number `7879` with the `TCP` protocol. For firmware
updates, SSH on port 22 is used. Refer to these values when in need of setting up firewall rules
and/or NAT forwarding.


#### Metronomo's default settings

At time of shipment, Metronomo is configured to automatically retrieve an IP address from a DHCP
server. In case that fails, it will fall back to a
[link-local address](https://en.wikipedia.org/wiki/Link-local_address).

Metronomo will advertise its hostname on the local network through multicast DNS
([mDNS](https://en.wikipedia.org/wiki/Multicast_DNS)). The hostname is based on the serial number:
if the serial number is e.g. `40042`, you can connect to the hostname `metronomo-40042.local`.

In practice, this means that you can connect Metronomo to your local router, and it will receive
an IP configuration automatically. You can then use the hostname to connect to it, or `ping` it to
discover the actual IP address:
```console
$ ping metronomo-40042.local
PING metronomo-40002.local (172.23.1.170) 56(84) bytes of data.
64 bytes from 172.23.1.170: icmp_seq=1 ttl=64 time=0.493 ms
64 bytes from 172.23.1.170: icmp_seq=2 ttl=64 time=0.268 ms
64 bytes from 172.23.1.170: icmp_seq=3 ttl=64 time=0.289 ms
64 bytes from 172.23.1.170: icmp_seq=4 ttl=64 time=0.279 ms
^C
--- metronomo-40002.local ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3031ms
rtt min/avg/max/mdev = 0.268/0.332/0.493/0.093 ms
```

If, instead, you connect Metronomo directly to your computer, it will fail to receive a valid IP
configuration from a DHCP server and it will fall back to link-local addressing. In practice, this
means that, after a minute or so, you can again reach Metronomo using its hostname:
```console
$ ping metronomo-40002.local
PING metronomo-40002.local (169.254.167.97) 56(84) bytes of data.
64 bytes from metronomo-40002.local (169.254.167.97): icmp_seq=1 ttl=64 time=0.253 ms
64 bytes from metronomo-40002.local (169.254.167.97): icmp_seq=2 ttl=64 time=0.154 ms
64 bytes from metronomo-40002.local (169.254.167.97): icmp_seq=3 ttl=64 time=0.126 ms
^C
--- metronomo-40002.local ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2065ms
rtt min/avg/max/mdev = 0.126/0.177/0.253/0.054 ms
```

For link-local addressing to work, you computer must support it. Consult the documentation for your
operating system if you find trouble.


(change-network)=
#### Changing Metronomo's network settings

Metronomo can be configured to use a static IP address, or to request a configuration from a DHCP
server. From factory, Metronomo units are configured to use DHCP. To change the network
configuration, use the `change_network` program available in your
[personal download folder](#downloads).

`change_network` can connect to Metronomo in two ways. One way is through a network connection,
which requires you to known the current IP address / hostname and to be able to connect to it. The
other way is through the USB serial port on the back panel, use the provided USB A-to-B cable, or
equivalent. Whichever connection method you use, follow the on-screen instructions and you should be
able to easily change the network settings.



## Python API

### Installing and updating

There is a Python [wheel package](https://packaging.python.org/en/latest/glossary/#term-Wheel) with
`.whl` extension available in your [personal download folder](#downloads). The package is just a
few kilobytes big, contains pure Python, and includes all the API required to interface with a
Metronomo unit.

You can easily install it using `pip`, e.g.:
```console
python -m pip install intermod_metronomo-1.1.0-py3-none-any.whl
```

For updating a previous installation, just add the `--upgrade` flag, e.g.:
```console
python -m pip install --upgrade intermod_metronomo-1.1.0-py3-none-any.whl
```

:::{tip}
If you get a _permission denied_ error while installing, you might try adding the `--user` flag to
the command to install the package in your user directory rather than the system directory.
:::

:::{important}
When installing/updating the package, make sure to use the same `python` executable and virtual
environment that you would using when running your experiments. If unsure, you can find out what
executable you are using in a Python shell by running the commands:
```python
import sys
print(sys.executable)
```
:::


### Getting help

The Python package `metronomo` is the entry point for controlling a Metronomo unit.
Refer to the [API Reference Guide](api/top) for the full documentation of the `metronomo` package.

If you get stuck, you're always welcome to [reach out](mailto:support@intermod.pro) and we'll
gladly help you get going with your experiments.

