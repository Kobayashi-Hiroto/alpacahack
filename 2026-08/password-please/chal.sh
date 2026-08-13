secret="${RANDOM}${RANDOM}${RANDOM}${RANDOM}"

printf $secret
printf 'Password: '
read -r password

if [[ $secret == $password ]]; then
    cat /flag.txt
else
    echo 'Access denied'
fi
