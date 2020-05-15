import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/'+ query_char
    res = requests.get(url)
    if(res.status_code != 200):
        raise RuntimeError(f'Error fetching: {res.status_code}, check api and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def password_hash_check(password):
    sha1_obj = (hashlib.sha1(password.encode('utf-8'))).hexdigest().upper() #convert password to sha1
    first_five, tail = sha1_obj[:5], sha1_obj[5:]
    response = request_api_data(first_five)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = password_hash_check(password)
        if count:
            print(f'{password} was found {count} times, choose a different one')
        else:
            print(f'{password} was not found, Carry on')
    return 'done!'
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))