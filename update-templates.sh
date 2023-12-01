for dir in */; do
    dir="${dir%/}"
    echo "Copying template to $dir..."
    if [ "$dir" != "template" ]; then
        if [ -d "$dir/template" ]; then
            rm -r "$dir/template"
        fi
        for f in "$dir"/*.sh; do
            rm "$f"
        done
    fi
    rsync -ar template/template "$dir"
    rsync -ar template/*.sh "$dir"
done
