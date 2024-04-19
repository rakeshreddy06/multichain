import asyncio

from tno.mpc.communication import Pool


async def async_main():
    # Create the pool for Bob.
    # Bob listens on port 61002 and adds Alice as client.
    pool = Pool()
    pool.add_http_server(addr="127.0.0.1", port=61002)
    pool.add_http_client("Alice", addr="127.0.0.1", port=61001)

    # Bob waits for a message from Alice and prints it.
    # He replies and shuts down his pool instance.
    message = await pool.recv("Alice")
    print(message)
    await pool.send("Alice", "Hello back to you, Alice!")
    await pool.shutdown()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())