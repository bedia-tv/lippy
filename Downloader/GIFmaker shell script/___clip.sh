vidfil=$1
jsonel=$2
filname=$3

mkdir GIFS

wordarray=( $(jq -r '.words[].word' "$jsonel") )
wordlength=( $(jq -r '.words | length' "$jsonel") )

for i in $(seq 1 $wordlength)
do
    alignedWord=$(jq -r ".words[${i}].alignedWord" "$jsonel")
    endtime=$(jq -r ".words[${i}].end" "$jsonel")
    starttime=$(jq -r ".words[${i}].start" "$jsonel")
    startint=$(printf %.1f $starttime)
    wholer="0$(echo "($endtime-$starttime)" | bc -l)"


pos=GIFS

if [ "$alignedWord" != null ] ;
then
    ffmpeg -y -ss "$starttime" -t "$wholer" -i "$vidfil" $pos/"$alignedWord||$filname||$startint.gif"    
fi


done