#!/usr/bin/env bash

. scripts/variables.sh

for i in $src_path/bmp/*.bmp; do
    # Разделяет страницу на 6 отдельных файлов
    # Первый индекс -- номер столбца (нумерация слева направо)
    # Второй -- номер строки (нумерация сверху вниз)
    # Заодно конвертирует в png
    
    f_name=`basename ${i%.*}`
    
    convert -crop 2014x1506+356+720   $i $res_path/png/${f_name}_1_1.png
    convert -crop 2014x1506+356+2754  $i $res_path/png/${f_name}_1_2.png
    convert -crop 2014x1506+356+4788  $i $res_path/png/${f_name}_1_3.png
    convert -crop 2014x1506+2587+720  $i $res_path/png/${f_name}_2_1.png
    convert -crop 2014x1506+2587+2754 $i $res_path/png/${f_name}_2_2.png
    convert -crop 2014x1506+2587+4788 $i $res_path/png/${f_name}_2_3.png
done

for i in $res_path/png/*.png; do
    # Обрезает поля картинки так, 
    # чтобы осталось по 10 пикселов по контуру
    # от краев собственно изображения
    convert -trim  -bordercolor white -border 10x10 $i $i
done
