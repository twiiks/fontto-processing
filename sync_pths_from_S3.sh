# !!!!!!!!필독!!!!!!!!
# aws 의 위치와 pths폴더의 위치를 바꿔주세요
# !!!!!!!!!!!!!!!!!!!!

WHERE_AWS=/Users/sjang/.pyenv/versions/anaconda3-4.4.0/bin/
WHERE_PTHS=/Users/sjang/work/fontto/fontto-processing/data

echo `date` >> ${WHERE_PTHS}/cron_log.txt
${WHERE_AWS}/aws s3 sync --no-progress --delete s3://fontto/data/pths/ ${WHERE_PTHS}/pths/ >> ${WHERE_PTHS}/cron_log.txt
