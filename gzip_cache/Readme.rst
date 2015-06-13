Gzip cache
----------

Certain web servers (e.g., Nginx) can use a static cache of gzip-compressed
files to prevent the server from compressing files during an HTTP call. Since
compression occurs at another time, these compressed files can be compressed
at a higher compression level for increased optimization.

The ``gzip_cache`` plugin compresses all common text type files into a ``.gz``
file within the same directory as the original file.
