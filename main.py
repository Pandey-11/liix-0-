import requests
import re
import json

def get_fb_name(token):
    url = f"https://graph.facebook.com/me?fields=id,name&access_token={token}"
    response = requests.get(url)
    data = response.json()
    
    if "name" in data:
        return data["name"]
    else:
        return None

def extract_token(cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
    }
    url = "https://business.facebook.com/business_locations"

    response = requests.get(url, cookies=cookies, headers=headers)

    if "access_token" in response.text:
        token = re.search(r'"access_token":"(EAA\w+)"', response.text)
        if token:
            token_value = token.group(1)
            print(f"\n✅ Your Access Token:\n{token_value}")

            # Extract User Name
            user_name = get_fb_name(token_value)
            if user_name:
                print(f"\n📌 Facebook Name: {user_name}")
            else:
                print("\n⚠ Unable to Fetch Facebook Name!")

        else:
            print("\n❌ Token Not Found. Try Again!\n")
    else:
        print("\n❌ Failed to Extract Token. Check Cookies or Try Again!\n")

if __name__ == "__main__":
    print("\n🔹 Facebook Cookies to Access Token & Name Extractor 🔹")
    raw_cookies = input("\n👉 Enter Your Facebook Cookies: ").strip()

    if "c_user=" in raw_cookies and "xs=" in raw_cookies:
        cookies_dict = {}
        for cookie in raw_cookies.split("; "):
            key, value = cookie.split("=", 1)
            cookies_dict[key] = value

        print(f"\n📌 Extracted c_user: {cookies_dict.get('c_user', 'Not Found')}")
        extract_token(cookies_dict)
    else:
        print("\n⚠ Invalid Cookie Format! Please Enter Valid Facebook Cookies.\n")
