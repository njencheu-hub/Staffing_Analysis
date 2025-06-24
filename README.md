# PBJ Daily Nurse Staffing Analysis (Q2 2024)

This Python project analyzes CMS's Payroll-Based Journal (PBJ) daily staffing data for nursing homes in the U.S., focusing on contractor utilization patterns.

---

## Table of Contents

- [Objective](#objective)
- [Real-World Use Cases](#real-world-use-cases)
- [Dataset](#dataset)
- [Features](#features)
  - [1. Data Cleaning & Preparation](#1-data-cleaning--preparation)
  - [2. Metric Engineering](#2-metric-engineering)
  - [3. Aggregated Insights](#3-aggregated-insights)
  - [4. Visualization](#4-visualization)
- [Insights](#insights)
- [Tools Used](#tools-used)
- [Outputs](#outputs)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

---

## Objective
To identify nursing homes and states with high reliance on contract-based staffing, enabling strategic outreach opportunities for platforms like Clipboard Health.

---

## Real-World Use Cases

- **Vendor Targeting**: Identify facilities that rely heavily on contractors for strategic outreach.
- **Operational Planning**: Detect understaffed or over-reliant regions for proactive engagement.
- **Healthcare Policy**: Inform regulatory analysis or incentives related to contract staffing patterns.
- **Sales Enablement**: Equip staffing platforms with data-driven entry points for customer acquisition.

---

## Dataset
- **Source**: CMS.gov PBJ Daily Nurse Staffing, Q2 2024  
- **Columns Include**:
  - Facility identifiers (e.g., PROVNUM, facility name)
  - Daily census and work dates
  - RN, LPN, and CNA hours split by employee and contractor
  - Total hours worked

---

## Features

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
- Python: `pandas`, `matplotlib` for EDA and visualization
- Data from CMS.gov PBJ Staffing Report

## Outputs
- Visualizations saved to `.png` for executive reporting
- Ranked tables of high-opportunity facilities and states

---

## Installation

To install the required Python packages:

pip install -r requirements.txt

## Usage

To run the analysis:

python staffing_Clipboard-Health.py

## Contributing
We welcome community contributions!

- Fork the repository

- Create a new branch:

git checkout -b feature/your-feature

- Make your changes

- Push to your branch:

git push origin feature/your-feature

- Submit a Pull Request

## License
This project is licensed under the MIT License.