# PBJ Daily Nurse Staffing Analysis (Q2 2024)

This Python project analyzes CMS's Payroll-Based Journal (PBJ) daily staffing data for nursing homes in the U.S., focusing on contractor utilization patterns.

## Objective
To identify nursing homes and states with high reliance on contract-based staffing, enabling strategic outreach opportunities for platforms like Clipboard Health.

## Dataset
- **Source**: CMS PBJ Q2 2024
- **Columns**: Facility info, daily census, RN/LPN/CNA hours by employee vs. contractor

## Key Steps

### 1. Data Cleaning & Preparation
- Converted `WorkDate` to datetime
- Handled missing values
- Standardized data types for analysis

### 2. Metric Engineering
- Calculated total contractor, employee, and overall hours
- Derived contractor utilization % at facility and state levels

### 3. Aggregated Insights
- Highlighted top states by average contractor % utilization
- Identified high-opportunity facilities (large census + >30% contractor use)

### 4. Visualization
- Bar charts for top contractor states
- Facility-level census plots with contractor overlays
- Distribution histogram of contractor utilization across facilities

## Insights
- Facilities like **Isabella Geriatric Center**, **Workmens Circle**, and **The Plaza Rehab** exhibit high census and contract reliance.
- States like **Vermont**, **Maine**, and **Montana** show the highest average contractor percentages.

## Tools Used
- Python (Pandas, Matplotlib)
- Data from CMS.gov PBJ Staffing Report

## Outputs
- Visualizations saved to `.png` for executive reporting
- Ranked tables of high-opportunity facilities and states

---