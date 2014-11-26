#!/bin/bash
python parse_dataset.py
cd stanford-postagger-2014-10-26
python annotate.py
cd ..
python pos_tagger_file.py ./data