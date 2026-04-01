results=./results
rep_history=./final-report/history
report=./final-report
rm -rf $results 2>/dev/null
pytest --alluredir=$results
mv $rep_history $results 2>/dev/null || true
rm -rf $report 2>/dev/null
allure generate $results -o $report
allure open $report
