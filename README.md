# Fast DKIM Scanner
This tool enables brute-forcing DKIM keys of a domain to identify weak keys or detect a lack of proper key rotation practices.
This is a tool similar to https://github.com/vavkamil/dkimsc4n or https://github.com/ryancdotorg/dkimscan. 

It is more efficient than the other tools since:
1. It generates a custom list of DKIM selectors based on the domain name.
2. It uses massdns to retrieve the records from the DNS servers.

# Requirements
- Python 3 + tldextract + cryptography
- massdns
  
You can run ```bash setup.sh``` to install the required python library (tldextract) and clone + build massdns.

# How to run
## Standalone generator
To generate the bruteforce list:
```python3 generate_dkim_selectors.py <domain> > dkim_selectors.txt ```

## Domain scanning
To bruteforce a domain's DKIM keys and detect weak RSA keys:
```python3 get_dkim_from_domain.py <domain> ```

![image](https://github.com/user-attachments/assets/56c4e0b4-6229-4894-8c3a-6a10a776c2ec)

![image](https://github.com/user-attachments/assets/f7ea5052-d5e3-4aa1-b0c5-9e1a65249809)

