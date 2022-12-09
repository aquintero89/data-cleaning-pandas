from dateutil.parser import parse
import numpy as np


"""It eliminates the spaces. The keyword determines if you want to eliminate all sapces or not.
If you put all, it eliminates all spaces. If you don't put all, it eliminates the spaces from the begining
and end"""
def no_spaces(data,column,key_word):
    if key_word=="all":
        data.loc[:,column]=data[column].str.replace(" ","")
    else:
        data.loc[:,column]=data[column].str.strip()


"""It elimnates words from that specific value in a column"""
def eliminate_words(data,column,word_list):
	for word in word_list:
		data.loc[:,column]=data[column].str.replace(word,"")

"""It checks if it could be transformed into a date or not"""
def check_date(data,fuzzy=False):
    new_list=[]
    for i in list(data.Date.values):
        try: 
            parse(str(i), fuzzy=fuzzy)
            None
        except ValueError:
            if i.count("-")==2:
                new_list.append(i)
    return new_list


"""It takes the rows where a column is null and the other not"""

def check_nulls(data,column1,column2):
    return data[(data[column1].isnull())&(data[column2].isnull()==False)&(data[column2]!="0")]

"""It formats the month in order that is understandable. You have to put the list of values you want to
change."""
def change_month(data,list_values):
    list_to_change=list_values
    coinc={"A":"Aug","Ma":"Mar","S":"Sep","Dc":"Dec","Oc":"Oct","Nv":"Nov","Ma":"Mar","Fb":"Feb"
      ,"J":"Jan","M":"Mar","F":"Feb","D":"Dec","N":"Nov","O":"Oct","Jul":"Jul","July":"Jul","Ap":"Apr"}
    for label, value in dict(data.Date).items():
        for to_change in list_to_change:
            if value==to_change:
                part_to_change=value.split("-")[1]
                data.loc[label,"Date"]=value.replace(part_to_change,coinc[part_to_change])

"""Function to group by the categories so it is easier to analyze it"""

def activity_class(data):
    
    conditions = [
    data['Activity'].str.lower().str.contains("boogi",na=False),
    data['Activity'].str.lower().str.contains("tread",na=False),
    data['Activity'].str.lower().str.contains("floa",na=False),
    data['Activity'].str.lower().str.contains("padd",na=False),
    data['Activity'].str.lower().str.contains('fell',na=False),
    data['Activity'].str.lower().str.contains('kaya',na=False),
    data['Activity'].str.lower().str.contains("snork",na=False),
    data['Activity'].str.lower().str.contains("divin",na=False),
    data['Activity'].str.lower().str.contains("bathin",na=False),
    data['Activity'].str.lower().str.contains('standi',na=False),
    data['Activity'].str.lower().str.contains('body',na=False),
    data['Activity'].str.lower().str.contains('fishi',na=False),
    data['Activity'].str.lower().str.contains('surf',na=False),
    data['Activity'].str.lower().str.contains('swim',na=False),
    data['Activity'].str.lower().str.contains('wading',na=False),
    data['Activity'].str.lower().str.contains('canoe',na=False),
    data['Activity'].str.lower().str.contains('sail',na=False),
    data['Activity'].str.lower().str.contains('rowi',na=False),
    data['Activity'].str.lower().str.contains('play',na=False),
    data['Activity'].str.lower().str.contains('track',na=False),
    data['Activity'].str.lower().str.contains('disaster',na=False),
    data['Activity'].str.lower().str.contains('clammi',na=False),
    data['Activity'].str.lower().str.contains('boati',na=False),
    data['Activity'].str.lower().str.contains('feed',na=False),
    data['Activity'].str.lower().str.contains('walki',na=False),
    data['Activity'].str.lower().str.contains('tagg',na=False),
    data['Activity'].str.lower().str.contains('kite',na=False),
    data['Activity'].str.lower().str.contains('rescu',na=False),
    data['Activity'].str.lower().str.contains('teasin',na=False),
    data['Activity'].str.lower().str.contains('skii',na=False)]


    values = ["Boogie boarding", "Treading water", "Floating", "Paddle boarding", "Fell off",
          "Kayaking", "Snorkling", "Diving", "Bathing", "Standing", "Body boarding_surfing", "Fishing", "Surfing",
          "Swimming", "Wading", "Canoeing", "Sailing", "Rowling", "Playing", "Tracking", "Plane or Sea Disaster",
          "Clamming", "Boating", "Feeading wild animals", "Walking", "Tagging", "KiteSurfing", "Rescuing", "Teasing",
          "Jet Skii"]
    
    data["Activity"] = np.select(conditions, values, default='Not defined precisely')


"""To clean the column Age based on some patterns"""
def age_cleaning(data):
    no_spaces(data,"Age","all")
    for x,v in dict(data.Age).items():
        if "teen" in str(v).lower():
            data.loc[x,"Age"]=16 #mean between 13-19
        elif str(v)==" " or str(v)=="  " or str(v)=="" or  str(v).strip()=="":
            data.loc[x,"Age"]=""
        elif str(v).strip()!=str(v):
            data.loc[x,"Age"]=int(str(v).strip())
        elif "'" in str(v):
            data.loc[x,"Age"]=int((str(v)[:str(v).find("'")]))
        elif  "," in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[:str(v).find(",")]))
        elif "young" in str(v).lower():
            data.loc[x,"Age"]=17 #mean between 10-24
        elif "s" in str(v).lower() and (len(str(v))==3 or len(str(v))==2):
            data.loc[x,"Age"]=int(str(v)[:len(str(v))-1])
        elif "minor" in str(v).lower(): #equivalent to minor
            data.loc[x,"Age"]=8 #the mean between 0-17
        elif "or" in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[:str(v).find("o")]))
        elif "½" in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[:str(v).find("½")]))
        elif "to" in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[:str(v).find("t")]))
        elif "&" in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[:str(v).find("&")]))
        elif "?" in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[:str(v).find("?")]))
        elif "Both 11" in str(v).lower():
            data.loc[x,"Age"]=int((str(v)[(str(v).find(" ")+1):]))
        elif "mid-" in str(v).lower():
            data.loc[x,"Age"]=(int((str(v)[4:6]))+(int((str(v)[4:6]))+10))/2
        elif 'Both 11' in str(v):
            data.loc[x,"Age"]=11
        elif "18 months" in str(v):
            data.loc[x,"Age"]=1
        elif "9 months" in str(v):
            data.loc[x,"Age"]=0
    transform_int(data,"Age")
    data["Age"]=data["Age"].apply(lambda x: float(x) if type(x)==str else x)

"""It transforms into integers if isnumeric is true"""
def transform_int(data,column):
     for i,n in dict(data[column]).items():
            if str(n).isnumeric()==True and type(n)==str:
                data.loc[i,column]=int(n)
            elif type(n)==str:
                data.loc[i,column]=None


"""In order to transform some invalid registers of some rows of Area"""
def fill_area_correctly(data):
    for label,area in dict(data.Area).items():
        if "300 miles from Antigua" in str(area):
            data.loc[label,"Area"]= "Antigua"
        elif "40 miles off Grand Bahama Island" in str(area):
            data.loc[label,"Area"] = "Bahama"
        elif "740 miles SE of Tarawa Atoll" in str(area):
            data.loc[label,"Area"] = "Tarawa Atoll"

"""We correct some invlaid registers of some rows of Sex"""
def assign_sex(data):
    for label, sex in dict(data['Sex']).items():
        if "." in str(sex):
            data.loc[label,"Sex"]= "Not valid sex"
        elif "N" in str(sex):
            data.loc[label,"Sex"]= "Not valid sex"
        elif "lli" in str(sex):
            data.loc[label,"Sex"]= "Not valid sex"

"""We correct some invalid registers of some rows of Fatal_(Y/N)"""

def assign_fatal(data):
    for label, fatal in dict(data["Fatal_(Y/N)"]).items():
        if "UNKNOWN" in str(fatal):
            data.loc[label,"Fatal_(Y/N)"]= "Not valid register"
        elif "2017" in str(fatal):
            data.loc[label,"Fatal_(Y/N)"]= "Not valid register"
        elif "M" in str(fatal):
            data.loc[label,"Fatal_(Y/N)"]= "Not valid register"

"""This function is to be able to the group by taking into account two columns"""

def group_column(data,column1,column2,method):
    merged_data_grouped=data.groupby(by=column1)
    merged_data_pt=merged_data_grouped.agg({column2:method})
    merged_data_pt.rename(columns={column2:"N_attacks_per_year"},inplace=True)
    return merged_data_pt

"""This fucntion is to be able to study the correlation between state and gdp per capita of that state. """

def corr_per_area(column):
    merged_data_grouped=merged_data_analysis[merged_data_analysis["Area"].isin([column])].groupby(by=["Area","Year"])
    merged_data_grouped=merged_data_grouped.agg({"Country":"count"})
    merged_data_grouped.rename(columns={"Country":"N_attacks_per_year"},inplace=True)
    attacks_gdp=merged_data_grouped.reset_index().set_index("Year").join(pd.DataFrame(usa_gdp_per_state.loc[column]),how="inner")
    attacks_gdp.rename(columns={column:"gdp_per_capita"},inplace=True)
    return attacks_gdp["N_attacks_per_year"].corr(attacks_gdp["gdp_per_capita"])