import asyncio

from src.application.plugin_core import PluginCore


async def main():
    core = PluginCore()
    await core.start()

if __name__ == "__main__":
    asyncio.run(main())
