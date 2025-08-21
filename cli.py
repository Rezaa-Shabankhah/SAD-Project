import requests
from colorama import init, Fore, Style

init(autoreset=True)

BASE = "http://127.0.0.1:8000/api"

def clear():
    print("\033[2J\033[H", end="")

def call_login(student_number,email=None,password=None):
    payload = {"student_number":student_number}
    if email is not None:
        payload["email"]=email
        payload["password"]=password
    r = requests.post(f"{BASE}/login/", json=payload)
    if r.status_code in (200,201):
        return r.json()
    return {"error":r.json().get("detail","error")}

def create_user_api(student_number,email,password):
    payload = {"student_number":student_number,"email":email,"password":password}
    r = requests.post(f"{BASE}/users/", json=payload)
    return r

def get_announcements():
    r = requests.get(f"{BASE}/announcements/")
    return r.json() if r.ok else []

def get_announcement(id):
    r = requests.get(f"{BASE}/announcements/{id}/")
    return r.json() if r.ok else None

def create_announcement(author_id,title,content):
    payload = {"author_id":author_id,"title":title,"content":content}
    r = requests.post(f"{BASE}/announcements/", json=payload)
    return r

def update_announcement(id,role,title,content):
    payload = {"role":role,"title":title,"content":content}
    r = requests.put(f"{BASE}/announcements/{id}/", json=payload)
    return r

def delete_announcement(id,role):
    payload = {"role":role}
    r = requests.delete(f"{BASE}/announcements/{id}/", json=payload)
    return r

def get_articles():
    r = requests.get(f"{BASE}/articles/?status=APPROVED")
    return r.json() if r.ok else []

def create_article(user_id,title,body,role):
    payload = {"user_id":user_id,"title":title,"content":body}
    r = requests.post(f"{BASE}/articles/", json=payload)
    return r

def get_article(id):
    r = requests.get(f"{BASE}/articles/{id}/")
    return r.json() if r.ok else None

def update_article(id,role,title,content):
    payload = {"role":role,"title":title,"content":content}
    r = requests.put(f"{BASE}/articles/{id}/", json=payload)
    return r

def delete_article(id,role):
    payload = {"role":role}
    r = requests.delete(f"{BASE}/articles/{id}/", json=payload)
    return r

def get_events():
    r = requests.get(f"{BASE}/events/")
    return r.json() if r.ok else []

def get_event(id):
    r = requests.get(f"{BASE}/events/{id}/")
    return r.json() if r.ok else None

def create_event(role,title,desc,cap):
    payload = {"role":role,"title":title,"description":desc,"capacity":cap}
    r = requests.post(f"{BASE}/events/", json=payload)
    return r

def join_event(event_id,user_id):
    payload = {"user_id":user_id}
    r = requests.post(f"{BASE}/events/{event_id}/join/", json=payload)
    return r

def get_comments(target_type,target_id):
    params = {"target_type":target_type,"target_id":target_id}
    r = requests.get(f"{BASE}/comments/", params=params)
    return r.json() if r.ok else []

def add_comment_api(author_id,target_type,target_id,content):
    payload = {"author_id":author_id,"target_type":target_type,"target_id":target_id,"content":content}
    r = requests.post(f"{BASE}/comments/", json=payload)
    return r

def delete_comment_api(comment_id,role):
    payload = {"role":role}
    r = requests.delete(f"{BASE}/comments/{comment_id}/", json=payload)
    return r

def get_users_admin():
    r = requests.get(f"{BASE}/admin/users/")
    return r.json() if r.ok else []

def get_pending_articles_admin():
    r = requests.get(f"{BASE}/admin/pending_articles/")
    return r.json() if r.ok else []

def admin_article_action(id,action,role):
    payload = {"role":role}
    r = requests.post(f"{BASE}/admin/articles/{id}/{action}/", json=payload)
    return r

def get_event_participants(event_id):
    params = {"event_id":event_id}
    r = requests.get(f"{BASE}/admin/event_participants/", params=params)
    return r.json() if r.ok else []

def login():
    print(Fore.BLUE + "Welcome!")
    sid = input("Enter your Student ID: ")
    resp = call_login(sid)
    if "error" in resp:
        print(Fore.RED + str(resp["error"]))
        input("\nPress Enter...")
        return None
    student = resp.get("student")
    user = resp.get("user")
    if user is None:
        print("No accounts found. Create one:")
        email = input("New Email: ")
        pwd = input("New Password: ")
        r = create_user_api(sid,email,pwd)
        if r.status_code == 201:
            print(Fore.GREEN + "Account created. Please login again.")
        else:
            print(Fore.RED + str(r.json().get("detail","error")))
        input("\nPress Enter...")
        return None
    email = input("Email: ")
    pwd = input("Password: ")
    auth = call_login(sid,email,pwd)
    if auth.get("error"):
        print(Fore.RED + str(auth["error"]))
        input("\nPress Enter...")
        return None
    return auth.get("user")

def show_comments(target_type,target_id):
    comments = get_comments(target_type,target_id)
    if not comments:
        print("No comments yet.")
    else:
        for comment in comments:
            name = comment.get("author_name") or "unknown"
            print(f"{comment['id']}. {name} : {comment['content']}")
            print("-" * 50)

def add_comment(target_type,target_id,user_id):
    content = input("Enter your comment: ").strip()
    if content:
        r = add_comment_api(user_id,target_type,target_id,content)
        if r.ok:
            print(Fore.GREEN + "Comment added!")
        else:
            print(Fore.RED + str(r.json().get("detail","error")))

def delete_comment():
    comment_id = input("Enter comment ID to delete: ")
    if comment_id.isdigit():
        return comment_id
    return None

def view_content_with_comments(content_type,content_id,user):
    if content_type == "ANNOUNCEMENT":
        content = get_announcement(content_id)
        if not content:
            return
        clear()
        print(Fore.YELLOW + f"--- {content['title']} ---")
        print(content["content"])
    elif content_type == "ARTICLE":
        content = get_article(content_id)
        if not content:
            return
        clear()
        print(Fore.YELLOW + f"--- {content['title']} ---")
        print(content["content"])
    elif content_type == "EVENT":
        content = get_event(content_id)
        if not content:
            return
        clear()
        print(Fore.YELLOW + f"--- {content['title']} ---")
        print(content.get("description") or "")
        print(f"Capacity: {content['capacity']}, Registered: {content['registered_count']}")
    show_comments(content_type,content_id)
    print("\nOptions:")
    if content_type == "ANNOUNCEMENT" and user["role"] == "MEMBER":
        print("E. Edit | D. Delete | A. Add Comment")
    elif content_type == "ANNOUNCEMENT" and user["role"] == "ADMIN":
        print("E. Edit | D. Delete | A. Add Comment | DC. Delete Comment")
    elif content_type == "ARTICLE" and user["role"] == "ADMIN":
        print("E. Edit | D. Delete | A. Add Comment | DC. Delete Comment")
    elif content_type == "EVENT" and user["role"] == "ADMIN":
        print("E. Edit | D. Delete | A. Add Comment | DC. Delete Comment")
    elif content_type == "EVENT" and user["role"] == "STUDENT":
        print("A. Add Comment | J. Join event")
    else:
        print("A. Add Comment")
    action = input("> ").upper()
    if action == "A":
        add_comment(content_type,content_id,user["id"])
        input("\nPress Enter...")
        return view_content_with_comments(content_type,content_id,user)
    elif action == "DC" and user["role"] == "ADMIN":
        cid = delete_comment()
        if cid:
            r = delete_comment_api(cid,user["role"])
            if r.status_code == 204:
                print(Fore.GREEN + "Comment deleted!")
            else:
                print(Fore.RED + str(r.json().get("detail","error")))
        input("\nPress Enter...")
        return view_content_with_comments(content_type,content_id,user)
    if content_type == "ANNOUNCEMENT" and user["role"] in ("MEMBER","ADMIN"):
        if action == "E":
            new_title = input("New title: ")
            new_content = input("New content: ")
            r = update_announcement(content_id,user["role"],new_title,new_content)
            if r.ok:
                print(Fore.GREEN + "Updated")
            input("\nPress Enter...")
        elif action == "D":
            r = delete_announcement(content_id,user["role"])
            if r.status_code == 204:
                print(Fore.GREEN + "Deleted")
            input("\nPress Enter...")
    elif content_type == "ARTICLE" and user["role"] == "ADMIN":
        if action == "E":
            new_title = input("New title: ")
            new_content = input("New content: ")
            r = update_article(content_id,user["role"],new_title,new_content)
            if r.ok:
                print(Fore.GREEN + "Updated")
            input("\nPress Enter...")
        elif action == "D":
            r = delete_article(content_id,user["role"])
            if r.status_code == 204:
                print(Fore.GREEN + "Deleted")
            input("\nPress Enter...")
    elif content_type == "EVENT":
        if action == "J" and user["role"] != "ADMIN":
            r = join_event(content_id,user["id"])
            if r.status_code in (201,200):
                print("Joined!")
            else:
                print(Fore.RED + str(r.json().get("detail","error")))
            input("Press Enter...")
        elif action == "E" and user["role"] == "ADMIN":
            new_title = input("New title: ")
            new_desc = input("New description: ")
            new_cap = int(input("New capacity: "))
            create_event(user["role"],new_title,new_desc,new_cap)
            input("Press Enter...")
        elif action == "D" and user["role"] == "ADMIN":
            print("Delete via admin panel")
            input("Press Enter...")

def comment_management(user):
    while True:
        clear()
        print(Fore.BLUE + "=== Comment Management ===")
        comments = requests.get(f"{BASE}/comments/").json() if requests else []
        r = requests.get(f"{BASE}/comments/")
        cur = []
        r = requests.get(f"{BASE}/comments/")
        r = requests.get(f"{BASE}/comments/", params={})
        r = requests.get(f"{BASE}/comments/")
        r = requests.get(f"{BASE}/comments/")
        all_comments = []
        r2 = requests.get(f"{BASE}/comments/")
        r3 = requests.get(f"{BASE}/comments/")
        comments = []
        params = {}
        q = requests.get(f"{BASE}/comments/", params=params)
        if q.ok:
            pass
        print(Fore.RED + "This feature is available via Admin Panel in CLI")
        input("\nPress Enter...")
        break

def menu(user):
    while True:
        clear()
        print(Fore.BLUE + "=== Main Menu ===")
        print("1. Announcements")
        print("2. Articles")
        print("3. Events")
        if user["role"] == "ADMIN":
            print("4. Admin Panel")
        print(Fore.RED + "0. Logout")
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
    while True:
        clear()
        print(Fore.BLUE + "=== Announcements ===")
        if user["role"] in ("MEMBER","ADMIN"):
            print("C. Create new announcement")
            print("-" * 26)
        anns = get_announcements()
        for a in anns:
            name = a.get("author_name") or "unknown"
            print(f"{a['id']}. {a['title']} (by {name})")
        print("0. Back")
        choice = input("> ").upper()
        if choice == "0":
            break
        elif choice == "C" and user["role"] in ("MEMBER","ADMIN"):
            title = input("Title: ")
            content = input("Content: ")
            create_announcement(user["id"],title,content)
        elif choice.isdigit():
            view_content_with_comments("ANNOUNCEMENT",choice,user)

def articles(user):
    while True:
        clear()
        print(Fore.BLUE + "=== Articles ===")
        if user["role"] == "ADMIN":
            print("C. Create new article")
        else:
            print("R. Request new article")
        print("-" * 22)
        arts = get_articles()
        for a in arts:
            print(f"{a['id']}. {a['title']}")
        print("0. Back")
        choice = input("> ").upper()
        if choice == "0":
            break
        elif choice == "R" and user["role"] != "ADMIN":
            title = input("Title: ")
            body = input("Body: ")
            create_article(user["id"],title,body,user["role"])
        elif choice == "C" and user["role"] == "ADMIN":
            title = input("Title: ")
            body = input("Body: ")
            create_article(user["id"],title,body,user["role"])
        elif choice.isdigit():
            view_content_with_comments("ARTICLE",choice,user)

def events(user):
    while True:
        clear()
        print(Fore.BLUE + "=== Events ===")
        if user["role"] == "ADMIN":
            print("C. Create new event")
            print("-" * 19)
        evs = get_events()
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
            create_event(user["role"],title,desc,cap)
        elif choice.isdigit():
            view_content_with_comments("EVENT",choice,user)

def admin_panel(user):
    while True:
        clear()
        print(Fore.BLUE + "=== Admin Panel ===")
        print("1. View users")
        print("2. Pending article requests")
        print("3. Event participants")
        print("4. Comment Management")
        print("0. Back")
        choice = input("> ")
        if choice == "0":
            break
        elif choice == "1":
            rows = get_users_admin()
            for r in rows:
                s = r.get("student")
                print(f"{s['student_number']} - {s['student']['name']} ({s['student']['role']})" if s else f"{r.get('email')}")
            input("\nPress Enter...")
        elif choice == "2":
            rows = get_pending_articles_admin()
            for r in rows:
                print(f"{r['id']}. {r['title']}")
            sel = input("Select article ID to review (0 back): ")
            if sel.isdigit() and sel != "0":
                art = get_article(sel)
                if art:
                    clear()
                    print(f"{art['title']}\n{art['content']}")
                    act = input("\nA=Approve | D=Deny > ").upper()
                    if act == "A":
                        admin_article_action(sel,"approve",user["role"])
                    elif act == "D":
                        admin_article_action(sel,"reject",user["role"])
        elif choice == "3":
            evs = get_events()
            for e in evs:
                print(f"{e['id']}. {e['title']}")
            sel = input("Select event ID: ")
            if sel.isdigit():
                rows = get_event_participants(sel)
                for r in rows:
                    print(f"{r['student_number']} - {r['name']}")
                input("\nPress Enter...")
        elif choice == "4":
            comment_management(user)

def main():
    user = None
    while not user:
        clear()
        user = login()
    menu(user)

if __name__ == "__main__":
    main()
