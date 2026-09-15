import os

from dotenv import load_dotenv
from mem0 import Memory


load_dotenv()

memory_config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "wasid_memories",
            "path": "qdrant_data"
        }
    }
}

memory = Memory.from_config(memory_config)

USER_ID = "wasid"


def get_memories():
    result = memory.search(
        "user name education skills career goals preferences favorite food likes dislikes",
        filters={"user_id": USER_ID},
        limit=100
    )

    return result.get("results", [])


def show_memories():
    memories = get_memories()

    print("\nStored memories:\n")

    if not memories:
        print("No memories found.")
        return

    for index, item in enumerate(memories, start=1):
        memory_id = item.get("id", "ID_NOT_AVAILABLE")
        memory_text = item.get("memory", "")

        print(f"{index}. {memory_text}")
        print(f"   ID: {memory_id}\n")


def delete_memory():
    memories = get_memories()

    if not memories:
        print("No memories available.")
        return

    show_memories()

    selected = input(
        "Delete karne ke liye memory number enter karo, "
        "ya cancel ke liye 'cancel' likho: "
    ).strip()

    if selected.lower() == "cancel":
        print("Deletion cancelled.")
        return

    if not selected.isdigit():
        print("Invalid number.")
        return

    index = int(selected)

    if index < 1 or index > len(memories):
        print("Invalid memory number.")
        return

    selected_memory = memories[index - 1]
    memory_id = selected_memory.get("id")

    if not memory_id:
        print("Is memory ka ID available nahi hai.")
        return

    print("\nSelected memory:")
    print(selected_memory.get("memory", ""))

    confirmation = input(
        "Kya tum ise delete karna chahte ho? "
        "Type 'YES' to confirm: "
    ).strip()

    if confirmation != "YES":
        print("Deletion cancelled.")
        return

    try:
        memory.delete(memory_id)
        print("Memory deleted successfully.")
    except Exception as error:
        print("Memory delete nahi ho saki:")
        print(error)


def main():
    print("\nMemory Manager")
    print("1. Show memories")
    print("2. Delete one memory")
    print("3. Exit")

    while True:
        choice = input("\nChoose option: ").strip()

        if choice == "1":
            show_memories()

        elif choice == "2":
            delete_memory()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. 1, 2 ya 3 choose karo.")


if __name__ == "__main__":
    main()