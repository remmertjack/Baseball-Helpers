# Baseball-Helpers: Functions
### Designed to aide in preprocessing and data collection.
***

##### FanGraphs_ServiceTime (as of July 30th, 2020)
  This function will webscrape the service time of a player from FanGraphs. For example, Manny Machado with Player Id 11493, has a service time of 7.326 as of April 30th, 2020. It requires the name and Player Id (from fangraphs of course). Requires `bs4` (*beautifulsoup4*), `urllib.request`, and `time` packages. However, given it is a webscraping function I included a system sleep for 5 seconds when the function is first called. Additionally, since it is a webscraping function, it may be better to execute in a loop to control the system with sleeps and progress checkers.

  The service time is the number of years + days/172. For example, Manny Machado with 7 years of service and 56 service days is 7 + 56/172. We divided by 172 because 172 service days is 1 service year.
  
   If the player has retired, Fangraphs removes their Service Time, which for the life me I cannot understand why, and the function will print `"No Service Time webpage tag for $id, Name: firstname-lastname"`.  Any tips on how to correct for this, please email me or comment down below!
  
  ```python
from Baseball-Helpers.functions.FanGraphs_ServiceTime import get_service_time
name = "Manny Machado"
f_id = 11493
get_service_time(name, f_id)
# 7.326
  
# OR in a dataframe:
df['service_time']=df[['name','f_id']].apply(lambda x: get_service_time(x['name'], x['f_id']), axis=1)
  
# OR in a loop:
import time, math
i=0
mod_check = math.ceil(len(df)/10)
st = [] 
for index, player in df.iterrows():
    name = player['name']
    f_id = player['f_id']
    service_time = get_service_time(name,f_id)
    st.append(service_time)
    i+=1
    if i % mod_check ==0:
        # print progress
        progress = round(i/len(df)*100,1)
        print(str(progress)+"% complete")
        time.sleep(10)
  ```
