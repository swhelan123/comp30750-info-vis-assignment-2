# Lichess Insights Dashboard

Interactive dashboard built with Streamlit and Plotly for exploring patterns in ~20,000 chess games from the [Lichess Open Database](https://database.lichess.org/). Made for COMP30750 Information Visualisation (Assignment 2) at UCD.

## What it does

The dashboard has six main visualisations (plus a bonus radar chart), each looking at a different angle of the dataset. A **personal data overlay** lets you compare your own Chess.com games against the full database on every chart.

1. **Rating Gap vs. Game Length** — Scatter plot showing how the rating difference between players relates to how long the game lasts, coloured by outcome (mate, resign, timeout).
2. **White's First-Move Advantage** — Diverging bar chart breaking down white vs. black wins across four skill tiers (Novice, Intermediate, Advanced, Master).
3. **Opening Popularity vs. Win Rate** — Bubble chart comparing how popular each opening is against White's actual win rate with it.
4. **Opening Theory Depth** — Violin/box plots showing how many moves deep into known book lines each skill tier tends to go.
5. **Upset Frequency** — How often the lower-rated player wins, binned by rating gap.
6. **Time Control vs. Outcome** — Stacked bar or heatmap showing how game endings (mate, resign, timeout, draw) shift across bullet, blitz, rapid, and classical time controls.
7. **Bonus: Opening Profiles** — Radar chart for comparing openings across multiple dimensions (win rates, draw rate, popularity, decisiveness).
8. **Personal Performance Summary** — Rating progression over time, personal KPIs, and side-by-side comparison with database averages (visible when overlay is enabled).

## Personal Data Overlay

Toggle **"Overlay My Games"** in the sidebar to see your personal Chess.com data (username `shanew012`) on top of every chart:

- **Gold diamond markers (⭐)** appear on scatter plots, heatmaps, and line charts so your games stand out against the 20k-game database.
- **Dedicated "👤 My …" tabs** are added to Tasks 2, 3, and 5 with personal breakdowns (win rate by colour, opening win rates vs. DB averages, underdog/favourite win splits).
- **Insight boxes** are extended with your personal stats for quick comparison.
- A **Rating Progression** chart and **personal KPI cards** appear at the bottom when the overlay is on.

To use your own data, export your games as PGN from Chess.com, convert with `Personal data/pgn_to_csv.py`, and place the resulting CSV in `Personal data/`.

## Project Structure

```
comp30750_assignment_2/
├── app.py                  # main streamlit app
├── chess.csv               # raw dataset (~20k games from Lichess)
├── data_aggr.sql           # SQL queries used to produce the task CSVs
├── requirements.txt        # python dependencies
├── task1_scatter.csv        # rating diff, turns, victory status per game
├── task2_tiers.csv          # win counts by skill tier and colour
├── task3_openings.csv       # top openings with outcome counts
├── task4_ply_by_tier.csv    # opening ply values per game, grouped by tier
├── task5_upsets.csv         # rating gap + whether it was an upset
├── task6_time_victory.csv   # time control, victory status, game count
└── Personal data/
    ├── pgn_to_csv.py        # converts Chess.com PGN exports to the CSV schema
    ├── shanew012_games.pgn  # raw PGN export
    └── shanew012_games.csv  # converted personal games (~1,450 games)
```

## How to Run

Make sure you have Python 3.9+ installed.

```bash
# install dependencies
pip install -r requirements.txt

# run the dashboard
streamlit run app.py
```

The app should open in your browser at `http://localhost:8501`.

## Data

The raw data (`chess.csv`) comes from Lichess and contains ~20,000 games with columns like player ratings, opening names, time controls, move sequences, etc. The `data_aggr.sql` file has the SQL queries that were used to aggregate this into the smaller per-task CSV files that the dashboard reads in.

Personal game data (`Personal data/shanew012_games.csv`) contains ~1,450 games exported from Chess.com and converted to the same CSV schema using the `pgn_to_csv.py` script. The app processes this at load time to derive extra columns (your colour, your rating, upset flags, time-control categories, etc.) and overlays the results on the database-wide charts when the sidebar toggle is enabled.

## Dependencies

- **Streamlit** for the web app framework
- **Plotly** for all the interactive charts
- **Pandas** for data loading and manipulation
