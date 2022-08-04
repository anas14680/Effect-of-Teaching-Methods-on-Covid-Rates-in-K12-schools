# import NY times data for covid cases for each county
import pandas as pd

covid_total = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv"
)

# filter the data for the seven states included in our analysis
covid_total = covid_total.loc[
    covid_total["state"].isin(
        ["Arkansas", "Texas", "New Hampshire", "Kansas", "Iowa", "Montana", "Florida"]
    )
]

# import the mapping data for all seven states
# Mapping from district to county
TX_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/Texas Mapping.xlsx"
)
NH_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/NH Mapping.xlsx"
)
MT_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/Montana Mapping.xlsx"
)
KS_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/Kansas Mapping.xlsx"
)
IA_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/IOWA MApping.xlsx"
)
FL_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/Florida mapping.xlsx"
)
AK_mapping = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/Mapping Data/Arkansas Mapping.xlsx"
)


# concat the mapping data
mapping = pd.concat(
    [TX_mapping, NH_mapping, MT_mapping, KS_mapping, IA_mapping, FL_mapping, AK_mapping]
)


# change county column to merge
def remove_county(x):
    x = x.split()
    return x[0]


# Remove the word "county" from the county name in the mapping data
# to make the merge easier
mapping["County Name*"] = mapping["County Name*"].apply(remove_county)


# rename the column
mapping = mapping.rename(columns={"County Name*": "county"}).copy()

# Do an outer merge so we can get rows from both datasets.
county_district_covid = pd.merge(
    covid_total, mapping, on="county", how="outer", indicator=True
)

# Filter out rows for which we have information in only one data
county_district_covid = county_district_covid.loc[
    county_district_covid["_merge"] == "both"
]

county_district_covid.to_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/county_cases_district_mapping.csv"
)
