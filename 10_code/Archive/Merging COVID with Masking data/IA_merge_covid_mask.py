# %%
# Importing libraries and initial configs
import pandas as pd
import os

os.chdir(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS_701_Unifying_Data_Science\\Final Project\\Gitdata\\uds-2022-team-9\\"
)


# %%
# Importing masking data of the shortlisted states
ia = pd.read_csv(
    "./00_source_data/Masking_Data_CSV/Masking Data CSV/Iowa_MaskingData.csv"
)

# %%
# Checking counts of our treatment variable of interest
ia["StudentMaskPolicy"].value_counts()


# %%
# Reading in COVID data for FL
ia_covid = pd.read_csv(
    "./00_source_data/CSDH_COVID-19_Data_CSV/CSDH COVID-19 Data CSV/CSDH_IA_COVID_Schools.csv"
)


# %%
# Dropping nulls in masking data
ia = ia.dropna(subset=["StudentMaskPolicy"])
cols_to_keep = [
    "StateName",
    "StateAbbrev",
    "NCESDistrictID",
    "EnrollmentTotal",
    "StudentMaskPolicy",
]
ia = ia[cols_to_keep]

# %%
# Aggregating from school to district level
ia_covid["ActiveCasesStudents"].fillna(0, inplace=True)
ia_covid_agg = ia_covid.groupby(["StateName", "NCESDistrictID"], as_index=False).agg(
    {"TimePeriodStart": "min", "TimePeriodEnd": "max", "ActiveCasesStudents": "sum"}
)

# %%
# Merging masking data to COVID
IA_covid_mask = ia_covid_agg.merge(ia, on=["StateName", "NCESDistrictID"], how="inner")
IA_covid_mask.head()


# %%
# Calculating COVID positivity rates
IA_covid_mask["PositivityRate"] = (
    IA_covid_mask["ActiveCasesStudents"] / IA_covid_mask["EnrollmentTotal"]
)

# Rearranging columns
IA_covid_mask = IA_covid_mask[
    [
        "StateName",
        "StateAbbrev",
        "NCESDistrictID",
        "TimePeriodStart",
        "TimePeriodEnd",
        "StudentMaskPolicy",
        "ActiveCasesStudents",
        "EnrollmentTotal",
        "PositivityRate",
    ]
]
IA_covid_mask["NCESDistrictID"] = IA_covid_mask["NCESDistrictID"].astype(int)

IA_covid_mask.to_csv(
    "./20_intermediate_files/Merging COVID with Masking data/IA_COVID_mask.csv",
    index=False,
)
