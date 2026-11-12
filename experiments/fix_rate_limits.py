import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; FILE=ROOT/"results"/"results.csv"; BACKUP=ROOT/"results"/"results_backup.csv"
if not BACKUP.exists(): BACKUP.write_bytes(FILE.read_bytes())
with open(FILE,"r",newline="",encoding="utf-8") as f:
    reader=csv.DictReader(f); rows=list(reader); headers=reader.fieldnames
corrected=0
for row in rows:
    if row["source"]=="real" and row["scenario"]=="manual" and row["status"]=="error":
        row["status"]="rate_limited"; corrected+=1
with open(FILE,"w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=headers); writer.writeheader(); writer.writerows(rows)
print("Corrected rate-limit records:",corrected); print("Backup:",BACKUP); print("Updated:",FILE)
