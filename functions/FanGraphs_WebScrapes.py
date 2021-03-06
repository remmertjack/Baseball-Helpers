import bs4 as bs
import urllib.request
import time
import datetime

def get_service_time(name,f_id):
    time.sleep(5)
    # remove any periods such as those in Jr. or Sr.
    name = name.replace(".","")
    # remove any spaces and replace with dashes
    name = name.replace(" ","-")
    # convert to lowercase
    name = name.lower()
    
    # url
    try: 
        address=("https://www.fangraphs.com/players/"+name+"/"+str(f_id)+"/stats")
        # submit and read url
        source = urllib.request.urlopen(address).read()      
        soup = bs.BeautifulSoup(source,"html")
    except:
        err = "No webpage for "+str(f_id)+" , Name: "+name
        return err
    
    try:
        # find tag for service time
        svt_html = soup.find_all('div', class_='tool-tip-item')[0]
        # split on the period since svt_html returns 2 sentences
        svt_html = svt_html.text.split(".")
        # remove excess values. First remove the Reported...
        svt_html.remove("Reported as the pre-2020 value")
        # then remove the excess space
        svt_html.remove('')
        # check to see if working with the string X years and Y days of service time
        if len(svt_html) !=1:
            err = "Error with getting Service Time for "+str(f_id)+" , Name: "+name
            return err
        else:
            # force back into a string
            svt_html = svt_html[0]
            # extract the integers
            ints = [int(s) for s in svt_html.split() if s.isdigit()]
            # we know the first value is the year and the second is number of days
            service_time = ints[0] + ints[1]/172
            return service_time
    except:
        err = "No Service Time webpage tag for "+str(f_id)+", Name: "+name
        return err

# name = "Manny Machado"
# f_id =  11493       
# get_service_time(name,f_id)
        
def get_bats_(name,f_id):
    time.sleep(3)
    # remove any periods such as those in Jr. or Sr.
    name = name.replace(".","")
    # remove any spaces and replace with dashes
    name = name.replace(" ","-")
    # convert to lowercase
    name = name.lower()
    
    # url
    try: 
        address=("https://www.fangraphs.com/players/"+name+"/"+str(f_id)+"/stats")
        # submit and read url
        source = urllib.request.urlopen(address).read()      
        soup = bs.BeautifulSoup(source,"html")
    except:
        err = "No webpage for "+str(f_id)+" , Name: "+name
        return err
    
    try:
        # find tag for bats throws
        bt = soup.find_all('div', class_='player-info-box-item')[1].text
        # split on : and get the Bats/Throws Value
        bt = bt.split(": ")[-1]
        return bt[0]
    except:
        err = "No Bats Throws webpage tag for "+str(f_id)+", Name: "+name
        return err

def get_throws_(name,f_id):
    time.sleep(3)
    # remove any periods such as those in Jr. or Sr.
    name = name.replace(".","")
    # remove any spaces and replace with dashes
    name = name.replace(" ","-")
    # convert to lowercase
    name = name.lower()
    
    # url
    try: 
        address=("https://www.fangraphs.com/players/"+name+"/"+str(f_id)+"/stats")
        # submit and read url
        source = urllib.request.urlopen(address).read()      
        soup = bs.BeautifulSoup(source,"html")
    except:
        err = "No webpage for "+str(f_id)+" , Name: "+name
        return err
    
    try:
        # find tag for bats throws
        bt = soup.find_all('div', class_='player-info-box-item')[1].text
        # split on : and get the Bats/Throws Value
        bt = bt.split(": ")[-1]
        return bt[-1]
    except:
        err = "No Bats Throws webpage tag for "+str(f_id)+", Name: "+name
        return err
    
    
def is_retired(name, sr = 1):
    time.sleep(3)
    # convert to lowercase
    name = name.lower()
    # remove any periods such as those in Jr. or Sr.
    name = name.replace(".","")
    # extract first and last name (only need last 5 chars of last name)
    first = name.split(" ")[0]
    last =  name.split(" ")[1][0:6]
    # first letter of the last name
    f_last = last[0]
    # first time of the first name
    f_first = first[:2]
    # is player first of his name?
    count = str(sr)
    count = "0"+count if len(count)<10 else sr
    
    
    # build unique identifier for bbreference
    bbid = "/"+f_last+"/"+last+f_first+count+".shtml"
    
    # url
    try: 
        address=("https://www.baseball-reference.com/players"+bbid)
        # submit and read url
        source = urllib.request.urlopen(address).read()      
        soup = bs.BeautifulSoup(source,"html")
    except:
        err = "No webpage for "+name
        return err
    
    {"id":"div_transactions_other"}
    try:
        # find tag for transactions
        svt_html = soup.find_all("div", class_="section_content")
        # split on the period since svt_html returns 2 sentences
        svt_html = svt_html.text.split(".")
        # remove excess values. First remove the Reported...
        svt_html.remove("Reported as the pre-2020 value")
        # then remove the excess space
        svt_html.remove('')
        # check to see if working with the string X years and Y days of service time
        if len(svt_html) !=1:
            err = "Error with getting Service Time for "+str(f_id)+" , Name: "+name
            return err
        else:
            # force back into a string
            svt_html = svt_html[0]
            # extract the integers
            ints = [int(s) for s in svt_html.split() if s.isdigit()]
            # we know the first value is the year and the second is number of days
            service_time = ints[0] + ints[1]/172
            return service_time
    except:
        err = "No Service Time webpage tag for "+str(f_id)+", Name: "+name
        return err


def get_birthday(name, f_id):
    time.sleep(3)
    # remove any periods such as those in Jr. or Sr.
    name = name.replace(".","")
    # remove any spaces and replace with dashes
    name = name.replace(" ","-")
    # convert to lowercase
    name = name.lower()
    # url
    try: 
        address=("https://www.fangraphs.com/players/"+name+"/"+str(f_id)+"/stats")
        # submit and read url
        source = urllib.request.urlopen(address).read()      
        soup = bs.BeautifulSoup(source,"html")
    except:
        err = "No webpage for "+str(f_id)+" , Name: "+name
        return err
    
    try:
        # find tag for bats throws
        bt = soup.find_all('tr', class_='player-info__bio-birthdate')[0].text
        # split on : and get the Bats/Throws Value
        bt = bt.split(": ")[1].split(" ")[0]
        bt_obj = datetime.datetime.strptime(bt, '%m/%d/%Y')
        today = datetime.datetime.now()
        days = abs((today-bt_obj).days)
        return days/365.25

    except:
        err = "No Birthday tag for "+str(f_id)+", Name: "+name
        return err