# %%
# Importing libraries and initial configs
import pandas as pd
import os

os.chdir(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS_701_Unifying_Data_Science\\Final Project\\Gitdata\\uds-2022-team-9\\"
)


# %%
# Importing masking data of the shortlisted states
# ar = pd.read_csv(
#     "./00_source_data/Masking_Data_CSV/Masking Data CSV/Arkansas_MaskingData.csv"
# )
fl = pd.read_csv(
    "./00_source_data/Masking_Data_CSV/Masking Data CSV/Florida_MaskingData.csv"
)
# ia = pd.read_csv(
#     "./00_source_data/Masking_Data_CSV/Masking Data CSV/Iowa_MaskingData.csv"
# )
# ks = pd.read_csv(
#     "./00_source_data/Masking_Data_CSV/Masking Data CSV/Kansas_MaskingData.csv"
# )
# mt = pd.read_csv(
#     "./00_source_data/Masking_Data_CSV/Masking Data CSV/Montana_MaskingData.csv"
# )
# nh = pd.read_csv(
#     "./00_source_data/Masking_Data_CSV/Masking Data CSV/NewHampshire_MaskingData.csv"
# )
# tx = pd.read_csv(
#     "./00_source_data/Masking_Data_CSV/Masking Data CSV/Texas_MaskingData.csv"
# )

# %%
# Merging masking data of all states
# all_states = pd.concat([ar, fl, ia, ks, mt, nh, tx])
# all_states.info()

# %%
# Checking counts of our treatment variable of interest
# all_states["StudentMaskPolicy"].value_counts()

# %%
# pd.crosstab(all_states["StudentMaskPolicy"], all_states["StateName"])


# %%
# Reading in COVID data for FL
fl_covid = pd.read_csv(
    "./00_source_data/CSDH_COVID-19_Data_CSV/CSDH COVID-19 Data CSV/CSDH_FL_COVID_Schools.csv"
)


# %%
# Dropping nulls in masking data
fl = fl.dropna(subset=["StudentMaskPolicy"])
cols_to_keep = [
    "StateName",
    "StateAbbrev",
    "NCESDistrictID",
    "EnrollmentTotal",
    "StudentMaskPolicy",
]
fl = fl[cols_to_keep]

# %%
# Aggregating from school to district level
fl_covid["ActiveCasesStudents"].fillna(0, inplace=True)
fl_covid_agg = fl_covid.groupby(["StateName", "NCESDistrictID"], as_index=False).agg(
    {"TimePeriodStart": "min", "TimePeriodEnd": "max", "ActiveCasesStudents": "sum"}
)

# %%
# Merging masking data to COVID
FL_covid_mask = fl_covid_agg.merge(fl, on=["StateName", "NCESDistrictID"], how="inner")
FL_covid_mask.head()


# %%
# Calculating COVID positivity rates
FL_covid_mask["PositivityRate"] = (
    FL_covid_mask["ActiveCasesStudents"] / FL_covid_mask["EnrollmentTotal"]
)

# Rearranging columns
FL_covid_mask = FL_covid_mask[
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

FL_covid_mask.to_csv(
    "./20_intermediate_files/Merging COVID with Masking data/FL_COVID_mask.csv",
    index=False,
)
