#!/bin/bash

# Gets the source data
cd scripts/
rye sync
. .venv/bin/activate
python3 -m scripts.download_src_data
deactivate
cd ..

# Executes the parsing
cd route_verification/
rye sync
. .venv/bin/activate
time cargo r --release -- parse_ordered \
    ../data/irrs/priority/apnic.db.* \
    ../data/irrs/priority/afrinic.db \
    ../data/irrs/priority/arin.db \
    ../data/irrs/priority/lacnic.db \
    ../data/irrs/priority/ripe.db \
    ../data/irrs/backup/idnic.db \
    ../data/irrs/backup/jpirr.db \
    ../data/irrs/backup/radb.db \
    ../data/irrs/backup/nttcom.db \
    ../data/irrs/backup/level3.db \
    ../data/irrs/backup/tc.db \
    ../data/irrs/backup/reach.db \
    ../data/irrs/backup/altdb.db \
    $RAW_DATA_OUTPUT_PATH |& tee parse_out.txt
deactivate
cd ..