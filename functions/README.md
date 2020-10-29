# Baseball-Helpers: Functions
### Designed to aide in preprocessing and data collection.

#### FanGraphs_WebScrapes (as of July 30th, 2020)
  This family of functions provides a lot of basic webscrapers for the FanGraphs site. For any of these functions, they require a Player Name and their FanGraphs Id. They also all work very much the same: request the url given the inputs of the function, find the desired data from any div and class tags, extract said data, and return the value. I may look into creating a wrapper function in which the user can select their desired data, like Service Time, Batting Style (R,L,S) and Throwing Style (R,L), to scrape, then the function queries the url and extracts the desired data.
  
  Requires `bs4` (*beautifulsoup4*), `urllib.request`, and `time` packages.
  
  Given these are a webscraping functions I included a system sleep for 5 seconds when the function is first called. Additionally, since it is a webscraping function, it may be better to execute in a loop to control the system with sleeps and progress checkers.
  
Basic Process:
  ```python
from Baseball-Helpers.functions.FanGraphs_WebScrapes import myfunction
name = "Manny Machado"
f_id = 11493
myfunction(name, f_id)
  
# OR in a dataframe:
df['service_time']=df[['name','f_id']].apply(lambda x: myfunction(x['name'], x['f_id']), axis=1)
  
# OR in a loop:
import time, math
i=0
mod_check = math.ceil(len(df)/10)
st = [] 
for index, player in df.iterrows():
    name = player['name']
    f_id = player['f_id']
    service_time = myfunction(name,f_id)
    st.append(service_time)
    i+=1
    if i % mod_check ==0:
        # print progress
        progress = round(i/len(df)*100,1)
        print(str(progress)+"% complete")
        time.sleep(10)
```
*****
##### The Functions:
###### * get_service_time  
  This function will webscrape the service time of a player from FanGraphs. For example, Manny Machado with Player Id 11493, has a service time of 7.326 as of April 30th, 2020. It requires the name and Player Id (from fangraphs of course).  

  The service time is the number of years + days/172. For example, Manny Machado with 7 years of service and 56 service days is 7 + 56/172. We divided by 172 because 172 service days is 1 service year.
  
   If the player has retired, Fangraphs removes their Service Time, which for the life me I cannot understand why, and the function will print `"No Service Time webpage tag for $id, Name: firstname-lastname"`.  Any tips on how to correct for this, please email me.
 
###### * get_bats_ & get_throws_
   Retireves the Batting and Throwing Handness of the player. For example, for Mike Trout with id of 10155, `get_bats_` will return R and `get_throws_` will return R.
