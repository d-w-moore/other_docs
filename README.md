# other_docs

## -- installation

[SLURM install](./SLURM_install_howto.md)

- startSlurm
```
#!/bin/bash

TMUX=0
while getopts t opt
do
  case $opt in
    t) TMUX=1  ;;
  esac
done

DIR=$(dirname "$0")
"$DIR/stopSlurm" -q || exit $?

sudo /etc/init.d/munge restart
echo >&2 -n "waiting ... "
sleep 2
echo >&2

cmd1="/usr/local/sbin/slurmctld"
cmd2="/usr/local/sbin/slurmd"

STATUS=0
if [ $TMUX -eq 1 ]; then
 sudo tmux new-session \
 -d "$cmd1 -D" \; \
 split-window -d "$cmd2 -D" \; attach
else
 sudo $cmd1
 sudo $cmd2
 sleep 2
 {
 pgrep -c slurmctld  || ((++STATUS)) 
 pgrep -c slurmd     || ((++STATUS)) 
 } # >/dev/null 2>&1
fi
exit $STATUS
```
- stopSlurm
```
#!/bin/bash
#===
ACOUNT=0
QUIET=0
while getopts q opt
do
  case $opt in
    q) QUIET=1  ;;
  esac
done
shift $((OPTIND-1))
#===
[ $QUIET -gt 0 ] && exec 2>/dev/null
for ptn in 'slurm(ctl|)d' munged; do
  echo -n Sending signal for "'$ptn' ..." >&2
  PIDS=$(pgrep "$ptn")
  if [ -n "$PIDS" ]
  then
    sudo kill $PIDS && echo >&2 -n " success: $PIDS killed"
    : $((++ACOUNT))
  else
    echo -n " not active" >&2
  fi
  echo >&2
done

[ $ACOUNT -gt 0 ] && sleep 2

STATUS=0
for ptn in 'slurm(ctl|)d' munged
do
  pgrep "$ptn" && : $((++STATUS))
done

exit $STATUS

```
