# BOUNDARY — Cricket Intelligence Studio

Interactive T20 cricket analytics project using Python, Pandas and Streamlit.

## Run locally
1. Install Python 3.10+.
2. Extract the ZIP and open a terminal in this folder.
3. Create environment: `python -m venv .venv`
4. Activate on Windows: `.venv\\Scripts\\activate`
5. Install: `pip install -r requirements.txt`
6. Run: `streamlit run app.py`

## Data note
Included CSVs are synthetic demonstration data, not verified ICC T20 World Cup 2022 scorecards. They make the app runnable immediately. Replace them with verified scorecards before reporting real-world findings.

## Data pipeline
Place `match_summary.json`, `batting_summary.json`, and `bowling_summary.json` in `data/raw/`, then run `python src/preprocess.py`. Import the CSVs in `data/processed/` into Power BI.

## Features
Overview dashboard; country/role/player filters; batting and bowling leaderboards; player comparison; role-based Dream XI selector; CSV upload; CSV download; JSON-to-CSV preprocessing.
