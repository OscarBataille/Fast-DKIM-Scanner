#!/bin/sh

pip install tldextract cryptography
git clone https://github.com/blechschmidt/massdns
cd massdns && make 
