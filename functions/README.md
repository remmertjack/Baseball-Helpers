# Baseball-Helpers: Functions
### Designed to aide in preprocessing and data collection.
***

##### FanGraphs_ServiceTime (as of July 30th, 2020)
  This function will webscrape the service time of a player from FanGraphs. For example, Manny Machado with Player Id 11493, has a service time of 7.15 as of April 30th, 2020. It requires the name and Player Id (from fangraphs of course). Requires `bs4` (*beautifulsoup4*) and `urllib.request` packages.
  ```python
  from Baseball-Helpers.functions.FanGraphs_ServiceTime import get_service_time
  name = "Manny Machado"
  f_id = 11493
  get_service_time(name, f_id)
  # 7.15
  
  # OR in a pandas dataframe
  df['service_time']=df[['name','f_id']].apply(lambda x: get_service_time(x['name'], x['f_id']), axis=1)
  ```
