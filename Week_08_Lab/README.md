Week 08 Lab — Intelligence Platform

Quick start

- Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- Populate the SQLite database and load sample CSVs:

```powershell
python main.py
```

Notes
- I fixed relative import issues in `app/data/datasets.py` and consolidated CSV loading into `app/data/tickets.py`.
- Sample CSVs are included in `DATA/` so `main.py` can load them.
