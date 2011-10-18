for FILE in $(ls tests/*py)
do
    python globaleaks/web2py.py -S globaleaks -M -R ../${FILE}
done
