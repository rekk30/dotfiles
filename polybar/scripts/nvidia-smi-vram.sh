total=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | awk '{ print ""$1""}')
used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | awk '{ print ""$1""}')
percent=$(printf "%.0f" $(echo "scale=2 ; $used / $total * 100" | bc))
echo $percent

