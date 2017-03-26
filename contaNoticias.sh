#!/bin/bash

if [[ $1 = "" ]]; then
	echo "USO: $0 <nome da pasta>"
	exit -1
fi

base=$(realpath $1)
saida="$base/estatisticas.txt"

echo -n "" > $saida

total=0
for pasta in $(find $base -maxdepth 1 -type d | tail -n +2); do
	total_pasta=$(find $pasta -name '*.txt' | wc -l)
	total=$(($total + $total_pasta))
	echo -e "${pasta#$base/}: $total_pasta" >> $saida
	for subpasta in $(find $pasta -type d -links 2 | tail -n +2); do
		total_subpasta=$(find $subpasta -name '*.txt' | wc -l)
		echo "- ${subpasta#$pasta/}: $total_subpasta" >> $saida
	done
	echo "" >> $saida
done
echo "Total: $total" >> $saida
