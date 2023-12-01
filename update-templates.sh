for dir in */; do
    echo "Copying template to $dir..."
    [ "${dir%/}" != "template" ] && rm -r "$dir/template" && rm -r "$dir/*.sh"
    rsync -avr template/template "$dir"
done
