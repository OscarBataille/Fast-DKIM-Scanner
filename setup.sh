#!/bin/sh

pip install tldextract
git clone https://github.com/blechschmidt/massdns
cd massdns && make 
