import supabase
import hashlib
from random import randint
from salts import salts

def add_prefix(redirect_code: str):
    return f"http://127.0.0.1:8000/{redirect_code}"

def push_shortened_url(supabase: supabase.Client, url: str, redirect_code: str):
    try:
        supabase.table("urls").insert(
            {
                "url": url,
                "redirect_code": redirect_code
            }
        ).execute()

    except Exception as e:
        raise Exception("Could not shorten url...")
    
def generate_redirect_code(url: str):
    url_bytes = url.encode()
    redirect_code = hashlib.md5(url_bytes).hexdigest()[:7]
    return redirect_code

def get_existing_short_code(supabase: supabase.Client, url: str):
    data = supabase.table("urls").select("redirect_code").eq("url", url).execute().data
    if data:
        exisitng_redirect_code = data[0]['redirect_code']
        return exisitng_redirect_code
    return ""

def recursive_free_code_search(supabase: supabase.Client, url: str):
    redirect_code = generate_redirect_code(url)
    while supabase.table("urls").select("redirect_code").eq("redirect_code", redirect_code).neq("url", url).execute().data:
        presalt = randint(0, len(salts)-1)
        postsalt = randint(0, len(salts)-1)
        redirect_code = generate_redirect_code(f"{presalt}{redirect_code}{postsalt}")
    return redirect_code

def get_redirect_code(supabase: supabase.Client, url: str):
    existing_short_code = get_existing_short_code(supabase, url)
    if existing_short_code:
        return existing_short_code
    return recursive_free_code_search(supabase, url)

def shorten_url(url: str, supabase: supabase.Client) -> str:
    redirect_code = get_redirect_code(supabase, url)
    push_shortened_url(supabase, url, redirect_code)
    shortened_url = add_prefix(redirect_code)
    return shortened_url
