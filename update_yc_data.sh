#!/bin/bash
cd "$(dirname "$0")"
python3 youtube_ingest.py
python3 create_knowledge_base.py
