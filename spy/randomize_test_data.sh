#!/bin/bash
filelist=$(ls /media/sanjay/HDD2/tflow/earnings_est/spy/data/ | shuf -n 99)
for file in $filelist
do
	mv /media/sanjay/HDD2/tflow/earnings_est/spy/data/$file /media/sanjay/HDD2/tflow/earnings_est/spy/data/test/$file 
	echo $file
done	
