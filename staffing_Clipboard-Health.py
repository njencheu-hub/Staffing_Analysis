# STEP 1: Load, understand and Prepare the Dataset
import pandas as pd

# Load the dataset
df = pd.read_csv(r'C:\Users\georg\OneDrive\Desktop\DEA\Projects\Staffing_Analysis\PBJ_Daily_Nurse_Staffing_Q2_2024.csv'
                 , encoding="ISO-8859-1", dtype={'PROVNUM': str})

# print(df.head())

# # PROVNUM                  PROVNAME          CITY STATE  ... Hrs_NAtrn_ctr  Hrs_MedAide Hrs_MedAide_emp Hrs_MedAide_ctr
# # 0   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL  ...           0.0          0.0             0.0             0.0
# # 1   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL  ...           0.0          0.0             0.0             0.0
# # 2   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL  ...           0.0          0.0             0.0             0.0
# # 3   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL  ...           0.0          0.0             0.0             0.0
# # 4   15009  BURNS NURSING HOME, INC.  RUSSELLVILLE    AL  ...           0.0          0.0             0.0             0.0

# [5 rows x 33 columns]

# Preview the columns
# print(df.columns.tolist())

# ['PROVNUM', 'PROVNAME', 'CITY', 'STATE', 'COUNTY_NAME', 'COUNTY_FIPS', 'CY_Qtr', 
#  'WorkDate', 'MDScensus', 'Hrs_RNDON', 'Hrs_RNDON_emp', 'Hrs_RNDON_ctr', 'Hrs_RNadmin', 
#  'Hrs_RNadmin_emp', 'Hrs_RNadmin_ctr', 'Hrs_RN', 'Hrs_RN_emp', 'Hrs_RN_ctr', 'Hrs_LPNadmin', 
#  'Hrs_LPNadmin_emp', 'Hrs_LPNadmin_ctr', 'Hrs_LPN', 'Hrs_LPN_emp', 'Hrs_LPN_ctr', 'Hrs_CNA', 
#  'Hrs_CNA_emp', 'Hrs_CNA_ctr', 'Hrs_NAtrn', 'Hrs_NAtrn_emp', 'Hrs_NAtrn_ctr', 'Hrs_MedAide', 
#  'Hrs_MedAide_emp', 'Hrs_MedAide_ctr']

# Each row represents a single day of staffing for a nursing home, broken down by:

# Facility info: PROVNUM, PROVNAME, STATE, COUNTY_NAME
# Date: WorkDate
# Census (patients): MDScensus
# Staffing hours for roles like RN, LPN, CNA, etc.
# Each role has 3 versions:
# Total (Hrs_CNA)
# Employee only (Hrs_CNA_emp)
# Contractor only (Hrs_CNA_ctr)

# This structure lets us compare how much a facility depends on 
# full-time staff vs. contractors — exactly what Clipboard Health cares about!

# Convert WorkDate to datetime
df['WorkDate'] = pd.to_datetime(df['WorkDate'], errors='coerce')

# Fill missing values
df.fillna(0, inplace=True)

# STEP 2: Calculate Contractor Utilization

# We’ll create a metric like:
# Contractor % = Sum of contractor hours / Total hours

# Identify contractor and employee hour columns
contractor_cols = [col for col in df.columns if col.endswith('_ctr')]
employee_cols = [col for col in df.columns if col.endswith('_emp')]

# Sum across all roles per row
df['Total_Contractor_Hours'] = df[contractor_cols].sum(axis=1)
df['Total_Employee_Hours'] = df[employee_cols].sum(axis=1)
df['Total_Hours'] = df['Total_Contractor_Hours'] + df['Total_Employee_Hours']

# DtypeWarning: Columns (0) have mixed types. Specify dtype option on import or set low_memory=False.

# df = pd.read_csv(
#     r'C:\Users\georg\OneDrive\Desktop\DEA\Projects\Staffing_Analysis\PBJ_Daily_Nurse_Staffing_Q2_2024.csv',
#     encoding="ISO-8859-1",
#     dtype={'PROVNUM': str}
# )

# Group by Facility
facility_summary = df.groupby(['PROVNUM', 'PROVNAME', 'STATE']).agg({
    'Total_Contractor_Hours': 'sum',
    'Total_Employee_Hours': 'sum',
    'Total_Hours': 'sum',
    'MDScensus': 'mean'  # average daily patient count
}).reset_index()

# Calculate contractor % at facility level
facility_summary['Contractor_Pct'] = (
    facility_summary['Total_Contractor_Hours'] / facility_summary['Total_Hours']
) * 100

# Show top 10 facilities by contractor %
# print(facility_summary.sort_values(by='Contractor_Pct', ascending=False).head(10))

#       PROVNUM                                    PROVNAME STATE  ...  Total_Hours   MDScensus  Contractor_Pct
# 5551   225110  THE MASSACHUSETTS VETERANS HOME AT CHELSEA    MA  ...       771.75   97.560440           100.0
# 2236   105982                       SUN HARBOR HEALTHCARE    FL  ...     38941.48  113.340659           100.0
# 5577   225219                  BEAR MOUNTAIN AT WORCESTER    MA  ...        42.75  134.175824           100.0
# 5201   195580                AVOYELLES MANOR NURSING HOME    LA  ...       723.00   55.186813           100.0
# 7566   295048                       HARMON HOSPITAL - SNF    NV  ...      5069.39    6.054945           100.0
# 5217   195603        BAYOU VISTA NURSING AND REHAB CENTER    LA  ...      1860.00   50.109890           100.0
# 12172  475058                          MENIG NURSING HOME    VT  ...      3316.25   28.230769           100.0
# 2579   115551               CUMMING OPERATING COMPANY LLC    GA  ...     30050.06   84.087912           100.0
# 8359   335436        JAMAICA HOSPITAL NURSING HOME CO INC    NY  ...      7945.25  225.164835           100.0
# 7981   315471                       ST CATHERINE OF SIENA    NJ  ...       119.25   26.516484           100.0

# Show top 10 facilities by average daily patient count
# print(facility_summary.sort_values(by='MDScensus', ascending=False).head(10))

#       PROVNUM                                         PROVNAME STATE  ...  Total_Hours   MDScensus  Contractor_Pct
# 8377   335462               THE PLAZA REHAB AND NURSING CENTER    NY  ...    192010.58  732.263736       31.749464
# 8143   335100                    ISABELLA GERIATRIC CENTER INC    NY  ...    203758.15  683.175824       36.645665
# 8512   335644                    KINGS HARBOR MULTICARE CENTER    NY  ...    189766.48  630.318681        9.555181
# 8157   335136         LORETTO HEALTH AND REHABILITATION CENTER    NY  ...    182950.72  551.351648        0.228204
# 8528   335665        TERENCE CARDINAL COOKE HEALTH CARE CENTER    NY  ...    167659.88  523.186813        9.478535
# 10722  395465        CEDARBROOK SENIOR CARE AND REHABILITATION    PA  ...    182326.05  515.758242        0.000000
# 7822   315249                         LINCOLN PARK CARE CENTER    NJ  ...    146344.91  515.395604       10.318780
# 8208   335227                 WORKMENS CIRCLE MULTICARE CENTER    NY  ...    148948.94  510.373626       40.788233
# 8155   335132  PARKER JEWISH INSTITUTE FOR HEALTH CARE & REHAB    NY  ...    165069.57  489.505495       15.637346
# 8278   335334                                    THE RIVERSIDE    NY  ...    122792.03  488.527473        3.780995

# [10 rows x 8 columns]

# Aggregate by State

state_summary = facility_summary.groupby('STATE').agg({
    'Total_Contractor_Hours': 'sum',
    'Total_Employee_Hours': 'sum',
    'Total_Hours': 'sum',
    'Contractor_Pct': 'mean'
}).reset_index()

# Show top 10 states by contractor %
# print(state_summary.sort_values(by='Contractor_Pct', ascending=False).head(10))

#     STATE  Total_Contractor_Hours  Total_Employee_Hours  Total_Hours  Contractor_Pct
# 47    VT               251810.02             597772.81    849582.83       29.521747
# 21    ME               317900.53            1675925.43   1993825.96       15.835437
# 26    MT               154521.03             975227.47   1129748.50       15.584072
# 28    ND               219092.37            1533691.36   1752783.73       14.968923
# 31    NJ              1874722.27           11504891.82  13379614.09       13.233463
# 38    PA              3140207.69           18733297.21  21873504.90       12.826295
# 30    NH               305300.62            1679101.83   1984402.45       12.458975
# 0     AK                35651.02             312862.10    348513.12       11.925940
# 37    OR               328261.52            2580502.36   2908763.88       11.735778
# 29    NE               364662.63            3176275.34   3540937.97       11.586613

# Visualize the results
import matplotlib.pyplot as plt

# plt.figure(figsize=(12,6))
# top_states = state_summary.sort_values(by='Contractor_Pct', ascending=False).head(10)
# plt.bar(top_states['STATE'], top_states['Contractor_Pct'])
# plt.title('Top 10 States by Contractor Utilization (%)')
# plt.ylabel('Contractor %')
# plt.xlabel('State')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('Top_10_states_by_contractor_utilization_pct.png')
# plt.show()

# Sort facility_summary by MDScensus (descending) and Contractor_Pct (also descending)
sorted_facilities = facility_summary.sort_values(
    by=['MDScensus', 'Contractor_Pct'],
    ascending=[False, False]  # Both in descending order
)

# Display top 10 facilities
# print(sorted_facilities.head(10))

# plt.figure(figsize=(12,6))
# sorted_facilities = facility_summary.sort_values(
#     by=['MDScensus', 'Contractor_Pct'],
#     ascending=[False, False]  # Both in descending order
# ).reset_index(drop=True)

# # Optionally slice top N
# top_n = 10
# fac_names = sorted_facilities['PROVNAME'].head(top_n)
# census = sorted_facilities['MDScensus'].head(top_n)
# contractor_pct = sorted_facilities['Contractor_Pct'].head(top_n)

# # Plot with contractor % labels
# plt.figure(figsize=(12, 6))
# bars = plt.bar(fac_names, census, color='skyblue', edgecolor='black')
# for i, pct in enumerate(contractor_pct):
#     plt.text(i, census.iloc[i] + 5, f'{pct:.1f}%', ha='center', fontsize=9)

# plt.xticks(rotation=45, ha='right')
# plt.title('Top 10 Facilities by Census (with Contractor %)')
# plt.ylabel('Avg Daily Census')
# plt.tight_layout()
# plt.savefig('Top_10_facilities_by_census_with_contractor_pct.png')
# plt.show()

# Histogram of Contractor % at Facility Level

# plt.figure(figsize=(10, 5))
# plt.hist(facility_summary['Contractor_Pct'], bins=30, color='skyblue', edgecolor='black')
# plt.title('Distribution of Contractor % Across Facilities')
# plt.xlabel('Contractor %')
# plt.ylabel('Number of Facilities')
# plt.savefig('Distribution_of_contractor_pct_across_facilities.png')
# plt.show()

# Build a Target List of High-Opportunity Facilities

# These may be facilities that:
# Use >30% contractors
# Have a high average patient census (e.g., >200)

# Target List of High-Opportunity Facilities

# Based on your data, a few standout facilities meet our “high-opportunity” criteria:
# High average daily census (proxy for size of operation)
# High contractor percentage (showing dependence on temp staffing)

# Here’s a shortlist of 3 high-opportunity targets:

# PROVNUM	Facility Name	State	Avg Census	Contractor %
# 335227	WORKMENS CIRCLE MULTICARE CENTER	NY	510	40.8% 
# 335100	ISABELLA GERIATRIC CENTER INC	NY	683	36.6% 
# 335462	THE PLAZA REHAB AND NURSING CENTER	NY	732	31.7% 

# These facilities combine large census with high contractor % 
# — prime candidates for Clipboard Health outreach.