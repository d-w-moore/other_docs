# SLURM install

```
--- GET TARBALLS
wget https://github.com/dun/munge/archive/munge-0.5.13.tar.gz
wget https://download.schedmd.com/slurm/slurm-17.11.4.tar.bz2
--- BUILD AND INSTALL dun/munge
tar zxf munge-0.5.13.tar.gz  && cd munge-*0.5.13/
./configure
make
sudo make install
--- BUILD and INSTALL  slurm
tar jxf slurm-17.11.4.tar.bz2 && cd slurm*17.11.4/
./configure
make ; sudo make install
--- USE easy configurator to generate slurm.conf : doc/html/configurator.easy.html
    * first: /usr/local/sbin/slurmd -C 
CPUs=32 Boards=1 SocketsPerBoard=2 CoresPerSocket=8 ThreadsPerCore=2 RealMemory=257890ards=1 SocketsPerBoard=2 

root@danm-HP-Z820-Workstation:/usr/local/sbin# mkdir /var/spool/slurm_state
root@danm-HP-Z820-Workstation:/usr/local/sbin# mkdir /var/spool/slurm
root@danm-HP-Z820-Workstation:/usr/local/sbin# chown danm.danm /var/spool/slurm*
  linuxproc
```
