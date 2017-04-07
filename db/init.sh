#!/bin/bash

function show_help() {
    echo $0 [-D] [-d DATABASE] [-u LOGIN_USER] [-p PASSWORD]
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
    local USER=$1
    local PASSWORD=$2
    local SCHEME=$3
    local VALUES_DIR=$4
    local MYSQL="mysql -p${PASSWORD} -u ${USER}"

    # create all table
    ${MYSQL} < ${SCHEME}

    for TABLE in $(ls ${VALUES_DIR} | sed -e 's/\.txt//g')
    do
        echo initializing ${TABLE}...
        cat ${VALUES_DIR}/${TABLE}.txt | while read VALUES
        do
            if [[ "${VALUES}" =~ ^# ]]; then
                continue
            fi
            ${MYSQL} ${DB} -e "INSERT INTO ${TABLE} VALUES (${VALUES})"
        done
    done
}

function delete_db() {
    local USER=$1
    local PASSWORD=$2
    local DB=$3
    local MYSQL="mysql -p${PASSWORD} -u ${USER}"

    # create all table
    echo "DROP DATABASE ${DB};" | ${MYSQL}
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

if [ ${IS_DELETE_ALL} -eq 0 ]; then
    create_db ${USER} ${PASSWORD} scheme.sql values
else
    delete_db ${USER} ${PASSWORD} ${DB}
fi
