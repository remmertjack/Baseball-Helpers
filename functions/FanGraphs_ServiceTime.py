import bs4 as bs
import urllib.request

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
            service_time = ints[0] + ints[1]/365.25
            return service_time
    except:
        err = "No Service Time webpage tag for "+str(f_id)+", Name: "+name
        return err

# name = "Manny Machado"
# f_id =  11493       
# get_service_time(name,f_id)
    

