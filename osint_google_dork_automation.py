import webbrowser
import time

def ask():
    u = input("username: ").strip()
    n = input("name: ").strip()
    s = input("surname: ").strip()
    return u,n,s

def build(u,n,s):
    d = []
    full = f"{n} {s}".strip()

    d.append(f'"{u}"')
    d.append(f'"{full}"')
    d.append(f'"{u}" site:instagram.com')
    d.append(f'"{u}" site:twitter.com')
    d.append(f'"{u}" site:facebook.com')
    d.append(f'"{u}" site:tiktok.com')
    d.append(f'"{u}" site:github.com')
    d.append(f'"{u}" site:linkedin.com')
    d.append(f'"{u}" filetype:pdf')
    d.append(f'"{u}" filetype:xls OR filetype:csv')
    d.append(f'"{u}" inurl:profile')
    d.append(f'"{u}" inurl:user')
    d.append(f'"{u}" intext:"email"')
    d.append(f'"{u}" intext:"password"')
    d.append(f'"{full}" site:vk.com')
    d.append(f'"{full}" site:ok.ru')
    d.append(f'"{full}" filetype:doc OR filetype:docx')
    d.append(f'"{full}" "@gmail.com"')
    d.append(f'"{full}" "@yahoo.com"')
    d.append(f'"{u}" "@gmail.com"')
    d.append(f'"{u}" "phone"')
    d.append(f'"{u}" "address"')

    return d

def make_links(dorks):
    links = []
    for q in dorks:
        links.append("https://www.google.com/search?q=" + q.replace(" ", "+"))
    return links

def save_txt(links):
    name = "osint_results.txt"
    with open(name, "w", encoding="utf-8") as f:
        for l in links:
            f.write(l + "\n")
    print("saved to", name)

def run(dorks):
    for i,x in enumerate(dorks):
        print(f"[{i+1}] {x}")

    print("\n1 - open in browser")
    print("2 - show links + save txt")
    choice = input("choose: ").strip()

    links = make_links(dorks)

    if choice == "1":
        for l in links:
            webbrowser.open(l)
            time.sleep(1)

    elif choice == "2":
        for i,l in enumerate(links):
            print(f"[{i+1}] {l}")
        save_txt(links)

    else:
        print("idk that option")

def main():
    while True:
        u,n,s = ask()
        d = build(u,n,s)
        run(d)
        again = input("again? y/n: ").lower()
        if again != "y":
            break

if __name__ == "__main__":
    main()
