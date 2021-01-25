#!/usr/bin/env bash

get_data='./get_data.py'
tosql='./csv2sql.py'

echo "Obtaining Data..."
if python3 $get_data; then
  echo "Making Insert Statements..."
  python3 $tosql
fi
echo "Done"