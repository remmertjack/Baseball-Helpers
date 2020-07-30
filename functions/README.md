# Baseball-Helpers: Functions
### Designed to aide in preprocessing and data collection.
***

##### FanGraphs_ServiceTime (as of July 30th, 2020)
  This function will webscrape the service time of a player from FanGraphs. For example, Manny Machado with Player Id 11493, has a service time of 7.15 as of April 30th, 2020. It requires the name and Player Id (from fangraphs of course). Requires `bs4` (*beautifulsoup4*), `urllib.request`, and `time` packages. However, given it is a webscraping function I included a system sleep for 5 seconds when the function is first called. Additionally, since it is a webscraping function, it may be better to execute in a loop to control the system with sleeps and progress checkers.
  ```python
  from Baseball-Helpers.functions.FanGraphs_ServiceTime import get_service_time
  name = "Manny Machado"
  f_id = 11493
  get_service_time(name, f_id)
  # 7.15
  
  # OR in a dataframe:
  df['service_time']=df[['name','f_id']].apply(lambda x: get_service_time(x['name'], x['f_id']), axis=1)
  
  # OR in a loop:
  import time
  i=0
  st = [] 
  for player in df:
      name = player['name']
      f_id = player['f_id']
      service_time = get_service_time(name,f_id)
      st.append(service_time)
      i+=1
      if i % round(len(df)/10)==0:
        # print progress
          progress= round(i/len(df)*100,1)
          print(progress+"% complete")
          time.sleep(10)
  ```
