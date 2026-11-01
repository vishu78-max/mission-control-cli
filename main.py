import json
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

file = Path(__file__).resolve().parent / "missions.json"

banner = r"""
    .       *                         .       *
               ___________________
              |   MISSION CONTROL |
              |___________________|
                   .--------.
                   |  o  o  |
                   |  ----  |
                  /|________|\
                 / |  [MC]  | \
                   |________|
                    /      \\
    -        Your corner of the galaxy.       .
"""


def save(data):
    with file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load():
    if file.exists():
        with file.open(encoding="utf-8") as f:
            return json.load(f)

    data = {"next_id": 1, "missions": []}
    save(data)
    return data


def show(data):
    active = [item for item in data["missions"] if not item["completed"]]
    finished = [item for item in data["missions"] if item["completed"]]

    print(f"\n{Fore.YELLOW}--- ACTIVE MISSIONS ---{Style.RESET_ALL}")
    for item in active:
        print(f"  {Fore.GREEN}[ ]{Style.RESET_ALL} #{item['id']}  {item['title']}")
    if not active:
        print(f"  {Fore.BLUE}All clear. The galaxy is quiet for now.{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}--- MISSION ARCHIVE ---{Style.RESET_ALL}")
    for item in finished:
        print(f"  {Fore.LIGHTBLACK_EX}[x] #{item['id']}  {item['title']}{Style.RESET_ALL}")
    if not finished:
        print(f"  {Fore.LIGHTBLACK_EX}Your heroic deeds will appear here.{Style.RESET_ALL}")

def add(data):
    title = input(f"\n{Fore.CYAN}Mission title: {Style.RESET_ALL}").strip()
    if not title:
        print(f"{Fore.RED}A mission needs a name, Commander.{Style.RESET_ALL}")
        return

    num = data["next_id"]
    data["missions"].append({"id": num, "title": title, "completed": False})
    data["next_id"] += 1
    save(data)
    print(f"{Fore.GREEN}Transmission received. Mission #{num} assigned: {title}{Style.RESET_ALL}")

def done(data):
    show(data)
    num = input(f"\n{Fore.CYAN}Mission ID to complete: {Style.RESET_ALL}").strip()
    for item in data["missions"]:
        if str(item["id"]) == num:
            if item["completed"]:
                print(f"{Fore.YELLOW}That mission is already in the archive, Commander.{Style.RESET_ALL}")
                return
            item["completed"] = True
            save(data)
            print(f"\n{Fore.GREEN}MISSION ACCOMPLISHED: {item['title']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Threat neutralized. One less problem in the galaxy.{Style.RESET_ALL}")
            return

    print(f"{Fore.RED}Mission not found. Check the ID on your mission board.{Style.RESET_ALL}")


def delete(data):
    show(data)
    num = input(f"\n{Fore.CYAN}Mission ID to delete: {Style.RESET_ALL}").strip()
    for item in data["missions"]:
        if str(item["id"]) == num:
            answer = input(f"{Fore.YELLOW}Delete mission #{num}: {item['title']}? (y/n): {Style.RESET_ALL}")
            if answer.strip().lower() == "y":
                data["missions"].remove(item)
                save(data)
                print(f"{Fore.RED}Mission #{num} removed from the records.{Style.RESET_ALL}")
            else:
                print("Deletion cancelled. Mission stays on the board.")
            return

    print(f"{Fore.RED}Mission not found. Check the ID on your mission board.{Style.RESET_ALL}")


def main():
    data = load()
    print(banner)
    print(f"{Fore.GREEN}Welcome back, Commander.{Style.RESET_ALL}")

    while True:
        num = sum(1 for item in data["missions"] if not item["completed"])
        print(f"\n{Fore.MAGENTA}" + "=" * 46 + f"{Style.RESET_ALL}")
        if num == 0:
            print(f"{Fore.BLUE}No active missions. Enjoy the peace, Commander.{Style.RESET_ALL}")
        elif num == 1:
            print(f"{Fore.YELLOW}1 active mission. The universe needs you.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}{num} active missions. The universe needs you.{Style.RESET_ALL}")

        print(f"""
{Fore.CYAN}1.{Style.RESET_ALL} {Fore.MAGENTA}View missions{Style.RESET_ALL}
{Fore.CYAN}2.{Style.RESET_ALL} {Fore.MAGENTA}Add a mission{Style.RESET_ALL}
{Fore.CYAN}3.{Style.RESET_ALL} {Fore.MAGENTA}Complete a mission{Style.RESET_ALL}
{Fore.CYAN}4.{Style.RESET_ALL} {Fore.MAGENTA}Delete a mission{Style.RESET_ALL}
{Fore.CYAN}5.{Style.RESET_ALL} {Fore.MAGENTA}Exit{Style.RESET_ALL}
""")
        choice = input(f"{Fore.CYAN}Your next move (1-5): {Style.RESET_ALL}").strip()

        if choice == "1":
            show(data)
        elif choice == "2":
            add(data)
        elif choice == "3":
            done(data)
        elif choice == "4":
            delete(data)
        elif choice == "5":
            print(f"\n{Fore.MAGENTA}Signing off. Stay legendary, Commander.\n{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Unknown command. Choose a number from 1 to 5.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
