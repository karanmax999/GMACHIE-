"""LinkedIn OAuth 2.0 Token & URN retrieval helper.

This script helps developers generate the redirect URL, exchange the authorization code
for a 3-legged access token, and fetch the user's URN for env configuration.
"""

import httpx
import urllib.parse
import sys
import os

def main():
    print("==========================================================")
    print("       GMACHIE LinkedIn OAuth 2.0 Helper Script           ")
    print("==========================================================\n")
    
    # Check for client keys in env or input
    client_id = os.getenv("LINKEDIN_CLIENT_ID") or input("Enter LinkedIn Client ID: ").strip()
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET") or input("Enter LinkedIn Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("Error: Client ID and Client Secret are required.")
        sys.exit(1)
        
    redirect_uri = input("Enter Redirect URI (default: https://oauth.pstmn.io/v1/browser-callback): ").strip()
    if not redirect_uri:
        redirect_uri = "https://oauth.pstmn.io/v1/browser-callback"
        
    # Standard scopes for OpenID Connect + UGC posting
    scopes = "openid profile w_member_social"
    encoded_scopes = urllib.parse.quote(scopes)
    encoded_redirect = urllib.parse.quote(redirect_uri)
    
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={encoded_redirect}&"
        f"state=gmachie_state_1234&"
        f"scope={encoded_scopes}"
    )
    
    print("\n1. Open the following URL in your browser to authorize:")
    print("-" * 80)
    print(auth_url)
    print("-" * 80)
    
    print("\n2. After authorizing, you will be redirected to your Redirect URI.")
    print("Copy the 'code' parameter from the URL bar.")
    auth_code = input("\nEnter the authorization code: ").strip()
    
    if not auth_code:
        print("Error: Authorization code cannot be empty.")
        sys.exit(1)
        
    print("\n3. Exchanging authorization code for Access Token...")
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    try:
        response = httpx.post(token_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        print("\nSuccess! Token obtained successfully.")
        
        print("\n4. Fetching your LinkedIn Profile URN...")
        # Get member profile using OpenID userinfo or me
        userinfo_url = "https://api.linkedin.com/v2/userinfo"
        profile_response = httpx.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            sub = profile_data.get("sub")
            author_urn = f"urn:li:person:{sub}"
            name = profile_data.get("name")
            print(f"Authenticated as: {name}")
        else:
            # Fallback to me endpoint
            me_url = "https://api.linkedin.com/v2/me"
            profile_response = httpx.get(me_url, headers={"Authorization": f"Bearer {access_token}"})
            profile_response.raise_for_status()
            profile_data = profile_response.json()
            person_id = profile_data.get("id")
            author_urn = f"urn:li:person:{person_id}"
            print(f"Authenticated as: {profile_data.get('localizedFirstName')} {profile_data.get('localizedLastName')}")
            
        print("\n==========================================================")
        print("          Add these to your backend/.env file:            ")
        print("==========================================================")
        print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
        print(f"LINKEDIN_AUTHOR_URN={author_urn}")
        print("==========================================================\n")
        
    except httpx.HTTPStatusError as e:
        print(f"\nAPI Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
