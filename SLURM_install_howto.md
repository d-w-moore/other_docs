# Guide to installing SLURM on Ubuntu 14

Do the following as your personal, sudo-enabled Ubuntu user:

---

First install one of the following for crypto support, for `munge`:
Either do
```sudo apt-get install libgcrypt-dev```
or

```sudo apt-get install libssl-dev```

Get the tar-balls for munge ( a prerequisite ) and SLURM itself:
```
wget https://github.com/dun/munge/archive/munge-0.5.13.tar.gz
wget https://download.schedmd.com/slurm/slurm-17.11.4.tar.bz2
tar xf munge-0.5.13.tar.gz 
cd munge-munge-0.5.13/
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var 
make
sudo make install
sudo adduser --system --group --no-create-home munge
```

Create and adjust owner/permissions for a pseudo-random key file for `munge`:  
```
sudo dd if=/dev/urandom of=/etc/munge/munge.key bs=1k count=1
sudo chmod 600 /etc/munge/munge.key
sudo chown -R munge:munge /var/run/munge/ /var/log/munge/ /etc/munge/
sudo /etc/init.d/munge start
pgrep munged -afl
cd ..
```
If the output from the above `pgrep` command is blank, the munge daemon is not running. Requirements for `munged` to run correctly on the system should be fulfilled if all the above instructions were followed verbatim, but in case of mishap we can optionally edit `/etc/init.d/munge` and add the following line as the last in the DEBIAN `case` clause of `service_start()`:
```
[ $STATUS -ne 0 ] && echo "failure to start ($ERRMSG)" >&2`  
```
If the daemon fails to start , this should provide verbose output to the reason why. Note for the purposes of this document, that if `munged` is not running for whatever reason, that must be investigated and corrected before proceeding with the SLURM installation proper.

Also important: To make the `munged` run automatically at boot-time, do the following:
```
sudo update-rc.d munge defaults
```


---

## Building & installing SLURM itself

Explode and build SLURM -

```
tar jxf slurm-17.11.4.tar.bz2 
cd slurm-17.11.14/
./configure --with-munge=/usr
make
make check && sudo make install
```

Running SLURM configurator
---

Before `slurmd` can run as a daemon, it's necessary to set up some configuration.  First, collect some needed statistics with `slurmd -C`:
```
/usr/local/sbin/slurmd -C
NodeName=daniel-StPC440FX-PIIX-1996 CPUs=4 Boards=1 SocketsPerBoard=4 CoresPerSocket=1 ThreadsPerCore=1 RealMemory=2000
```
Without the proper values of `CPUs`, `CoresPerSocket`, and `ThreadsPerCore`,  **slurmd** will refuse to run, so keep those values handy for filling in the configuration.

Now bring up a browser to create the `slurm.conf` configuration file:

```
firefox ./doc/html/configurator.easy.html
```
Fill in , using hostname as all note names for a 1-node cluster example.  
Choose ie. `/var/spool/slurmd` and `/var/spool/slurmstate`, below we'll create these directories ourselves. 

Choose eg. ***LinuxProc*** option over ***cgroup***, which doesn't appear to work in Ubuntu 14. 

Make sure to specify the login name of the desired SLURM user instead of `slurm`. That user does not need to be `sudo`-enabled. Use your default login, or `irods` if you wish.  SLURM can also be (reconfigured)[#SLURM_reconfigure] later to allow switching to a different user , but currently only one is allowed at a time. 

Submit and copy text from web page into clipboard, then:
```
sudo su -c 'cat >/usr/local/etc/slurm.conf'
```
And paste into terminal from clipboard, using *Shift-Ctrl-V*

Create necessary directories for SLURM:
```
sudo mkdir /var/spool/slurm{d,state}
sudo chown $(id -un):$(id -gn) /var/spool/slurm{d,state}/
```
If irods or some other user was chosen specifically, alter the content of the chown command above to be (for example):
```
sudo chown irods:irods /var/spool/slurm{d,state}/
```

Starting up SLURM
---

Now we can start the `slurm` daemons:
```
sudo /usr/local/sbin/slurmctld 
sudo /usr/local/sbin/slurmd
```
To examine the PIDs of these daemons: 
```
more /var/run/slurmctld.pid /var/run/slurmd.pid
```

Use the `sbatch` command to submit a job and `squeue` to monitor SLURM's job queue.

**Note** `sbatch` without arguments or options will take a shell script (make sure shebang is first line!) and, after final *Ctrl-D* to mark end of standard-input, will  place that script on the queue.  Also note the the output of the job will be sent to a file in whichever was the current working directory when `sbatch` was run.

To make the daemons run persistently
---
Under Ubuntu Linux, these lines should be added to `/etc/rc.local`, to allow the `munged` and SLURM daemons to start automatically at boot-up. (If it has been decided to run these under user control, they can be launched via `sudo` or a `root` login). Make sure these are placed before the final `exit 0`:
```
# /etc/init.d/munge restart
/usr/local/sbin/slurmctld
/usr/local/sbin/slurmd
```

Uncomment the munge line only if you opted out of making the Ubuntu boot system start `munged` at boot time.

To change the SLURM user
---
The user empowered to submit SLURM jobs does not need to have sudo. The system-wide SLURM user can be easily changed for our current case of the 1-node cluster. 

To change the SLURM user to a different one (for this example, `irods`):

1. Stop the daemons:
```
sudo pkill slurm
```
2. Then edit the line starting with `SlurmUser=` to reflect the new user in the `/usr/local/etc/slurm.conf`:
```
SlurmUser=irods
```
3. Reset the state and ownership of the appropriate directories in `/var/spool`. 
```
sudo su -c "rm /var/spool/slurm*/* ; chown irods:irods /var/spool/slurm*/"
```
4. Restart the SLURM daemons:
```
sudo /etc/rc.local
```
