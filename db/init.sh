#!/bin/bash

function show_help() {
    echo $0 [-D] [-t] [-d DATABASE] [-u LOGIN_USER] [-p PASSWORD]
}

function parse_args() {
    local IS_DELETE_ALL=0
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
            * )
                ;;
        esac
        shift

        if [ -z "${1}" ]; then break; fi
    done

    echo ${IS_DELETE_ALL} ${DB} ${USER} ${PASSWORD}
}

function create_db() {
    local SCHEME=$1
    local DATA_DIR=$2
    local USER=$3
    local PASSWORD=$4
    local DB_COMMAND=''

    DB_COMMAND="mysql -p${PASSWORD} -u ${USER}"
    ${DB_COMMAND} < ${SCHEME}
    DB_COMMAND="${DB_COMMAND} ${DB} -e"

    for TABLE in $(ls ${DATA_DIR} | sed -e 's/\.txt//g')
    do
        echo initializing ${TABLE}...
        cat ${DATA_DIR}/${TABLE}.txt | while read VALUES
        do
            if [[ "${VALUES}" =~ ^# ]]; then
                continue
            fi
            ${DB_COMMAND} "INSERT INTO ${TABLE} VALUES (${VALUES})"
        done
    done
}

function delete_db() {
    local USER=$1
    local PASSWORD=$2
    local DB=$3
    local DB_COMMAND="mysql -p${PASSWORD} -u ${USER}"

    echo "DROP DATABASE ${DB};" | ${DB_COMMAND}
}

if [[ "${@}" =~ .*\ (-h|help)\ .* ]]; then
    show_help
    exit 0
fi

RES=($(parse_args ${@}))
IS_DELETE_ALL=${RES[0]}
DB=${RES[1]}
USER=${RES[2]}
PASSWORD=${RES[3]}
DATA_DIR='data'

if [ ${IS_DELETE_ALL} -eq 0 ]; then
    create_db scheme.sql ${DATA_DIR} ${USER} ${PASSWORD}
else
    delete_db ${USER} ${PASSWORD} ${DB}
fi
