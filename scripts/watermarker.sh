#!/usr/bin/env bash

. scripts/variables.sh

for i in $res_path/png/*.png; do
    # Добавляет ссылку на контактную 
    # информацию автора рисунков
    convert $i -background White label:'http://vk.com/zharnasek' -gravity SouthEast -append $i
    convert $i -threshold 75% -negate mask.png
    convert $i -alpha Off mask.png -compose CopyOpacity -composite $i
    rm mask.png
done
