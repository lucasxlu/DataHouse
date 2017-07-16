mkdir converted
filelist=`ls 1`
for file in $filelist
do 
    sox '1/'$file 'converted/'$file'.wav' channels 1 rate 16k fade 3 norm
done