# Now in Android - Run & Report Script
$env:PYTHONPATH = "."

Write-Host "[NiA] Running Pure Python Tests..." -ForegroundColor Cyan
pytest -s tests/

Write-Host "[NiA] Generating Markdown Report..." -ForegroundColor Cyan
python report_generator.py

Write-Host "[NiA] Finished! Check REPORT.md for results." -ForegroundColor Green
