#!/bin/bash

NAME=${1?Error: no video file name given}

filename=$(basename -- "$NAME")
extension="${filename##*.}"
filename="${filename%.*}"

echo "GENERATING COLOUR PALETTE FROM: $NAME"

ffmpeg -ss 0 -t 10 -i $NAME -vf fps=24,scale=728:-1:flags=lanczos,palettegen palette.png &&

echo "MAKING GIFs: $NAME" &&

# ffmpeg -ss 0 -t 10 -i $NAME -i palette.png -filter_complex "fps=24,scale=728:-1:flags=lanczos[x];[x][1:v]paletteuse" -loop 1 ${filename}_LOOP1.gif &&
# ffmpeg -ss 0 -t 10 -i $NAME -i palette.png -filter_complex "fps=24,scale=728:-1:flags=lanczos[x];[x][1:v]paletteuse" -loop 2 ${filename}_LOOP2.gif &&
# ffmpeg -ss 0 -t 10 -i $NAME -i palette.png -filter_complex "fps=24,scale=728:-1:flags=lanczos[x];[x][1:v]paletteuse" -loop -1 ${filename}_NOLOOP.gif &&
# ffmpeg -ss 0 -t 10 -i $NAME -i palette.png -filter_complex "fps=30,scale=1024:-1:flags=lanczos[x];[x][1:v]paletteuse" -loop 0 ${filename}_LOOP_FOREVER.gif &&
ffmpeg -ss 0 -t 10 -i $NAME -i palette.png -filter_complex "fps=24:-1:flags=lanczos[x];[x][1:v]paletteuse" -loop 0 ${filename}_LOOP_FOREVER.gif &&

echo "GENERATING HTML PAGE"

cat > index.html << EOF1
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="description" content="GIFs">
  <meta name="author" content="Metaboy.tech">
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #EEE;
    }
    .add {
      width: 100%;
      height: 100%;
      display: block;
      position: absolute;
    }
    #gif {
      position: relative;
      top: 50%;
      transform: translateY(-50%);
      width: auto;
      height: 600px;
      display: block;
      margin: 0 auto;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="add">
    <div id="gif">
      <p><img src="${filename}_LOOP_FOREVER.gif"></p>
    </div>
  </div>
</body>
</html>
EOF1

echo "READY!"