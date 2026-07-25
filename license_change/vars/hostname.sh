#!/bin/bash

# 로그 디렉토리 및 파일 설정
LOGDIR=/home/sysmng/license
DOWNLOADDIR=/home/sysmng/license/downloads

mkdir -p $DOWNLOADDIR
unzip -o /home/sysmng/license/JEUS_DEMO.zip -d $DOWNLOADDIR
unzip -o /home/sysmng/license/WEBTOB_DEMO.zip -d $DOWNLOADDIR

LOGFILE=$LOGDIR/license_hostname_change.log

echo "HOSTNAME=$(hostname)"

# 현재 HOSTNAME
HOSTNAME=$(hostname)

# 작업파일 경로 설정
FILE_PATH="/home/sysmng/license"

# HOSTNAME 일치하는 license 파일 매칭
MATCHING_FILES=$(ls "$FILE_PATH/downloads" | grep "$HOSTNAME$")

# 파일존재 여부 확인 후 이름 변경
if [ -n "$MATCHING_FILES" ]; then
        for FILE in $MATCHING_FILES; do
        mv "$DOWNLOADDIR/$FILE" "/home/sysmng/license/license.dat"
        echo "$(date) - 파일 '$FILE'을 license으로 변경" >> $LOGFILE
        done
else
        echo "$(date) - license_$HOSTNAME 파일을 찾을 수 없음" >> $LOGFILE
fi

echo -e "[info] HOSTNAME: $HOSTNAME / FILE_PATH: $FILE_PATH / MATCHING_FILES: $MATCHING_FILES / NEW_NAME: license.dat / FILE: $FILE"
echo "$(date) ########## 작업 완료 ##########" >> $LOGFILE
