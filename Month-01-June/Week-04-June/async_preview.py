import asyncio

async def slow_task(name):
    print(f"{name} started")
    await asyncio.sleep(1)
    print(f"{name} done")

async def main():
    await asyncio.gather(
        slow_task("Task A"),
        slow_task("Task B"),
        slow_task("Task C")
    )
asyncio.run(main())