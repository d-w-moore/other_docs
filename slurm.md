# SLURM install

It's recommended you perform the procedure below as your sudo-enabled personal Ubuntu user, not as root!

##
Install a cryptography library ([OpenSSL](https://packages.ubuntu.com/trusty/libssl-dev) is recommended, but [libgcrypt](https://packages.ubuntu.com/trusty/libgcrypt11-dev) from GNU would also suffice).
```
sudo apt-get install libssl-dev
```
## GET TARBALLS

```
wget https://github.com/dun/munge/archive/munge-0.5.13.tar.gz
wget https://download.schedmd.com/slurm/slurm-17.11.4.tar.bz2
```

## BUILD AND INSTALL dun/munge

```
tar zxf munge-0.5.13.tar.gz  && cd munge-*0.5.13/
./configure --prefix=
make
sudo make install
```
The munge.key needs to be initialized with pseudo-random data, and then the daemon can be started:
```
MUNGEKEY=/etc/munge/munge.key
sudo su -c  "dd if=/dev/urandom of=$MUNGEKEY bs=1k count=1 ;chmod 600 $MUNGEKEY"
sudo su -c  "/etc/init.d/munged start"
```

## BUILD and INSTALL  slurm
```
tar jxf slurm-17.11.4.tar.bz2 && cd slurm*17.11.4/
./configure
make ; sudo make install
```

## Configure slurm
```
/usr/local/sbin/slurmd -C
```
Which will generate output of the form:
```
CPUs=32 Boards=1 SocketsPerBoard=2 CoresPerSocket=8 ThreadsPerCore=2 RealMemory=257890ards=1 SocketsPerBoard=2 
```
* use easy configurator: `./doc/html/configurator.easy.html`
    - use values output by `slurmd -C` where asked for; if these aren't correct, SLURM will not run!
    - use node name for all resources and the controller
    - use ***linuxproc*** , not ***cgroup***
    - make your Ubuntu user the SLURM user.
    - suggest using `/var/spool/slurmd` and `/var/spool/slurmstate` where prompted ; then we create these and make them writeable by the SLURM user:
    
    ```
    mkdir /var/spool/slurm{d,state}
    chown $(id -un):$(id -gn) /var/spool/slurm*
    ```
    
