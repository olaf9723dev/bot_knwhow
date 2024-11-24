import imaplib
import base64
import requests
import hashlib
import os

# Raw data in the given format
raw_data = "roulzcosmus@outlook.com:u2IdcAUDk9EBXTK:M.C535_SN1.0.U.-Ck06cyDOHLqZbxK8t4M9JjzJtdHOvqEgqtgyEOdaH!NstNd2ojBoTFLZFHu7caZNXkte*EuCIdwQoRzdQw*E0923Uv3cNzVZpki0NMvLXttfHpMJzHLhc4Swbhk8bhzmk3VOP2jCpe76hO9E*ywreH83WABJoWYygsd!1tCuhrlTYAyzgLw6fFZ7X7uKa8d1Py12B0WilUy24RoDnVMdQoQxRgUTGWgJw1Y9979d*VHl7UeblMxIchLCOiwagW5nBdGzzhoWAU4Jv6Mc40KEKABAlwxYeCJQGTe0vLN!aXVGNJHCCXxRoMXreNTRkTvj!OS6G*yzCcq9Q7Egaf9JTIDNZhsEySwY7RBXCuBB8DkNAXlRA17mcqD2d9LhLSMzTkkgXqYmW*mOuM!kCpEeZddseIDm8yBDLvJQVFRatJ6Y:9e5f94bc-e8a4-4e73-b8be-63364c29d753"

# Parse the data
data_parts = raw_data.split(":")
login = data_parts[0]         # Email address
password = data_parts[1]      # Password (not used in OAuth2)
refresh_token = data_parts[2] # Refresh token
client_id = data_parts[3]     # Client ID

# Constants
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
IMAP_SERVER = "outlook.office365.com"
IMAP_PORT = 993
GRAPH_API_URL = "https://graph.microsoft.com/v1.0/me/messages"
redirect_uri = "https://login.microsoftonline.com/common/oauth2/nativeclient"
# scope = "https://ads.microsoft.com/msads.manage"
# scope = "https://graph.microsoft.com/.default"
scope = "https://ps.outlook.com/.default"

# Step 1: Obtain Access Token
def get_access_token(client_id, refresh_token):
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        'client_id': client_id,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'scope': scope,
    }
    response = requests.post(TOKEN_URL, data=payload, headers=token_headers)
    if response.status_code == 200:
        token_data = response.json()

        return token_data['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")

# Step 2: Connect to IMAP using OAuth2
def connect_to_imap(login, access_token):
    auth_string = f"user={login}\x01auth=Bearer {access_token}\x01\x01"
    base64_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    # base64_auth_string = base64.b64encode(auth_string)
    
    print(base64_auth_string)
    # Establish IMAP connection
    imap_conn = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    try:
        imap_conn.authenticate('XOAUTH2', lambda _: base64_auth_string)
        print("Authentication successful!")
        return imap_conn
    except imaplib.IMAP4.error as e:
        print(f"Failed to authenticate: {e}")
        return None

# Main Execution
try:
    print("Fetching access token...")
    access_token = get_access_token(client_id, refresh_token)
    print("Access token obtained successfully.")

    print("Connecting to IMAP...")
    imap_conn = connect_to_imap(login, access_token)

    if imap_conn:
        # Example: List mailboxes
        status, mailboxes = imap_conn.list()
        if status == "OK":
            print("Mailboxes:")
            for mailbox in mailboxes:
                print(mailbox.decode())

        # Don't forget to logout
        imap_conn.logout()

except Exception as e:
    print(f"Error: {e}")
