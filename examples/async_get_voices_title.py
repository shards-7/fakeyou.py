import asyncio

import fakeyou

# Create an instance of the AsyncFakeYou class
fy = fakeyou.AsyncFakeYou()


# Define the main coroutine
async def main():
    # Call the login method with email and password and await the result
    login = await fy.login("< email >", "< password >")

    # Print the username of the logged-in user
    print("Logged in as:", login.username)

    # Call the list_voices method and await the result
    voices = await fy.list_voices()

    # Print the title number and title of each voice
    for i, title in enumerate(voices.title):
        print(f"Title {i}: {title}")


# Run the main coroutine in an event loop using asyncio.run()
asyncio.run(main())
