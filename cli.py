import pymysql


def get_conn():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="12345",
        database="university_association",
        cursorclass=pymysql.cursors.DictCursor,
    )


def clear():
    print("\033[2J\033[H", end="")


def login():
    conn = get_conn()
    with conn.cursor() as cur:
        sid = input("Enter your Student ID: ")
        cur.execute("SELECT * FROM students WHERE student_number=%s", (sid,))
        student = cur.fetchone()
        if not student:
            print("Invalid Student ID.")
            return None

        cur.execute("SELECT * FROM users WHERE student_id=%s", (student["id"],))
        user = cur.fetchone()
        if user:
            email = input("Email: ")
            pwd = input("Password: ")
            if email == user["email"] and pwd == user["password"]:
                return {**student, **user}
            else:
                print("Wrong credentials.")
                return None
        else:
            print("No account. Create one:")
            email = input("New Email: ")
            pwd = input("New Password: ")
            cur.execute("INSERT INTO users (student_id,email,password) VALUES (%s,%s,%s)", (student["id"], email, pwd))
            conn.commit()
            print("Account created. Please login again.")
            return None


def menu(user):
    while True:
        clear()
        print("=== Main Menu ===")
        print("1. Announcements")
        print("2. Articles")
        print("3. Events")
        if user["role"] == "ADMIN":
            print("4. Admin Panel")
        print("0. Logout")

        choice = input("> ")
        if choice == "1":
            announcements(user)
        elif choice == "2":
            articles(user)
        elif choice == "3":
            events(user)
        elif choice == "4" and user["role"] == "ADMIN":
            admin_panel(user)
        elif choice == "0":
            break


def announcements(user):
    conn = get_conn()
    with conn.cursor() as cur:
        while True:
            clear()
            print("=== Announcements ===")
            if user["role"] in ("MEMBER", "ADMIN"):
                print("C. Create new announcement")
                print("--------------------------")
            cur.execute("SELECT a.id,a.title,s.name FROM announcement a JOIN users u ON a.author_id=u.id JOIN students s ON u.student_id=s.id")
            anns = cur.fetchall()
            for a in anns:
                print(f"{a['id']}. {a['title']} (by {a['name']})")
            print("0. Back")

            choice = input("> ").upper()
            if choice == "0":
                break
            elif choice == "C" and user["role"] in ("MEMBER", "ADMIN"):
                title = input("Title: ")
                content = input("Content: ")
                cur.execute("INSERT INTO announcement (author_id,title,content) VALUES (%s,%s,%s)", (user["id"], title, content))
                conn.commit()
            elif choice.isdigit():
                cur.execute("SELECT * FROM announcement WHERE id=%s", (choice,))
                ann = cur.fetchone()
                if ann:
                    clear()
                    print(f"--- {ann['title']} ---")
                    print(ann["content"])
                    if user["role"] in ("MEMBER", "ADMIN"):
                        print("\nE. Edit | D. Delete")
                        act = input("> ").upper()
                        if act == "E":
                            new_title = input("New title: ")
                            new_content = input("New content: ")
                            cur.execute("UPDATE announcement SET title=%s,content=%s WHERE id=%s", (new_title, new_content, ann["id"]))
                            conn.commit()
                        elif act == "D":
                            cur.execute("DELETE FROM announcement WHERE id=%s", (ann["id"],))
                            conn.commit()
                    input("\nPress Enter...")


def articles(user):
    conn = get_conn()
    with conn.cursor() as cur:
        while True:
            clear()
            print("=== Articles ===")
            if user["role"] == "ADMIN":
                print("C. Create new article")
            else:
                print("R. Request new article")
            print("----------------------")
            cur.execute("SELECT * FROM article WHERE status='APPROVED'")
            arts = cur.fetchall()
            for a in arts:
                print(f"{a['id']}. {a['title']}")
            print("0. Back")

            choice = input("> ").upper()
            if choice == "0":
                break
            elif choice == "R" and user["role"] != "ADMIN":
                title = input("Title: ")
                body = input("Body: ")
                cur.execute("INSERT INTO article (title,content,status) VALUES (%s,%s,'PENDING')", (title, body))
                conn.commit()
                cur.execute("SELECT LAST_INSERT_ID() as new_id")
                new_id = cur.fetchone()["new_id"]
                cur.execute("INSERT INTO article_authors (article_id,users_id) VALUES (%s,%s)", (new_id, user["id"]))
                conn.commit()
            elif choice == "C" and user["role"] == "ADMIN":
                title = input("Title: ")
                body = input("Body: ")
                cur.execute("INSERT INTO article (title,content,status) VALUES (%s,%s,'APPROVED')", (title, body))
                conn.commit()
                cur.execute("SELECT LAST_INSERT_ID() as new_id")
                new_id = cur.fetchone()["new_id"]
                cur.execute("INSERT INTO article_authors (article_id,users_id) VALUES (%s,%s)", (new_id, user["id"]))
                conn.commit()
            elif choice.isdigit():
                cur.execute("SELECT * FROM article WHERE id=%s", (choice,))
                art = cur.fetchone()
                if art:
                    clear()
                    print(f"--- {art['title']} ---\n{art['content']}")
                    if user["role"] == "ADMIN":
                        print("\nE. Edit | D. Delete")
                        act = input("> ").upper()
                        if act == "E":
                            new_title = input("New title: ")
                            new_content = input("New content: ")
                            cur.execute("UPDATE article SET title=%s,content=%s WHERE id=%s", (new_title, new_content, art["id"]))
                            conn.commit()
                        elif act == "D":
                            cur.execute("DELETE FROM article WHERE id=%s", (art["id"],))
                            conn.commit()
                    input("\nPress Enter...")


def events(user):
    conn = get_conn()
    with conn.cursor() as cur:
        while True:
            clear()
            print("=== Events ===")
            if user["role"] == "ADMIN":
                print("C. Create new event")
                print("-------------------")
            cur.execute("SELECT * FROM event")
            evs = cur.fetchall()
            for e in evs:
                print(f"{e['id']}. {e['title']} (Capacity {e['capacity']}, Registered {e['registered_count']})")
            print("0. Back")

            choice = input("> ").upper()
            if choice == "0":
                break
            elif choice == "C" and user["role"] == "ADMIN":
                title = input("Title: ")
                desc = input("Description: ")
                cap = int(input("Capacity: "))
                cur.execute("INSERT INTO event (title,description,capacity,registered_count) VALUES (%s,%s,%s,0)", (title, desc, cap))
                conn.commit()
            elif choice.isdigit():
                cur.execute("SELECT * FROM event WHERE id=%s", (choice,))
                ev = cur.fetchone()
                if ev:
                    clear()
                    print(f"--- {ev['title']} ---\n{ev['description']}")
                    print(f"Capacity: {ev['capacity']}, Registered: {ev['registered_count']}")
                    if user["role"] == "ADMIN":
                        print("\nE. Edit | D. Delete")
                    else:
                        print("\nJ. Join this event")
                    act = input("> ").upper()
                    if act == "J" and user["role"] != "ADMIN":
                        try:
                            cur.execute("INSERT INTO event_registration (event_id,users_id) VALUES (%s,%s)", (ev["id"], user["id"]))
                            cur.execute("UPDATE event SET registered_count=registered_count+1 WHERE id=%s", (ev["id"],))
                            conn.commit()
                            print("Joined!")
                        except:
                            print("Already joined.")
                        input("Enter...")
                    elif act == "E" and user["role"] == "ADMIN":
                        new_title = input("New title: ")
                        new_desc = input("New description: ")
                        new_cap = int(input("New capacity: "))
                        cur.execute("UPDATE event SET title=%s,description=%s,capacity=%s WHERE id=%s", (new_title, new_desc, new_cap, ev["id"]))
                        conn.commit()
                    elif act == "D" and user["role"] == "ADMIN":
                        cur.execute("DELETE FROM event WHERE id=%s", (ev["id"],))
                        conn.commit()
                        print("Deleted.")


def admin_panel(user):
    conn = get_conn()
    with conn.cursor() as cur:
        while True:
            clear()
            print("=== Admin Panel ===")
            print("1. View users")
            print("2. Pending article requests")
            print("3. Event participants")
            print("0. Back")

            choice = input("> ")
            if choice == "0":
                break
            elif choice == "1":
                cur.execute("SELECT s.student_number,s.name,s.role FROM students s JOIN users u ON s.id=u.student_id")
                rows = cur.fetchall()
                for r in rows:
                    print(f"{r['student_number']} - {r['name']} ({r['role']})")
                input("\nEnter...")
            elif choice == "2":
                cur.execute("SELECT * FROM article WHERE status='PENDING'")
                rows = cur.fetchall()
                for r in rows:
                    print(f"{r['id']}. {r['title']}")
                sel = input("Select article ID to review (0 back): ")
                if sel.isdigit() and sel != "0":
                    cur.execute("SELECT * FROM article WHERE id=%s", (sel,))
                    art = cur.fetchone()
                    if art:
                        clear()
                        print(f"{art['title']}\n{art['content']}")
                        act = input("\nA=Approve | D=Deny > ").upper()
                        if act == "A":
                            cur.execute("UPDATE article SET status='APPROVED' WHERE id=%s", (sel,))
                            conn.commit()
                        elif act == "D":
                            cur.execute("UPDATE article SET status='REJECTED' WHERE id=%s", (sel,))
                            conn.commit()
            elif choice == "3":
                cur.execute("SELECT * FROM event")
                evs = cur.fetchall()
                for e in evs:
                    print(f"{e['id']}. {e['title']}")
                sel = input("Select event ID: ")
                if sel.isdigit():
                    cur.execute(
                        """SELECT s.student_number,s.name
                                   FROM event_registration er
                                   JOIN users u ON er.users_id=u.id
                                   JOIN students s ON u.student_id=s.id
                                   WHERE er.event_id=%s""",
                        (sel,),
                    )
                    rows = cur.fetchall()
                    for r in rows:
                        print(f"{r['student_number']} - {r['name']}")
                    input("\nEnter...")


def main():
    user = None
    while not user:
        clear()
        user = login()
    menu(user)


if __name__ == "__main__":
    main()
