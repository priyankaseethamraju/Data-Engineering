import pandas as pd





acs_df = pd.read_csv("acs2017_census_tract_data.csv")
covid_df = pd.read_csv("COVID_county_data.csv") 

#print(acs_df.head(10))




acs_df = acs_df.groupby('County' , as_index = False).agg({"IncomePerCap" : "mean"})




#acs_df[acs_df['County'] == 'Autauga County'].groupby('County').agg({"IncomePerCap" : "mean"}) 
print(acs_df.head(10))

