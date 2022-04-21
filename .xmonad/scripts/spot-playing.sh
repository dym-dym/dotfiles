running=$(pidof spotify)
if [ "$running" != "" ]; then
    artist=$(playerctl metadata artist)
    song=$(playerctl metadata title | cut -c 1-60)
    echo -n "<fc=#666666>|</fc> Now Playing : $artist · $song"
fi
