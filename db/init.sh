#!/bin/bash

DB='necco'

function show_help() {
    echo $0 [-d DATABASE] [-u LOGIN_USER] [-p PASSWORD]
}

for OPT in "${@}"
do
    case ${OPT} in
        '-d' | '--database' )
            DB=${2}
            shift
            ;;
        '-u' | '--user' )
            USER=${2}
            shift
            ;;
        '-p' | '--password' )
            PASSWORD=${2}
            shift
            ;;
        '-h' | '--help' )
            show_help
            exit 0
            ;;
        * )
            shift
            ;;
    esac
done

MYSQL="mysql -p${PASSWORD} -u ${USER}"

# create all table
${MYSQL} < tables.sql

for TABLE in User Profile Ability Request UsersAbility UsersRequest Prefecture
do
    echo initializing ${TABLE}...
    cat values/${TABLE}.txt | while read VALUES
    do
        if [[ "${VALUES}" =~ ^# ]]; then
            continue
        fi
        ${MYSQL} ${DB} -e "INSERT INTO ${TABLE} VALUES (${VALUES})"
    done
done
