# %%
import numpy as np
import pandas as pd

# %%
# Read in covid data for counties
county_covid = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
)


# %%
# convert date to datetime format
county_covid["date"] = pd.to_datetime(county_covid["date"])


# %%
# Get New cases on each day.
# the cases currently available are cummulative cases
county_covid = county_covid.sort_values(by=["county", "date"])
county_covid["New_Cases"] = county_covid.groupby(["state", "county"])["cases"].diff()
county_covid.loc[county_covid["New_Cases"].isna(), "New_Cases"] = county_covid["cases"]

# %%
# We create terms in the data
# these terms are based on the following cut offs
# Fall - August to December (inclusive)
# Spring - January to May (inclusive)
# we have school data for 2 academic years
# hence we have four terms and we create data for
# all these terms here
county_covid["Term"] = "Find Out"

# academic years Fall 2020-2021
county_covid.loc[
    (county_covid["date"] >= pd.to_datetime("2020-08-01"))
    & (county_covid["date"] <= pd.to_datetime("2020-12-31")),
    "Term",
] = "Fall 2020-2021"

# academic years Spring 2020-2021
county_covid.loc[
    (county_covid["date"] >= pd.to_datetime("2021-01-01"))
    & (county_covid["date"] <= pd.to_datetime("2021-05-31")),
    "Term",
] = "Spring 2020-2021"

# academic years Fall 2021-2022
county_covid.loc[
    (county_covid["date"] >= pd.to_datetime("2021-08-01"))
    & (county_covid["date"] <= pd.to_datetime("2021-12-31")),
    "Term",
] = "Fall 2021-2022"


# academic years Spring 2021-2022
county_covid.loc[
    (county_covid["date"] >= pd.to_datetime("2022-01-01")),
    "Term",
] = "Spring 2021-2022"


# remove data for all other dates that we do not need
county_covid = county_covid.loc[county_covid["Term"] != "Find Out"].copy()


# %%
# Now we aggregate data by county and term
# This gives us our data in form of a Panel data.
county_covid_agg = county_covid.groupby(
    ["state", "county", "fips", "Term"], as_index=False
)["New_Cases"].sum()


# %%
# convert fips code to integer for better merge
county_covid_agg["fips"] = county_covid_agg["fips"].astype("int")


# %%
# Load the population data

county_pop = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/County Population Data.xlsx"
)


# %%
# filter out only FIPS and Population data
county_pop = county_pop[["FIPS", "TOT_POP"]].copy()

# %%
# Rename FIPS to make merge easier
county_pop.rename(columns={"FIPS": "fips"}, inplace=True)

# %%
# merge our county covid data with population data
county_covid_pop = pd.merge(
    county_covid_agg, county_pop, on="fips", how="left", indicator=True
)


# %%
# For some counties we had not information in one of the datasets
# these were US territories and excluded from the analysis
county_covid_pop = county_covid_pop.loc[county_covid_pop["_merge"] == "both"]

# %%
county_covid_pop.to_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/county_pop_covid_panel.csv"
)
