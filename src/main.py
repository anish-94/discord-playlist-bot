import os
from dotenv import load_dotenv
from controllers.discord_client import DiscordClient

def main():
    load_dotenv()
    client = DiscordClient()
    client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()