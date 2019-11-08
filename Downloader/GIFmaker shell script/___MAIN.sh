#!/usr/bin/env bash
set -e

#2) YOUTUBE VIDEO TO BE DOWNLOADED
url=$1

echo ""
echo "Download Video Online?"
echo "INTEGER -- YES | ENTER -- NO"
read downloadvid 

echo ""
echo "Convert Subtitle to Text?"
echo "INTEGER -- YES | ENTER -- NO"
read subconvert 

echo ""
echo "Create Gentle JSON before clipping?"
echo "INTEGER -- YES | ENTER -- NO"
read createjson 

if [ "$createjson" -ge 1 ]
then    
  echo "Same text file for multiple videos?"
  echo "INTEGER -- YES | ENTER -- NO"
  read samefile
  if [ "$samefile" -ge 1 ]
  then    
    echo "What is it?"
    read filesamename
  else
    echo ""
  fi  
else
  echo ""
fi
  




if [ "$downloadvid" -ge 1 ]
then    
  youtube-dl -i -f mp4 --no-check-certificate --write-sub "$url"
else
  echo ""
fi

for f in *\ *; do mv "$f" "${f// /_}"; done || continue

mediafile=($(ls *.mp4))

for a in "${mediafile[@]}"
do
  name=$(basename $a .mp4)  
  if [ "$subconvert" -ge 1 ]
  then    
    ffmpeg -i "$name.en.vtt" "$name.srt"
    python ___extract_text.py "$name.srt" "$name.txt"
  else
    echo "text file already supplied"
  fi
  if [ "$createjson" -ge 1 ]
  then    
    echo Gentle is processing: $a
    echo $name
      if [ "$samefile" -ge 1 ]
      then    
        textname=$filesamename
      else
        textname=$name
      fi 
    curl -F "audio=@$name.mp4" -F "transcript=@$textname.txt" "http://localhost:8765/transcriptions?async=false" > "$name.json" 
  else
    echo "Gentle JSON already created"
  fi 
  bash ___clip.sh "$name.mp4" "$name.json" "$name"
done
