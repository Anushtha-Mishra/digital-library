import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Set SUPABASE_URL and SUPABASE_KEY in your .env file!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)









# import os
# from supabase import create_client, Client
# from dotenv import load_dotenv

# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# if not SUPABASE_URL or not SUPABASE_KEY:
#     raise ValueError("Set SUPABASE_URL and SUPABASE_KEY in your .env file!")

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)