#!/bin/sh

PAGE_PATH="content/pages"
ARTICLE_PATH="content/posts"
IMAGE_PATH="content/images"
FILE_PATH="content/files"

IMAGE_URL="/images/"
FILE_URL="/files/"

# Set to "1" if all files should be converted.
# Otherwise only files containing image links are converted.
CONVERT_ALL_FILES=0

MKDIR="mkdir -p"
MV="git mv"
SED="sed"
## All modifying commands can be switched to DRY-mode by uncommenting te following lines
#MKDIR="echo mkdir -p"
#MV="echo git mv"
#SED="echo sed"

rename_markdown_files() {
  for md_file in $PAGE_PATH/*.md $ARTICLE_PATH/*.md
  do
    [ -e "$md_file" ] || continue
    tb_file="${md_file/.md/.textbundle}"
    grep -qE '\!\[.*\]\([^ \)]*' "$md_file" /dev/null
    if [ $? == 0 -o $CONVERT_ALL_FILES ]
    then
      echo "Convert '$md_file'"
      $MKDIR "$tb_file/assets"
      $MV "$md_file" "$tb_file/text.md"
    else
      echo "Skip '$md_file', because it doesn't contain image links."
    fi
  done
}

create_metadata() {
  for tb_file in $PAGE_PATH/*.textbundle $ARTICLE_PATH/*.textbundle
  do
    test -e "$tb_file/info.json" || cat > "$tb_file/info.json" <<INFOJSON
{
  "version":              1,
  "transient":            false,
  "creatorURL":           "http://getpelican.com/",
  "creatorIdentifier":    "https://github.com/DirkR/pelican-textbundle"
}
INFOJSON
  done
}

move_assets() {
  echo '# Apache Rewrite rules for moved assets' > assets_htaccess_fragment.txt
  for tb_file in $PAGE_PATH/*.textbundle $ARTICLE_PATH/*.textbundle
  do
    md_file="$tb_file/text.md"
    [ -e "$md_file" ] || continue
    for asset in $(perl -n -e '/\[.*\]\((\/[^ \)]*)/ && print "$1\n"' "$md_file")
    do
      if [ -z "${asset##*$IMAGE_URL*}" -o -z "${asset##*$FILE_URL*}" ]
      then
        rel_path=$(echo $asset | $SED -e "s!^($IMAGE_URL|$FILE_URL)!!")
        asset_name=$(basename $asset)
        [ -d "$tb_file/assets" ] || MKDIR "$tb_file/assets"
        $MV "content$asset" "$tb_file/assets/$asset_name"
        slug=$(perl -n -e '/slug\s*:\s*(.+)/ && print $1' "$tb_file/text.md")
        if [ ! -z "$slug" ]
        then
          echo "RewriteRule ^$asset /post/$slug/assets/$asset_name [R=301,L]" >> assets_htaccess_fragment.txt
        fi
        $SED -i.bak -e "s|$asset|assets/$asset_name|g" "$md_file"
      fi
    done
  done
}

rename_markdown_files
create_metadata
move_assets