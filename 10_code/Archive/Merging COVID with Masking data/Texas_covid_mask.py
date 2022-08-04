# %%
import pandas as pd

# %%
# Load Texas data
texas_covid = pd.read_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/CSDH_TX_COVID_Schools (2).csv"
)
texas_mask = pd.read_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/Texas_MaskingData (2).csv"
)


# %%
# impute NAs in covid cases
texas_covid["NewCasesStudents"] = texas_covid["NewCasesStudents"].fillna(0)


# %%
# filter out the needed columns
texas_relevant = texas_covid.loc[
    :,
    [
        "StateName",
        "StateAbbrev",
        "NCESDistrictID",
        "DistrictName",
        "TimePeriodInterval",
        "TimePeriodStart",
        "TimePeriodEnd",
        "NewCasesStudents",
    ],
].copy()


# %%
# convert time period to datetime
texas_relevant["TimePeriodStart"] = pd.to_datetime(
    texas_relevant["TimePeriodStart"]
).copy()
texas_relevant["TimePeriodEnd"] = pd.to_datetime(texas_relevant["TimePeriodEnd"]).copy()

# %%
# group data by district, take the sum of covid cases
# min of minimum date and max of maximum date
texas_covid_data_new = texas_relevant.groupby("NCESDistrictID").agg(
    {"NewCasesStudents": "sum", "TimePeriodStart": "min", "TimePeriodEnd": "max"}
)


# %%
# Add state indicators back
texas_covid_data_new["StateName"] = "Texas"
texas_covid_data_new["StateAbbrev"] = "TX"

# %%
# remove columns from masking data where there is no masking policy available
texas_mask_new = texas_mask.loc[~(texas_mask["StudentMaskPolicy"].isna())]


# %%
# Filter out relevant columns from masking data
texas_mask_new = texas_mask_new[
    ["NCESDistrictID", "EnrollmentTotal", "StudentMaskPolicy"]
]


# %%
# merge the covid data and masking data
final_texas_data = pd.merge(
    texas_covid_data_new, texas_mask_new, on="NCESDistrictID", how="inner"
)


# %%
## Rename NewCasesStudent to Covid Cases
final_texas_data = final_texas_data.rename(columns={"NewCasesStudents": "Covid Cases"})

# %%
final_texas_data.to_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/Texas_Covid_Mask.csv"
)
