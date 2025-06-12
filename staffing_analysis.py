# We want to help the sales team at Clipboard Health identify:
# High contractor use → Potential clients to win over from competitors.
# Low staffing without contractors → Homes that might need your help.
# Multi-state chains or underserved markets → Strategic opportunities.

# Step 1: Load and Clean the Data

import pandas as pd

# Load PBJ staffing data for Q2 2024

nurse_staffing = pd.read_csv(r'C:\Users\georg\OneDrive\Desktop\DEA\Projects\Staffing_Analysis\PBJ_Daily_Nurse_Staffing_Q2_2024.csv', encoding='ISO-8859-1',
    engine='python',
    on_bad_lines='skip')

# print(nurse_staffing.head())

#   PROVNUM                  PROVNAME          CITY STATE COUNTY_NAME  ...  Hrs_NAtrn_emp Hrs_NAtrn_ctr  Hrs_MedAide  Hrs_MedAide_emp  Hrs_MedAide_ctr
# 0   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL    Franklin  ...            0.0           0.0          0.0              0.0              0.0
# 1   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL    Franklin  ...            0.0           0.0          0.0              0.0              0.0
# 2   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL    Franklin  ...            0.0           0.0          0.0              0.0              0.0
# 3   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL    Franklin  ...            0.0           0.0          0.0              0.0              0.0
# 4   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL    Franklin  ...            0.0           0.0          0.0              0.0              0.0

# [5 rows x 33 columns]

# Preview the columns
# print(nurse_staffing.columns.tolist())

# ['PROVNUM', 'PROVNAME', 'CITY', 'STATE', 'COUNTY_NAME', 'COUNTY_FIPS', 'CY_Qtr', 
#  'WorkDate', 'MDScensus', 'Hrs_RNDON', 'Hrs_RNDON_emp', 'Hrs_RNDON_ctr', 'Hrs_RNadmin', 
#  'Hrs_RNadmin_emp', 'Hrs_RNadmin_ctr', 'Hrs_RN', 'Hrs_RN_emp', 'Hrs_RN_ctr', 'Hrs_LPNadmin', 
#  'Hrs_LPNadmin_emp', 'Hrs_LPNadmin_ctr', 'Hrs_LPN', 'Hrs_LPN_emp', 'Hrs_LPN_ctr', 'Hrs_CNA', 
#  'Hrs_CNA_emp', 'Hrs_CNA_ctr', 'Hrs_NAtrn', 'Hrs_NAtrn_emp', 'Hrs_NAtrn_ctr', 'Hrs_MedAide', 
#  'Hrs_MedAide_emp', 'Hrs_MedAide_ctr']

# Our Dataset Summary
# Each row seems to represent daily staffing data per facility (PROVNUM) with detailed hours broken down by:
# Job roles: RN, LPN, NA (Nursing Assistant), Med Aide
# Employment type: _emp (employee), _ctr (contractor)
# Additional info: state, county, facility name, etc.

# Convert key hour columns to numeric (in case of strings or missing data)
hour_cols = [col for col in nurse_staffing.columns if col.startswith("Hrs_")]
nurse_staffing[hour_cols] = nurse_staffing[hour_cols].apply(pd.to_numeric, errors='coerce')

# Step 2: Analyze Contractor Usage by State

import matplotlib.pyplot as plt

# Compute total contractor and employee hours
nurse_staffing['Total_Contractor_Hours'] = nurse_staffing[
    ['Hrs_RN_ctr', 'Hrs_LPN_ctr', 'Hrs_NAtrn_ctr', 'Hrs_MedAide_ctr']
].sum(axis=1)

nurse_staffing['Total_Employee_Hours'] = nurse_staffing[
    ['Hrs_RN_emp', 'Hrs_LPN_emp', 'Hrs_NAtrn_emp', 'Hrs_MedAide_emp']
].sum(axis=1)

# Group by state and compute contractor %
state_summary = nurse_staffing.groupby('STATE')[['Total_Contractor_Hours', 'Total_Employee_Hours']].sum()
state_summary['Contractor_%'] = (
    state_summary['Total_Contractor_Hours'] / 
    (state_summary['Total_Contractor_Hours'] + state_summary['Total_Employee_Hours']) * 100
)

# Sort by contractor percentage
state_summary_sorted = state_summary.sort_values('Contractor_%', ascending=False)

# # Print top 10 states
# print(state_summary_sorted.head(10))

# # Plot the top 10
# top10 = state_summary_sorted.head(10)

# plt.figure(figsize=(10, 6))
# top10['Contractor_%'].plot(kind='bar', color='darkcyan')
# plt.title('Top 10 States by Contractor Nurse Staffing (%) – Q2 2024')
# plt.ylabel('Contractor % of Total Hours')
# plt.xlabel('State')
# plt.xticks(rotation=0)
# plt.grid(axis='y', linestyle='--', alpha=0.6)
# plt.tight_layout()
# plt.savefig('Top_10_States_by_Contractor_nurse_staffing_Q2_2024')
# # plt.show()

#        Total_Contractor_Hours  Total_Employee_Hours  Contractor_%
# STATE
# VT                   89120.34             234311.51     27.554596
# DE                   98245.91             418253.79     19.021484
# NY                 1961562.63            9375905.63     17.301593
# ME                  120494.15             611359.83     16.464234
# PA                 1340281.60            6853835.98     16.356631
# MA                  538663.63            3203257.12     14.395378
# NH                  106665.05             655702.58     13.991288
# OR                  130216.30             852653.31     13.248583
# NJ                  619240.06            4116536.69     13.075787
# AK                   15640.06             110511.52     12.397831

# Interpretation we could include in our Memo:
# Vermont and Delaware lead the nation in contractor staffing proportions, 
# with Vermont exceeding 27% contractor hours. These high-usage states are strong candidates 
# for Clipboard Health to focus competitive sales efforts, as they demonstrate high demand for 
# temporary staffing support.


# Visualizing understaffed facilities helps spotlight homes that may benefit from Clipboard Health's 
# contractor services — especially those not yet using contractors.

# Plot Nursing Homes with Low Staffing and No Contractors
# We'll identify nursing homes that:
# Have low total nursing hours in the quarter (e.g., < 500 hours), and
# Use no contractor hours, suggesting potential staffing gaps.
# Then, we’ll create a bar chart of the 10 most understaffed facilities.

nurse_staffing['Total_Hours'] = nurse_staffing['Total_Contractor_Hours'] + nurse_staffing['Total_Employee_Hours']

# Aggregate total hours per facility across the quarter
facility_summary = nurse_staffing.groupby('PROVNUM').agg({
    'Total_Contractor_Hours': 'sum',
    'Total_Employee_Hours': 'sum',
    'Total_Hours': 'sum',
    'PROVNAME': 'first',
    'STATE': 'first',
    'CITY': 'first'
})

# Filter for low-staffed facilities that don't use contractors
understaffed = facility_summary[
    (facility_summary['Total_Hours'] < 500) &
    (facility_summary['Total_Contractor_Hours'] == 0)
]

# Sort and select bottom 10
understaffed_sorted = understaffed.sort_values('Total_Hours').head(10)

# Print bottom 10 facilities
print(understaffed_sorted.head(10))

# # Plot the results
# plt.figure(figsize=(12, 6))
# plt.bar(
#     understaffed_sorted['PROVNAME'] + ' (' + understaffed_sorted['STATE'] + ')',
#     understaffed_sorted['Total_Hours'],
#     color='crimson'
# )
# plt.ylabel('Total Staffing Hours (Quarter)') 
# plt.title('10 Most Understaffed Facilities Not Using Contractors - Q2 2024')
# plt.gca().invert_xaxis()  # Highest understaffed on the right 
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.grid(axis='y', linestyle='--', alpha=0.5)  # Changed axis to 'y'
# plt.savefig('10_most_understaffed_facilities_not_using_contractors_Q2-2024.png')
# # plt.show()

