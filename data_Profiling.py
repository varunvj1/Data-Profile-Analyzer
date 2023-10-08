import pandas as pd
#import numpy as nm
#import os
#import sys
from bs4 import BeautifulSoup
from ydata_profiling import ProfileReport

df = pd.read_csv(r"C:\Users\Varun\Desktop\SparkCourse\ml-latest-small\ratings.csv")

profile = ProfileReport(df, title="Profiling Report", minimal=True)
profile.to_file("report.html")


#### Generate CSV ###
path = "report.html"

# empty list
data = []

# Declare soup
soup = BeautifulSoup(open(path), "html.parser")

# for getting the data
HTML_data = soup.find_all("table", class_="table table-condensed stats")[0].find_all("tr")

for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)

# Add 2 empty lines at the end for division
data.extend(["\n", "\n"])

# Storing the data into Pandas DataFrame
df_basic_stats = pd.DataFrame(data=data)


### Attribute(s) Analysis ###
headers = []
attr_data = []

head1 = [
    "Attribute Name",
    "Uniqueness Analysis",
    "Uniqueness Analysis",
    "Completeness Analysis",
    "Values Distribution Analysis",
]

head2 = ["", "Unique %", "Null", "Null %", "Distinct Values"]
headers.append(head1)
headers.append(head2)

# for getting the data
attr_data_items = soup.find_all("div", class_="section-items")[1]
attr_data_child = attr_data_items.find_all("div", class_="row spacing")

for element in attr_data_child:
    try:
        elem_variable = element.find("div", class_="variable")
        elem_attr_name = elem_variable.find("a")
    except:
        continue

    try:
        elem_attr_stats_tbl = elem_variable.find(
            "table", class_="table table-condensed stats"
        )
    except:
        continue

    data_stats = []
    req_data = ["Distinct (%)", "Missing", "Missing (%)", "Distinct"]

    for req_data_elem in req_data:
        if elem_attr_stats_tbl.find(string=req_data_elem) == None:
            continue
        else:
            tbl_rows = elem_attr_stats_tbl.find_all("tr")
            for tbl_row in tbl_rows:
                tbl_ctgry = tbl_row.find("th")
                if tbl_ctgry.string == req_data_elem:
                    tbl_val = tbl_row.find("td")
                    data_stats.append(tbl_val.get_text())

    data_stats.insert(0, elem_attr_name.get_text())
    attr_data.append(data_stats)


# Add 2 empty lines at the end for division
attr_data.extend(["\n", "\n"])

print(attr_data)

# Storing the data into Pandas DataFrame
df_headers = pd.DataFrame(data=headers)
df_attr = pd.DataFrame(data=attr_data)

# Append all the data frames to generate the final report
df_headers = pd.concat([df_basic_stats, df_headers, df_attr])

# Converting Pandas DataFrame into CSV file
df_headers.to_csv("data_profing_report.csv")


### LOVs (New CSV)
df_lov = pd.DataFrame()
df_lov = df_lov._append(df.groupby("rating").agg(Count_of_LOV=pd.NamedAgg(column="rating", aggfunc="count")).reset_index())

df_lov.to_csv("lov.csv")


