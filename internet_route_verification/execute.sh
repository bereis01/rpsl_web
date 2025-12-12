#!/bin/bash
set -eu

if [ $MODE == "LIVE" ]; then

    # Defines output path
    outdir="./data"
    if [ -d "$outdir" ]; then rm -Rf $outdir; fi
    mkdir -p "$outdir"

    # Downloads IRR data
    wget --quiet http://ftp.arin.net/pub/rr/arin.db.gz -O "$outdir/arin.db.gz"
    wget --quiet https://ftp.ripe.net/ripe/dbase/ripe.db.gz -O "$outdir/ripe.db.gz"
    wget --quiet http://ftp.afrinic.net/dbase/afrinic.db.gz -O "$outdir/afrinic.db.gz"
    wget --quiet ftp://ftp.radb.net/radb/dbase/radb.db.gz -O "$outdir/radb.db.gz"
    wget --quiet https://irr.lacnic.net/lacnic.db.gz -O "$outdir/lacnic.db.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.as-block.gz -O "$outdir/apnic.db.as-block.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.as-set.gz -O "$outdir/apnic.db.as-set.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.aut-num.gz -O "$outdir/apnic.db.aut-num.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.domain.gz -O "$outdir/apnic.db.domain.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.filter-set.gz -O "$outdir/apnic.db.filter-set.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.inet-rtr.gz -O "$outdir/apnic.db.inet-rtr.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.inet6num.gz -O "$outdir/apnic.db.inet6num.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.inetnum.gz -O "$outdir/apnic.db.inetnum.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.irt.gz -O "$outdir/apnic.db.irt.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.key-cert.gz -O "$outdir/apnic.db.key-cert.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.limerick.gz -O "$outdir/apnic.db.limerick.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.mntner.gz -O "$outdir/apnic.db.mntner.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.organisation.gz -O "$outdir/apnic.db.organisation.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.peering-set.gz -O "$outdir/apnic.db.peering-set.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.role.gz -O "$outdir/apnic.db.role.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.route-set.gz -O "$outdir/apnic.db.route-set.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.route.gz -O "$outdir/apnic.db.route.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.route6.gz -O "$outdir/apnic.db.route6.gz"
    wget --quiet http://ftp.apnic.net/apnic/whois/apnic.db.rtr-set.gz -O "$outdir/apnic.db.rtr-set.gz"
    wget --quiet https://ftp.apnic.net/apnic/dbase/data/krnic.db.gz -O "$outdir/krnic.db.gz"
    wget --quiet http://ftp.apnic.net/apnic/dbase/data/jpnic.db.gz -O "$outdir/jpnic.db.gz"
    wget --quiet http://ftp.apnic.net/apnic/dbase/data/twnic.db.gz -O "$outdir/twnic.db.gz"
    wget --quiet ftp://ftp.nic.ad.jp/jpirr/jpirr.db.gz -O "$outdir/jpirr.db.gz"
    wget --quiet ftp://irr-mirror.idnic.net/idnic.db.gz -O "$outdir/idnic.db.gz"
    wget --quiet ftp://ftp.bgp.net.br/tc.db.gz -O "$outdir/tc.db.gz"
    ls -al "$outdir"

    # Unzips all files
    for filename in $outdir/*; do gzip -d "${filename}"; done

    # Executes the parsing
    cd route_verification/
    rye sync
    . .venv/bin/activate
    time cargo r --release -- parse_ordered \
        ../$outdir/apnic.db.* \
        ../$outdir/*.db \
        $RAW_DATA_OUTPUT_PATH |& tee parse_out.txt
    deactivate
    cd ..

else

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

fi