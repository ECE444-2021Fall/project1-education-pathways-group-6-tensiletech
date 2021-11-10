from .db_models import Courses, add_to_table
from app import df
import pandas as pd
import numpy as np
import os

if os.path.exists("resources_db_done.log"):
    print("Resources to DB transition completed, if needed to redo the DB, please remove 'resources_db_done.log'" +
        "from the current folder and delete betterpaths.db(mostly)!\nThe next time the app is run, DB transition from resources will take place!")
else:
    df_cleaned = df.replace(np.nan,"",regex=True)

    def list_to_string(list_cols):
        return_str = ""
        for val in list_cols:
            return_str += (str(val) + " ")
        return return_str

    print("\n************** INITIALIZING DB WITH DF_PROCESSED.PICKLE *******************\n")
    print("\n****************************************************************************\n")

    for index, row in df_cleaned.iterrows():
        course = Courses(courseId=index, name=row["Name"], division=row["Division"], description=row["Course Description"], department=row["Department"], \
            prerequisites=list_to_string(row["Pre-requisites"]), course_level=row["Course Level"], utsc_breadth=row["UTSC Breadth"], apsc_electives=row["APSC Electives"], \
                campus=row["Campus"], terms_offered=list_to_string(row["Term"]), activity=list_to_string(row["Activity"]), last_updated=row["Last updated"], \
                    exclusion=list_to_string(row["Exclusion"]), utm_distribution=row["UTM Distribution"], corequisites=list_to_string(row["Corequisite"]), recommended_prep=list_to_string(row["Recommended Preparation"]), \
                        as_breadth=row["Arts and Science Breadth"], as_distribution=row["Arts and Science Distribution"], later_term_course_details=row["Later term course details"], \
                            course_hyperlink=row["Course"], fase_available=row["FASEAvailable"], maybe_restricted=row["MaybeRestricted"], major_outcomes=list_to_string(row["MajorsOutcomes"]), \
                                minor_outcomes=list_to_string(row["MinorsOutcomes"]), aip_rereqs=list_to_string(row["AIPreReqs"]))
        add_to_table(course)

    with open("resources_db_done.log", "w") as f:
        f.write("Courses DF to Course DB Table Complete! If you need to reinitialize the DB please delete this file!")

    print("\n****************************************************************************\n")
    print("\n****************************************************************************\n")


