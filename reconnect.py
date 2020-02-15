#!/home/y/bin/python3

import paramiko
import argparse
import time
import errno
import os

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-H", "--host",
                    help="Specify hostname",
                    type=str)

ARGS = PARSER.parse_args()



def main():

    hosts_arg = ARGS.host

    user = os.getlogin()

    if hosts_arg is not None:
        hosts = hosts_arg.split(',')

    else:
        with open('hosts.txt') as hosts:
            hosts = hosts.read().splitlines()

    reboot(hosts, user)
    retry(hosts, user)


def reboot(hosts, user):

    try:
        for host in hosts:
            output = ""
            print(host)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=user)
            s = ssh.get_transport().open_session()
            paramiko.agent.AgentRequestHandler(s)

            print("Touch YubiKey if flashing...")

            sh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/reboot -h now", get_pty=True)
            stdout = ssh_stdout.readlines()

            for line in stdout:
                output = output+line

            if output != "":
                print(output.rstrip('\n'))
                print("Rebooting Host...")

            else:
                print("Problem rebooting host.")

            ssh.close()

    except OSError as e:
        if e.errno == errno.ENETUNREACH or errno.ECONNREFUSED or errno.ETIMEDOUT:
            print(e)
            pass


def retry(hosts, user):

    for host in hosts:

        output = ""

        retry_interval = 1
        timeout = 300

        retry_interval = float(retry_interval)
        timeout = int(timeout)

        timeout_start = time.time()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        retry_count = 0
        while time.time() < timeout_start + timeout:
            time.sleep(retry_interval)
            retry_count += 1
            try:
                if retry_count == 1:
                    print("testing connection...")
                else:
                    print("retrying connection...")

                ssh.connect(hostname=host, username=user)

                if ssh.get_transport() is not None:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("echo This will be bootstrap command")
                    stdout = ssh_stdout.readlines()

                    for line in stdout:
                        output = output + line
                    if output != "":
                        print(output.rstrip('\n'))
                    else:
                        print("No output")

                    ssh.close()
                    break

            except OSError as e:
                if e.errno == errno.ENETUNREACH or errno.ECONNREFUSED or errno.ETIMEDOUT:
                    print(e)
                    continue


if __name__ == '__main__':
    main()
