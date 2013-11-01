#!/bin/sh

cd static/books
find . -name "*.epub" -exec ebook-convert {} {}.mobi \;
find . -name "*.epub.mobi" -exec rename 's/\.epub\.mobi$/.mobi/' {} +
find . -name "*.epub" -exec rm {} \;
