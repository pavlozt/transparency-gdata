#!/bin/bash

country_codes=("RU" "NL" "DE" "FI" "JP" "US" "UK" "IS" "IT" "IS" "FR" "BR" "AU")

for code in "${country_codes[@]}"; do
  echo "Processing country code: $code"
  docker compose run --rm parser  --loop --start 1640995200000 --end 1737676799999 --filename data-$code.xlsx --pause 10 --product 21 --region $code
done
