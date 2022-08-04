# %%
from linearmodels import PanelOLS
import pandas as pd
import numpy as np
import scipy.stats
from functools import reduce

import warnings

warnings.simplefilter("ignore")

# %%
useable_counties_school_data = pd.read_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/useable_counties_school_data.csv"
)

# %%
useable_counties_school_data = useable_counties_school_data.loc[
    ~(
        useable_counties_school_data["TeachingMethod"].isin(
            ["Unknown", "Other", "Pending"]
        )
    )
].copy()


# %%
# One major limitation of our model is that we have imbalanced
# treatment variable. The data for remote teaching is very less
# as compared to hybrid and online teaching. Therefore, to make
# results robust we create three variations of treatment variable
# than run three different models.
# the purpose of the model is the same but there is variation in
# the treatment variable


# create one variation of treatment
# 0- remote
# 1- hybrid
# 2- in person

useable_counties_school_data["Teaching_ind"] = 0

useable_counties_school_data.loc[
    useable_counties_school_data["TeachingMethod"].isin(["Hybrid", "Hybrid/Partial"]),
    "Teaching_ind",
] = 1

useable_counties_school_data.loc[
    useable_counties_school_data["TeachingMethod"].isin(
        ["Full In-Person", "On Premises"]
    ),
    "Teaching_ind",
] = 2


# %%
# second variation
# 0 - remote
# 1 _ all else
# sever imbalance

useable_counties_school_data["Teaching_ind2"] = 0

useable_counties_school_data.loc[
    useable_counties_school_data["TeachingMethod"].isin(
        ["Full In-Person", "On Premises", "Hybrid", "Hybrid/Partial"]
    ),
    "Teaching_ind2",
] = 1

# %%
# another variation
# exactly same as variation 1 but WILL
# slightly different when we aggregate

useable_counties_school_data["Teaching_ind3"] = 0
useable_counties_school_data.loc[
    useable_counties_school_data["TeachingMethod"].isin(["Hybrid", "Hybrid/Partial"]),
    "Teaching_ind3",
] = 1
useable_counties_school_data.loc[
    useable_counties_school_data["TeachingMethod"].isin(
        ["Full In-Person", "On Premises"]
    ),
    "Teaching_ind3",
] = 2


# %%
# Now we concate year and term columns to maintain
# consistence with other datasets
useable_counties_school_data["Term"] = (
    useable_counties_school_data["Term"]
    + " "
    + useable_counties_school_data["SchoolYear"]
)

# %%
# Select only the required columns
final_school_data = useable_counties_school_data[
    [
        "Term",
        "county_fips",
        "Enrollment",
        "Teaching_ind",
        "Teaching_ind2",
        "Teaching_ind3",
    ]
].copy()

# create a copy
final_school_data_1 = final_school_data.copy()

# Create two continuous variable by taking mean
# and aggregating on counties

# Last one is different it is not the mean
# but rather we choose counties teaching method
# based on mode of teaching method
# in that county


def w_avg(df, values, weights):
    """Take weighted average."""
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


# # creating new variation corr to teaching method against max enrollments
def common_teach(df, values, weights):
    """Take most common teaching method."""
    num_students = list(df.groupby(values)[weights].sum())
    teach_meth = list(df.groupby(values)[weights].sum().index)
    return teach_meth[np.argmax(num_students)]


# aggregating them with all three variables
final_school_data_var1 = final_school_data.groupby(
    ["Term", "county_fips"], as_index=False
).apply(w_avg, "Teaching_ind", "Enrollment")

final_school_data_var2 = final_school_data.groupby(
    ["Term", "county_fips"], as_index=False
).apply(w_avg, "Teaching_ind2", "Enrollment")

# create a variable indicating majority teaching method
final_school_data_var3 = final_school_data.groupby(
    ["Term", "county_fips"], as_index=False
).apply(common_teach, "Teaching_ind3", "Enrollment")


final_school_data_var1.rename(columns={None: "Teaching_ind_1"}, inplace=True)
final_school_data_var2.rename(columns={None: "Teaching_ind_2"}, inplace=True)
final_school_data_var3.rename(columns={None: "Teaching_ind_3"}, inplace=True)


# %%

# compile the list of dataframes you want to merge
data_frames = [final_school_data_var1, final_school_data_var2, final_school_data_var3]
# merging the three variations of datasets
final_school_data = reduce(
    lambda left, right: pd.merge(left, right, on=["Term", "county_fips"], how="inner"),
    data_frames,
)


# %%
# Load panel data
covid_data = pd.read_csv(
    "/Users/mohammadanas/Desktop/Nicks Project/New project/county_pop_covid_panel.csv"
)

# %%
# List all the data fips counties
counties_to_use = list(np.unique(useable_counties_school_data["county_fips"]))
# get only relevant counties from panel data
covid_data = covid_data.loc[covid_data["fips"].isin(counties_to_use)].copy()
# get covid rate
covid_data["Covid_Rate"] = covid_data["New_Cases"] / covid_data["TOT_POP"]
# filter out relevant columns
final_covid_data = covid_data[["Term", "fips", "Covid_Rate"]]


# %%
# rename to fips to merge
final_school_data.rename(columns={"county_fips": "fips"}, inplace=True)

# %%
# we finally merge school and covid data
master_data = pd.merge(
    final_covid_data, final_school_data, on=["Term", "fips"], how="left", indicator=True
)


# %%
# encode term to be processed by Panel OLS
master_data["Final_term"] = 1
master_data.loc[master_data["Term"] == "Spring 2020-2021", "Final_term"] = 2
master_data.loc[master_data["Term"] == "Fall 2021-2022", "Final_term"] = 3
master_data.loc[master_data["Term"] == "Spring 2021-2022", "Final_term"] = 4


# %%
# For variation 3 of treatment we do get dummies to treat variables as
# categorical
master_data["Teaching_ind_3"] = pd.Categorical(master_data["Teaching_ind_3"])
master_data = pd.get_dummies(master_data, columns=["Teaching_ind_3"])

# %%
# set indexes
master_data_v2 = master_data.set_index(["fips", "Final_term"])

# %%
# run regression on variation 1
lm1 = PanelOLS.from_formula(
    "Covid_Rate ~ Teaching_ind_1 + EntityEffects + TimeEffects", data=master_data_v2
)
lm1.fit(cov_type="clustered", cluster_entity=True)

# %%
# Panel OLS on panel data for variation 2
lm1 = PanelOLS.from_formula(
    "Covid_Rate ~ Teaching_ind_2 + EntityEffects + TimeEffects", data=master_data_v2
)
lm1.fit(cov_type="clustered", cluster_entity=True)

# %%
# OLS regression on variation 3
# baseline hybrid
lm1 = PanelOLS.from_formula(
    "Covid_Rate ~ 	Teaching_ind_3_0.0 + Teaching_ind_3_2.0 + EntityEffects + TimeEffects",
    data=master_data_v2,
)
lm1.fit(cov_type="clustered", cluster_entity=True)
