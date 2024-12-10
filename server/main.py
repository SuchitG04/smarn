import asyncio


async def main():

    search_api = await asyncio.create_subprocess_exec("python", "server/api/main.py")
    model_api = await asyncio.create_subprocess_exec("python", "server/model/main.py")
    screenshot_service = await asyncio.create_subprocess_exec(
        "python", "server/screenshot.py"
    )

    try:
        await asyncio.gather(
            search_api.wait(),
            model_api.wait(),
            screenshot_service.wait(),
        )
    except KeyboardInterrupt:
        print("Stopping server and subprocesses...")
        search_api.terminate()
        model_api.terminate()
        screenshot_service.terminate()


if __name__ == "__main__":
    asyncio.run(main())
