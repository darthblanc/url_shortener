import supabase

def get_url(redirect_code: str, supabase: supabase.Client):
    url = ""
    try:
        url = supabase.table("urls").select("url").eq("redirect_code", redirect_code).execute().data[0]['url']
    except Exception as e:
        raise e
    return url
