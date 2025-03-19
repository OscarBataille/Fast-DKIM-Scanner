# Fast DKIM Scanner
This tool enables brute-forcing DKIM keys of a domain to identify weak keys or detect a lack of proper key rotation practices.
This is a tool similar to https://github.com/vavkamil/dkimsc4n or https://github.com/ryancdotorg/dkimscan. 

It is more efficient than the other tools since:
1. It generates a custom list of DKIM selectors based on the domain name.
2. It uses massdns to retrieve the records from the DNS servers.

# Requirements
- Python 3 
- massdns
You can run ```bash setup.sh``` to install the required python library (tldextract) and clone massdns.

# How to run
## Standalone generator
To only run the DKIM key bruteforce list and save it to a file "output":
```python3 generate_dkim_selectors.py <domain> > dkim_selectors.txt ```

## Domain scanning
To bruteforce a domain's DKIM keys:
```python3 generate_dkim_selectors.py <domain> ```

