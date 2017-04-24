#!/bin/bash

DB_FOR_TEST='/tmp/necco_test.db'
SCHEME_FOR_TEST="$(dirname ${DB_FOR_TEST})/scheme.sql"

function show_help() {
    echo $0 [-D] [-t] [-d DATABASE] [-u LOGIN_USER] [-p PASSWORD]
}

function parse_args() {
    local IS_DELETE_ALL=0
    local IS_TEST=0
    local DB=necco
    local USER=temp
    local PASSWORD=temp

    while :
    do
        case ${1} in
            '-D' | '--delete-all' )
                IS_DELETE_ALL=1
                ;;
            '-d' | '--database' )
                shift
                DB=${1}
                ;;
            '-u' | '--user' )
                shift
                USER=${1}
                ;;
            '-p' | '--password' )
                shift
                PASSWORD=${1}
                ;;
            '-t' | '--test' )
                shift
                IS_TEST=1
                ;;
            * )
                ;;
        esac
        shift

        if [ -z "${1}" ]; then break; fi
    done

    echo ${IS_TEST} ${IS_DELETE_ALL} ${DB} ${USER} ${PASSWORD}
}

function create_db() {
    local IS_TEST=$1
    local SCHEME=$2
    local DATA_DIR=$3
    local USER=$4
    local PASSWORD=$5
    local DB_COMMAND=''

    if [ ${IS_TEST} -ne 0 ]; then
        DB_COMMAND="sqlite3 ${DB_FOR_TEST}"
        cat ${SCHEME} | \
            sed -e '/^CREATE DATABASE /d' | \
            sed -e '/^USE /d' | \
            sed -e 's/ INT / INTEGER /g' | \
            sed -e 's/ BIGINT / INTEGER /g' | \
            sed -e 's/ UNSIGNED / /g' | \
            sed -e 's/ AUTO_INCREMENT */ AUTOINCREMENT /g' \
            > ${SCHEME_FOR_TEST}
        ${DB_COMMAND} < ${SCHEME_FOR_TEST}
    else
        DB_COMMAND="mysql -p${PASSWORD} -u ${USER}"
        ${DB_COMMAND} < ${SCHEME}
        DB_COMMAND="${DB_COMMAND} ${DB} -e"
    fi

    for TABLE in $(ls ${DATA_DIR} | sed -e 's/\.txt//g')
    do
        echo initializing ${TABLE}...
        cat ${DATA_DIR}/${TABLE}.txt | while read VALUES
        do
            if [[ "${VALUES}" =~ ^# ]]; then
                COLUMNS=$(echo ${VALUES} | sed -e 's/^#//')
                continue
            fi
            if [ ${IS_TEST} -eq 0 ]; then
                ${DB_COMMAND} "INSERT INTO ${TABLE} VALUES (${VALUES})"
            else
                ${DB_COMMAND} "INSERT INTO ${TABLE}(${COLUMNS}) VALUES (${VALUES})"
            fi
        done
    done
}

function delete_db() {
    local IS_TEST=$1
    local USER=$2
    local PASSWORD=$3
    local DB=$4
    local DB_COMMAND="mysql -p${PASSWORD} -u ${USER}"

    if [ ${IS_TEST} -eq 0 ]; then
        echo "DROP DATABASE ${DB};" | ${DB_COMMAND}
    else
        echo Deleting ${DB_FOR_TEST}...
        rm -f ${DB_FOR_TEST}
    fi
}

if [[ "${@}" =~ .*\ (-h|help)\ .* ]]; then
    show_help
    exit 0
fi

RES=($(parse_args ${@}))
IS_TEST=${RES[0]}
IS_DELETE_ALL=${RES[1]}
DB=${RES[2]}
USER=${RES[3]}
PASSWORD=${RES[4]}

if [ ${IS_TEST} -ne 0 ]; then
    DATA_DIR='test_data'
else
    DATA_DIR='data'
fi

if [ ${IS_DELETE_ALL} -eq 0 ]; then
    create_db ${IS_TEST} scheme.sql ${DATA_DIR} ${USER} ${PASSWORD}
else
    delete_db ${IS_TEST} ${USER} ${PASSWORD} ${DB}
fi
