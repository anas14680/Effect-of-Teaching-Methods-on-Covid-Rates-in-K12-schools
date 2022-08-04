# %%
# Import New Hampshire Covid and Masking data
import pandas as pd

NH_covid = pd.read_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/CSDH_NH_COVID_Schools.csv"
)
NH_mask = pd.read_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/NewHampshire_MaskingData.csv"
)

# %%
# convert time columns to datetime
NH_covid["TimePeriodStart"] = pd.to_datetime(NH_covid["TimePeriodStart"]).copy()
NH_covid["TimePeriodEnd"] = pd.to_datetime(NH_covid["TimePeriodEnd"]).copy()


# %%
# Group by district , sum active cases
NH_covid_new = NH_covid.groupby("NCESDistrictID").agg(
    {"ActiveCasesCombined": "sum", "TimePeriodStart": "min", "TimePeriodEnd": "max"}
)


# %%
# add state columns Back
NH_covid_new["StateName"] = "New Hampshire"
NH_covid_new["StateAbbrev"] = "NH"

# %%
# Filter out columns where masking policy is indicated
NH_mask_new = NH_mask.loc[~(NH_mask["StudentMaskPolicy"].isna())]

# %%
# Filter out needed columns from masking data
NH_mask_new = NH_mask_new[
    ["NCESDistrictID", "EnrollmentTotal", "StudentMaskPolicy"]
].copy()

# %%
# merge Masking and covid data
final_NH_data = pd.merge(NH_mask_new, NH_covid_new, on="NCESDistrictID", how="inner")

# %%
# Rename column to covid cases to maintain consistency
final_NH_data = final_NH_data.rename(columns={"ActiveCasesCombined": "Covid Cases"})

# %%
final_NH_data.to_csv("/Users/mohammadanas/Desktop/Nicks Project/NH_Covid_Mask.csv")
