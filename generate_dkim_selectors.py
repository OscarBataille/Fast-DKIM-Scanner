
import datetime 
import sys
import tldextract

selectors = ['default',
             'google', 
             'bedrock', 'bk',
             'bmy',
             'dkim1k', 'dkim2k',
             'intercom',
             'emv',
             'flexmail',
             'gears',
             'ire',
             'itb',
             'kl',
             'litesrv',
             'mail',
             'www',
             'mandrill',
             'mailout',
             'mailster',
             'mg',
             'mta',
             'mx',
             'neolane',
             'oraclersys',
             'prd',
             'prod',
             'tst',
             'test',
             'relay',
             'relaydkim',
             'spop'
             'postfix',
             'dkimpr',
             'mymail',
             'sms',
             'phpmailer',
             'brisbane',
             'ga',
             'yibm',
             'dkimrnt',
             'gamma',
             'mt',
             'bounce',
             'harold',
             'delta',
             # 'pp-dkim',
             # 'pp-epsilon',
             # 'pp-alpha',
             # 'pp-beta',
             # pp-gamma',
             # 'p-omega',
             'ED-DKIM-V',
             'pf',
             'exim',
             'smtp',
             'cisco'

             ]
selectors_with_key = [
                      'proddkim',
                      'testdkim',
                      'dk',
                      'rsa',
                      'spop', 
                      'sp', 
                      'a', 
                      'dkim',
                      'acy',
                      'gmmailerd',
                      'd'

                      ]

selectors_with_numbers = [
                            's', 
                            'selector', 
                            'sel', 
                            'sl',
                            'k', 
                            'cs', 
                            'key', 
                            'hs', 
                            'm', 
                            'my',
                            'salesforce', 
                            'sf', 
                            'smtp', 
                            'zendesk', 
                            'fm',  
                            'e', 
                            'email', 
                            'krs', 
                            'mailjet', 
                            'p', 
                            'pf',
                            'selectorprod', 
                            'selectortest', 
                            'ser', 
                            'sim', 
                            'smtp', 
                            'smtpapi', 
                            'stxsel',
                            'v',
                            'x',
                            'ei',
                            'maxer',
                            'n',
                            'arc'

                         ]

key_sizes = ['384', '512', '768', '1024', '2048']


def get_keys(domain = None):
    output = []

    # If the domain is submitted as the first parameter, then uses it for the wordlist
    if(domain and len(domain) >= 2 ):
        selectors.append(domain) # instagram.com
        selectors.append(tldextract.extract(domain).domain) # instagram.com => instagram
    # Step 1: Output the arrays without any processing
    allData = selectors + selectors_with_key + selectors_with_numbers + key_sizes   
    for x in allData:
        output.append(x)

    # Step 2: Append the key sized to the selectors_with_key
    allSelectorsWithKey = []

    for sel_with_key in selectors_with_key:
        for keysize in key_sizes:
            allSelectorsWithKey.append(sel_with_key + "-" + keysize)                   # ex: dkim-1024
            allSelectorsWithKey.append(sel_with_key + keysize)  # ex: dkim1024
    for x in allSelectorsWithKey:
        output.append(x)

    #Step 3: Append the number to the selectors_with_numbers
    allSelectorsWithNumbers = []

    for sel_with_number in selectors_with_numbers:
        for value in range(1, 20):               # 1 to 10
            allSelectorsWithNumbers.append(sel_with_number + "-" + str(value)) # cs-1
            allSelectorsWithNumbers.append(sel_with_number + str(value) )       # cs1
            allSelectorsWithNumbers.append(sel_with_number + "-" + str(value).zfill(2)) # cs-01
            allSelectorsWithNumbers.append(sel_with_number + str(value).zfill(2) )       # cs01

    for x in allSelectorsWithNumbers:
        output.append(x)

    # Step 4: Append the number to the other selectors
    allOtherSelectorsWithNumbers = []

    for other_sel_with_number in selectors + selectors_with_key + key_sizes:
         for value in range(1, 20):
             allOtherSelectorsWithNumbers.append(other_sel_with_number + "-" + str(value))
             allOtherSelectorsWithNumbers.append(other_sel_with_number +  str(value))
             allOtherSelectorsWithNumbers.append(other_sel_with_number + "-" + str(value).zfill(2))
             allOtherSelectorsWithNumbers.append(other_sel_with_number +  str(value).zfill(2))

    for x in allOtherSelectorsWithNumbers:
        output.append(x)

    # Step 4: Generate dates
    today = datetime.date.today()


    ## Years from 2005
    years = []
    for year in range (2005,today.year):
        years.append(str(year))

    for year in range (5, int(str(today.year)[-2:])): # 5 to 23
        years.append(str(year).zfill(2))

    for year in years:
        output.append(year)

    ## Months from 2005
    months = []
    for year in years:
        for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            months.append(month + year)       #jan2022 jan22
            months.append(month+ "-" + year)  #jan-2022 jan-22
            months.append(year + month )       #2022jan 22-jan
            months.append( year + "-" + month)  #2022-jan  22jan

        for month in range(1, 12):
            months.append(year+str(month).zfill(2)) # 202208 2208
            months.append(year+"-"+str(month).zfill(2)) # 2022-08 22-08
            months.append(str(month).zfill(2) + year) # 082022 0822
            months.append(str(month).zfill(2) + "-" + year) # 08-2022 08-22

        for quarter in range(1, 4):
            months.append(str(year) +"-q"+ str(quarter)) #2022-q1
            months.append(str(year) +"q"+ str(quarter)) # 2022q1
            months.append("q"+ str(quarter)+ str(year) ) # q12022

    months = list(set(months))


    
    for month in months:
        output.append(month)

   

    # Step 5 Prepend Year to all selectors
    allSelectorsWithYear = []
    for sel in allData:
        for year in years:
            allSelectorsWithYear.append(sel + year)
            allSelectorsWithYear.append(sel + "-" + year) # -2025

    for x in allSelectorsWithYear: 
        output.append(x)


    # Step 6: Preprend Months to all selectors
    allSelectorsWithMonth = []
    for sel in allData:
        for month in months:
            allSelectorsWithMonth.append(sel + month)
            allSelectorsWithMonth.append(sel + "-" + month) 

    for x in allSelectorsWithMonth: 
        output.append(x)

    # Step 6: Prepend the key size to all the other selectors (except key sizes)
    allOtherSelectorsWithKeys = []
    for sel in selectors  + selectors_with_numbers :
        for keysize in key_sizes:
            allOtherSelectorsWithKeys.append(sel + "-" + keysize)  # ex: dkim-1024
            allOtherSelectorsWithKeys.append(sel + keysize)  # ex: dkim1024

    for x in allOtherSelectorsWithKeys:
        output.append(x)
    

    # Make sure each entry is unique
    output = list(set(output))


    return output

## If standalone
if __name__ == "__main__":
    # If the domain is submitted as the first parameter, then use it for the wordlist
    keys = get_keys(sys.argv[1] if len(sys.argv) >= 2 else None)


    for x in keys:
        print(x)



