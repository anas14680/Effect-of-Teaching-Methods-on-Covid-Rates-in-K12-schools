# %%
from linearmodels import PanelOLS
import pandas as pd
import numpy as np

import warnings

warnings.simplefilter("ignore")

# %%
# We load school data for all four terms

Fall_2020_2021 = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/covid-data Fall 2020- 2021.xlsx"
)
Spring_2020_2021 = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/covid-data spring 2020-2021.xlsx"
)
Fall_2021_2022 = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/covid-data Fall 2021 - 2022.xlsx"
)
Spring_2021_2022 = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/covid-data Spring 2021 - 2022.xlsx"
)


# %%
# read in the county to city mapping file
# we use this file to map counties onto city
city_county = pd.read_excel(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/City to county mapping.xlsx"
)

# select only relevant columns from mapping files
city_county = city_county[["city", "county_fips"]].copy()

# %%
# rename physical columns for ease of analysis
Fall_2020_2021.rename(columns={"PhysicalCity": "city"}, inplace=True)
Spring_2020_2021.rename(columns={"PhysicalCity": "city"}, inplace=True)
Fall_2021_2022.rename(columns={"PhysicalCity": "city"}, inplace=True)
Spring_2021_2022.rename(columns={"PhysicalCity": "city"}, inplace=True)
Fall_2021_2022.rename(columns={"Term ": "Term"}, inplace=True)


# %%
# merge counties and fips codes onto the normal data
Fall_2020_2021 = pd.merge(Fall_2020_2021, city_county, on="city", how="left")
Spring_2020_2021 = pd.merge(Spring_2020_2021, city_county, on="city", how="left")
Fall_2021_2022 = pd.merge(Fall_2021_2022, city_county, on="city", how="left")
Spring_2021_2022 = pd.merge(Spring_2021_2022, city_county, on="city", how="left")


# %%
# drop unmatched couties
datasets = [Fall_2020_2021, Fall_2021_2022, Spring_2020_2021, Spring_2021_2022]
for i in datasets:
    i.dropna(subset=["county_fips"], inplace=True)
    i["county_fips"] = i["county_fips"].astype("int")


# %%
# select only relevant columns from the school data
Fall_2020_2021 = Fall_2020_2021[
    [
        "Term",
        "DistrictID",
        "SchoolYear",
        "county_fips",
        "Enrollment",
        "TeachingMethod",
        "StudentMaskPolicy",
    ]
]
Fall_2021_2022 = Fall_2021_2022[
    [
        "Term",
        "DistrictID",
        "SchoolYear",
        "county_fips",
        "Enrollment",
        "TeachingMethod",
        "StudentMaskPolicy",
    ]
]
Spring_2020_2021 = Spring_2020_2021[
    [
        "Term",
        "DistrictID",
        "SchoolYear",
        "county_fips",
        "Enrollment",
        "TeachingMethod",
        "StudentMaskPolicy",
    ]
]
Spring_2021_2022 = Spring_2021_2022[
    [
        "Term",
        "DistrictID",
        "SchoolYear",
        "county_fips",
        "Enrollment",
        "TeachingMethod",
        "StudentMaskPolicy",
    ]
]


# %%
# Now we combine all the school data
complete_schools_data = pd.concat(
    [Fall_2020_2021, Fall_2021_2022, Spring_2020_2021, Spring_2021_2022]
)
# impute missing values for enrollments by mean of county enrollments
complete_schools_data["avg_enr"] = complete_schools_data.groupby("county_fips")[
    "Enrollment"
].transform(lambda x: x.mean())

complete_schools_data["Enrollment"] = np.where(
    complete_schools_data["Enrollment"].isna(),
    complete_schools_data["avg_enr"],
    complete_schools_data["Enrollment"],
)


# %%
complete_schools_data.to_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/complete_school_data.csv"
)


# %%
# alot of information on teaching method is missing and
# unknown information. # Therefore, we choose only counties
# for which we have more than 80% data
complete_schools_data["useit"] = np.where(
    complete_schools_data["TeachingMethod"].isin(["Unknown", "Other", "Pending"]), 0, 1
)


complete_schools_data["useit_ind"] = complete_schools_data.groupby("county_fips")[
    "useit"
].transform("mean")

complete_schools_data2 = complete_schools_data[
    complete_schools_data["useit_ind"] >= 0.80
]

counties_to_use = list(np.unique(complete_schools_data2["county_fips"]))
# in the end we are left with 545 counties


# %%
useable_counties_school_data = complete_schools_data.loc[
    complete_schools_data["county_fips"].isin(counties_to_use)
]


# %%
useable_counties_school_data.to_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/useable_counties_school_data.csv"
)
