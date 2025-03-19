#!/usr/bin/env python3

import generate_dkim_selectors
import argparse
import os
import subprocess
import re
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes


folder_name = "output"

def extract_and_save_dkim_keys(domain):    
    print(f"[1] Generating the DKIM keys for: {domain}")
    keys = generate_dkim_selectors.get_keys(domain)
    print( "{0} keys generated".format(len(keys)))
    # Check if folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    
    # Write each key
    filename = folder_name+f"/dkim_{domain}.txt"
    with open(filename, "w") as file:
        for key in keys:
            file.write(key+f"._domainkey.{domain}" + "\r\n")  # Write the DNS name of each key:  $key._domainkey.$domain

    return filename


def run_massdns(dkimfilename,domain):
    print(f"[2] Running MassDNS for all the domains defined in {dkimfilename} [...]")
    outputfile = f"{folder_name}/results_{domain}.txt"

    subprocess.run(["./massdns/bin/massdns", "-q", "-r", "./massdns/lists/resolvers.txt", "-t", "TXT", "-w", outputfile, dkimfilename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
    
    answers = [] # array of DNS result

    # Parse MassDNS result
    with open(outputfile, "r") as file:
        for line in file:
            # Search for "ANSWER: {num}" where num > 0
            match = re.search(r"ANSWER: ([1-9]\d*)", line)  # Matches any number > 0
            if match:
                num = int(match.group(1))
                ## ANSWER > 0
                break  # Stop looping once we find an answer with num > 0
            # Get to the ANSWER SECTION
            for next_line in file:
                    if ";; ANSWER SECTION:" in next_line:
                        answer = next(file, None)
                        answers.append(answer)
                        break

    print("[*] {0} DNS answers".format(len(answers)))
    return answers

def parse_dns_answers(answers):
    print("[3] Parsing the massdns answers")
    for answer in answers:
        match = re.search(r"^(.*?)\._domainkey", answer)
        if match:
            selector = match.group(1)  # Get the extracted value
        else:
            print("Couldn't extract the domain key from " + answer)
            break;

        print(f"[*] !! Key found: \033[32m {selector} \033[0m" )

        ## Extract the DNS TXT value
        matches = re.findall(r'"([^"]*)"', answer)

        if matches:
            joined_answer = ' '.join(matches)

            print(f' TXT Value: {joined_answer}')  # Extracts the first match
        else:
            print(" No TXT value for: " + answer)
            break;

        # extract the p=
        match = re.search(r'p=([^";]+)', joined_answer)

        if match:
            extracted_p = match.group(1)  # Extract the value
            print(f' Extracted p-value: {extracted_p}')
        else:
            print(" No p-value found.")
            break;
            

        pem_public_key = f"""
        -----BEGIN PUBLIC KEY-----
        {extracted_p}
        -----END PUBLIC KEY-----
        """

        try:
            # Load the PEM public key
            public_key = serialization.load_pem_public_key(
                pem_public_key.encode(), backend=default_backend()
            )

            # Check if the key is RSA
            if isinstance(public_key, rsa.RSAPublicKey):
                key_size_bits = public_key.key_size  # Get the RSA key size in bits
                if key_size_bits < 1024:

                        print(f" \033[31m !!!  Weak RSA Public Key Size: {key_size_bits} bits on selector {selector} \033[0m ")
                else:
                    print(f" [*] RSA Public Key Size: {key_size_bits} bits on selector {selector}")
            else:
                print(" The public key is not RSA.")
                
        except Exception as e:
            print(f" Error loading public key: {e}")


def main():
    parser = argparse.ArgumentParser(description="Bruteforce DKIM keys of a domain name.")
    parser.add_argument("domain", help="The domain name to process")
    args = parser.parse_args()

    dkimfilename = extract_and_save_dkim_keys(args.domain)
    
    answers = run_massdns(dkimfilename, args.domain)

    parse_dns_answers(answers)

   
if __name__ == "__main__":
    main()


