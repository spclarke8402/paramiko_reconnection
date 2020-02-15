# paramiko_reconnection
Paramiko reboot host, keep re-trying connection to host to run bootstrap.

This python script uses Paramiko to ssh to a host or list of host(s) in a file and run reboot command followed by reconnection function in order to re-gain connection after reboot to run bootstrap command with yubikey prompt.

<b><i>Script times out after 5 mins if a connection can't be made.</i></b>

<b>:: Usage ::</b><br>
<code>
usage: reboot.py [-h] [-H HOST]

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Specify hostname
</code>


<b>:: Expect Output ::</b><br>
<code>
 ./reboot.py -H example.hostname.com
example.hostname.com
Touch YubiKey if flashing...
Touch YubiKey:
Rebooting Host...
testing connection...
[Errno 101] Network is unreachable
retrying connection...
[Errno 110] Connection timed out
retrying connection...
[Errno 110] Connection timed out
retrying connection...
[Errno 110] Connection timed out
retrying connection...
This will be bootstrap command
</code>

