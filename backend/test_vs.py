import asyncio
from app.services.vector_store import vector_store

async def main():
    try:
        print("Querying...")
        res = vector_store.query(query_text="hi", n_results=1)
        print("Result:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
