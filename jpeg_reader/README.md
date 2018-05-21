### Pelican JPEG Reader.

Original author: [Mitchell Currie](https://github.com/mitchins)

##### Requirements:

* Python3
* Pelican
* Pillow library (PIL for python3)
* Exiv2 binary accessible by $PATH

To avoid undesired creation of content, the specific extension must be `jpeg_article`, i.e. "myPhoto.jpeg_article", it's a regular JPEG image, but this avoids your other JPEG images getting picked up. It can work for pages or blogs, and determines based on whether it's `content/blog` or `content/pages` (or whatever you use for content).

#### Most relevant EXIF/IPTC flags from Exiv2 that are used

|  Page/Article Field | Exiv2 Key  |  Description |
|---|---|---|
| title  | `Exif.Image.ImageDescription`  |  Defaults to 'Untitled' |
| author  | `Exif.Image.Artist`  |  Default to Unknown. Currently Scalar |
| date  |  `Exif.Photo.DateTimeOriginal` |  Undefined behaviour if not present as required |
|  slug |  `Iptc.Application2.Headline` |  Defaults to title's value |
|  body |  `Exif.Photo.UserComment` |  This goes under image in page/article, blank default |
|  summary |  `Iptc.Application2.Caption` |  Used for article index, defaults to first 140 characters of the body |
|  category |  `Iptc.Application2.SuppCategory` |  Specifies the category of page/article if `USE_FOLDER_AS_CATEGORY` not set  |
|  template |  `Iptc.Application2.ObjectName` |  If specified will set the template metadata property to tell pelican where to look  |
|  tags |  `Iptc.Application2.Keywords` |  For each entry found with this key, a tag is created with the value of the entry |
|  `metadata['exiv2']` | ***Everything***|  All exiv2 fields from the image are shoved into the metadata dictionary of the item, under `exiv2` key for template usage |



#### Pelican Settings Added or Honoured:

|  Key in pelicanconf.py |  Description |
|---|---|
| `PATH`  |  **Content Path** |
| `OUTPUT_PATH` |  **Output Path** |
| `USE_FOLDER_AS_CATEGORY` | **Category from folder name** If enabled, takes the category from the name of the folder the file is in. Otherwise the category will attempt to be read from `Iptc.Application2.SuppCategory` |
|  `SITEURL` | **Site Url** The optional absolute Url for the site, defaults to '' usually. |
|  `PAGE_URL` | **Page Url** The format string to specify where page html files are saved to |
|  `PAGE_SAVE_AS` | **Page Save Path** The format string to specify where page html files are physically written to disk |
|  `ARTICLE_URL` | ** Article Url** The format string to specify where page html files are saved to |
|  `ARTICLE_SAVE_AS` | **Article Save Path** The format string to specify where page html files are physically written to disk |



