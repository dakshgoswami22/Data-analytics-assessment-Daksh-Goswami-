# Data Analyst Assessment Submission Pack

## Dataset
- Primary source: NYC Taxi & Limousine Commission (TLC) Trip Record Data
- Primary URL: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Reproducible 200,000-row sample URL: https://datatweets.com/datasets/nyc-taxi/yellow_tripdata_sample.csv
- Sample shape: 200,000 rows × 10 columns
- The assessment source document asks for Q1–Q10 worksheets, processing, insights, dashboard and management presentation.

## Key verified sample metrics
- Trips: 200,000
- Total revenue: $5,343,779.62
- Average trip value: $26.72
- Average trip distance: 3.582 miles
- High-fare trips (> $50): 12,675 (6.3%)
- Credit-card trips: 156,378 (78.2%)
- Cash trips: 29,522 (14.8%)
- Missing passenger_count: 9,511

## Important submission note
The workbook intentionally does **not** fabricate 200,000 raw records. The `Data` worksheet contains a schema preview and explains how to populate it. The Python script downloads the exact sample and produces `processed_data.csv` plus dashboard-ready summary files.

Before final submission:
1. Run `process_taxi_assessment.py` with internet access.
2. Open the generated `processed_data.csv`.
3. Upload/copy the required analysis-ready data to Google Sheets.
4. Build the Looker Studio dashboard from the summary/processed outputs.
5. Add the final dashboard screenshots/link to Q8.
6. Replace any sample-based wording with full-file results if you choose to analyze a complete TLC month instead.

## Files
- Data_Analyst_Assessment_Submission.xlsx — Q1, Q2, Q3, Processed Data, Q4, Q5, Q6, Q7, Q8 and Q10
- process_taxi_assessment.py — reproducible Python/Pandas processing pipeline
- Management_Presentation.pptx — management deck
- dashboard_payment_mix.png — dashboard visual starter
