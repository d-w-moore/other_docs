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
sudo adduser --system --group munge
man adduser
sudo vi /etc/init.d/munge
```

At this point, we can insert as a helpfully verbose test of STATUS at end of start-stop-daemon clause:  

  `[ $STATUS -ne 0 ] && echo "failure to start or stop ($ERRMSG)" >&2`  

Create a pseudo-random random key for `munge`:  
```
sudo dd if=/dev/urandom of=/etc/munge/munge.key bs=1k count=1
sudo chmod 600 /etc/munge/munge.key
sudo chown -R munge:munge /var/run/munge/ /var/log/munge/ /etc/munge/
sudo /etc/init.d/munge start
pgrep munge -afl
cd ..
```

---


Explode and build SLURM -

```
tar jxf slurm-17.11.4.tar.bz2 
cd slurm-17.11.14/
./configure --with-munge=/usr
make ; sudo make install
```

Bring up browser to create configuration file

```
firefox ./doc/html/configurator.easy.html
```
Fill in , using hostname as all note names for a 1-node cluster example.  
Choose ie. `/var/spool/slurmd` and `/var/spool/slurmstate`, below we'll create these directories ourselves.  
Choose eg. ***LinuxProc*** option over ***cgroup***, which doesn't appear to work in Ubuntu 14.  
Make sure to use your sudo-enabled Ubuntu user instead of `slurm` for the SLURM user.

Submit and copy text from web page into clipboard, then:
```
sudo su -c 'cat >/usr/local/etc/slurm.conf'
```
And paste into terminal from clipboard, using *Shift-Ctrl-V* .

Create necessary directories for SLURM:
```
mkdir /var/spool/slurm{d,state}
sudo mkdir /var/spool/slurm{d,state}
sudo chown $(id -un):$(id -gn) /var/spool/slurm{d,state}/
```

Make sure `munged` daemon is running:
```
sudo /etc/init.d/munge restart
pgrep munged -afl
```

And start the `slurm` daemons:
```
sudo /usr/local/sbin/slurmctld 
sudo /usr/local/sbin/slurmd
```
To examine the PIDs of these daemons: 
```
more /var/run/slurmctld.pid /var/run/slurmd.pid
```

Use the `sbatch` command to submit a job and `squeue` to monitor SLURM's job queue.

**Note** `sbatch` without arguments or options will take a shell script (make sure shebang is first line!) and, after final *Ctrl-D* to mark end of standard-input, will  place that script on the queue.
