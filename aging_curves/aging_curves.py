'''
Project: Aging Curves
Author: Jack Remmert
Date: April 11, 2020
'''
# import packages
import pandas as pd
import numpy as np
from scipy import stats
from plotnine import *

# import helper functions

# user helper functions

# user defined functions
def myround(x, base=5):
    return base * round(x/base)

# user preferences
pd.options.mode.chained_assignment = None 

'''
Aging Curve Functions
'''
def delta_method(playerid, age, stat, weight = None):
    '''
    Creates and Aging Curve based on the delta method.
    Returns Pandas DataFrame object: ac_data (aging curve data).
    
    playerid and age should be self explanatory.
    stat is the value of the stat you want to caluclate the Aging Curve for.
    weight is the vairable you would like to weight the stat by.
    
    Columns Names: age, n, ac
        age : Age
        n : Total Number of Players in that Age cohort
        ac : Year over year change of stat per player,
            weighted by weighting variable
        
    Useful links: 
        https://mglbaseball.com/2016/12/21/
            a-new-method-of-constructing-more-accurate-aging-curves/
        https://www.beyondtheboxscore.com/2011/5/31/2199146/hitter-aging-curves
        https://blogs.fangraphs.com/pitcher-aging-curves-introduction/
    '''
    # read additional optional arguments and set defults if nonexistent
    weight = pd.Series(1).repeat(len(playerid)) if weight is None else weight
    # combine into dataframe and rename
    df = pd.concat([playerid, age, stat, weight], axis=1)
    cols = ['playerid','age','stat','weight']
    df.columns = cols
    # inclusion principle, i.e. played at least two seasons
    incl_prin = df.playerid.value_counts().reset_index()
    incl_prin = incl_prin.loc[incl_prin.playerid > 1]
    # filter
    df = df.loc[df.playerid.isin(list(incl_prin['index']))]
    # order by playerid, age. We sort to make it easier.
    df = df.sort_values(by=['playerid','age'])
    df['w_hm'] = None
    df['delta'] = None
    for player in df.playerid.unique():
        plyr = df.loc[df.playerid == player]
        list_ages = iter(plyr.age[1:])
        for ag in list_ages:
            if ag-1 not in list(plyr.age):
                pass
            else:
                # adjust to harmonic mean
                w_yr0 = plyr.weight.loc[plyr.age == ag-1].values[0]
                w_yr1 = plyr.weight.loc[plyr.age == ag].values[0]
                w_hm = stats.hmean([w_yr0, w_yr1])
                # difference between yr0 and yr1
                s_yr0 = plyr.stat.loc[plyr.age == ag-1].values[0]
                s_yr1 = plyr.stat.loc[plyr.age == ag].values[0]
                delta = s_yr1 - s_yr0
                # index of value
                ind = df.index[(df.playerid == player) 
                                & (df.age == ag)].tolist()[0]
                # set value in dataframe
                df.at[ind, 'w_hm'] = w_hm
                df.at[ind, 'delta'] = delta
    
    # remove Nulls
    df = df.loc[df.w_hm.notnull()]
    # Mulitply to find weighted difference stat
    df['w_hmXdelta'] = df.w_hm * df.delta
    # aggregate by Age
    ac_data = df.groupby('age').agg({'weight':'size' # use weight as counter
                            ,'w_hmXdelta':'sum'
                            ,'w_hm':'sum'
                            }).reset_index()
    # rename 'weight' to n
    ac_data.rename(columns={'weight':'n'}, inplace=True)
    # calculate Year over Year change by Age
    ac_data['ac'] = ac_data.w_hmXdelta/ac_data.w_hm
    return ac_data[['age','n','ac']]

def zscore_method(playerid, age, stat, weight = None):
    '''
    https://www.reddit.com/r/fantasybaseball/comments/a7iwvo/some_aging_curves/
    '''
    pass

# https://stackoverflow.com/questions/61177678/plotting-with-plotnine-and-trying-to-use-fill-transparent
def plot_ac(age, n, agecurve
            ,statname = ''
            ,minimize_age = True, min_age = 0, max_age=100
            ,stat_type = 'rate'
            ):
    '''
    Reproducible plot for Aging Curves.
    If want two different groups on the same graph, use plot_ac_group.
    Returns ggplot object.
    
    See delta_method for explanation of age, n, agecurve (ac in delta_method)
    
    statname is the Name of your statistic, i.e. AVG, OBP, SLG.
    
    'minimize_age = True' means find the minimum age, subtract 1.
        The graphs will use min(age)-1 to start.
        
    min_age = 0 and max_age = 100 are defult values used in filitering.
        Primairly utilized for ease of use in plotting rathering than calling
        df = df.loc(df.age > x) everytime want to filter the ages. 
    
    stat_type is the type of stat looking at.
        For example AVG, OBP would be 'rate'.
        For AB, velocity, wRC, would be 'counting'.
    '''
    df = pd.concat([age, n, agecurve], axis=1)
    cols = ['age','n','agecurve']
    df.columns = cols
    df = df.loc[(df.age >= min_age) & (df.age <= max_age)]
    if minimize_age is True:
        start_age = min(df.age) - 1
        start_row = pd.DataFrame([pd.Series([start_age,0,0])])
        start_row.columns = cols
        df = pd.concat([start_row, df], axis = 0).reset_index(drop=True)
    else:
        start_age = min(df.age)
        # index of value
        ind = df.index[df.age == start_age].tolist()[0]
        # set value in dataframe
        df.at[ind, 'agecurve'] = 0
        
    df = df.sort_values(by=['age'])
    # cumulative sum
    df['csum'] = df.agecurve.cumsum()
    # set up plot basics
    minage = min(df.age)
    maxage = max(df.age)
    yb_type_start = round(min(df.csum),2) - .015 if stat_type == 'rate' else myround(df.csum) - 5
    yb_type_end = round(max(df.csum),2) + .015 if stat_type == 'rate' else myround(df.csum) + 5
    yb_type_ = 0.01 if stat_type == 'rate' else 5
    # plot
    p = ggplot()+ \
        geom_line(df, aes(x='age',y='csum'))+ \
        geom_text(df, aes(x='age',y=df.csum-0.004,label = 'n'),color='dodgerblue')+ \
        scale_x_continuous(breaks=range(minage,maxage+1,2)
                            ,minor_breaks=range(minage,maxage+1))+ \
        scale_y_continuous(breaks=np.arange(yb_type_start,yb_type_end,yb_type_)
                            ,minor_breaks=np.arange(yb_type_start,yb_type_end,yb_type_))+ \
        labs(y=statname, x = 'Age')+ \
        theme_bw() + \
        theme(
            axis_title_x = element_text(size = 15, vjust=1,color='black'),
            axis_title_y = element_text(size = 15,vjust=1.75,color='black'),
            axis_text=element_text(color='black',size=10),
            plot_background = element_rect(),
            legend_position = None
            )
        
    return p
    

#    def plot_ac_group(age, n, ac, group, **kwargs):
#        # read additional optional arguments and set defults if nonexistent
#        statname = kwargs.get('statname', None)
#        df = pd.concat([group, age, n, ac], axis=1)
#        df = df.sort_values(by=['group','age'])
#          
#        ggplot()+
#          geom_line(data=df,aes(x=age,y=ac,group=group,color=group))+
#          scale_x_continuous(breaks=c(seq(21,40,1)),minor_breaks = c(seq(21,40,1)))+
#          scale_y_continuous(breaks=c(seq(-5,0.5,0.5)),minor_breaks=c(seq(-5,0.5,0.25)))+
#          labs(color="",y='Fastball (mph) Over Time (Cumulative)')+
#          theme_bw() +
#          theme(
#            axis.title.x = element_text(size = 16, vjust=0,color='black'),
#            axis.title.y = element_text(size = 16,vjust=1.75,color='black'),
#            axis.text=element_text(color='black',size=15),
#            plot.background = element_rect(fill = "transparent", colour = NA),
#            legend.position = 'bottom',
#            #legend.title = element_text(size=14,color='black'),
#            legend.text = element_text(size=14,color='black'),
#            legend.background = element_rect(fill = "transparent"),
#            #legend.box.background = element_rect(fill = "transparent")
#          )
        
        
        

