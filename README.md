# stained-glasser
Stained-Glasser creates a stained-glass-like image formed by triangles.

## Environment variables

The `.env` file should look like:

```buildoutcfg
APP_NAME=stained-glasser
LOGS_FOLDER_PATH=logs

OUTPUT_FOLDER_PATH=output

SG_WIDTH=1000
SG_HEIGHT=1000

PALETTE_SIZE=4
```

## Run

Run
```buildoutcfg
python3 stained-glasser.py
```
and check your `output` folder.