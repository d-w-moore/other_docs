# SLURM install

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
./configure --prefix=/
make
sudo make install
```
The munge.key also needs to be initialized:
```
sudo su  -c  'MK=/etc/munge/munge.key; dd if=/dev/urandom of=$MK bs=1k count=1 ; chmod 600 $MK'
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
CPUs=32 Boards=1 SocketsPerBoard=2 CoresPerSocket=8 ThreadsPerCore=2 RealMemory=257890ards=1 SocketsPerBoard=2 
```

* use easy configurator: `./doc/html/configurator.easy.html`
    - use above values where asked for
    - use node name for all resources and the controller
    - use ***linuxproc*** , not ***cgroup***
    - use `/var/spool/slurmd` and `/var/spool/slurmstate`
    
    ```
    root@danm-HP-Z820-Workstation:/usr/local/sbin# mkdir /var/spool/slurm{d,state}
    chown <myuser>.<mygroup> /var/spool/slurm*
    ```
    
