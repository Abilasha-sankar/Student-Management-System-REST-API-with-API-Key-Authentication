import urllib.request
import urllib.error
import urllib.parse
API_KEY = "STUDENT123"
BASE_URL = "http://localhost:8081/student"
while True:
    print("\n========== STUDENT MENU ==========")
    print("1. CREATE")
    print("2. DISPLAY")
    print("3. UPDATE")
    print("4. DELETE")
    print("5. EXIT")
    choice = input("Enter Choice: ")
    try:
        # CREATE
        if choice == "1":
            sid = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            name = urllib.parse.quote(name)
            url = f"{BASE_URL}?id={sid}&name={name}"
            request = urllib.request.Request(url, method="POST")
            request.add_header("X-API-KEY", API_KEY)
            response = urllib.request.urlopen(request)
            print("\n------------------------------")
            print(response.read().decode())
            print("------------------------------")
        # DISPLAY
        elif choice == "2":
            url = BASE_URL
            request = urllib.request.Request(url, method="GET")
            request.add_header("X-API-KEY", API_KEY)
            response = urllib.request.urlopen(request)
            print("\n------------------------------")
            print(response.read().decode())
            print("------------------------------")
        # UPDATE
        elif choice == "3":
            sid = input("Enter Student ID: ")
            name = input("Enter New Name: ")
            name = urllib.parse.quote(name)
            url = f"{BASE_URL}?id={sid}&name={name}"
            request = urllib.request.Request(url, method="PUT")
            request.add_header("X-API-KEY", API_KEY)
            response = urllib.request.urlopen(request)
            print("\n------------------------------")
            print(response.read().decode())
            print("------------------------------")
        # DELETE
        elif choice == "4":
            sid = input("Enter Student ID: ")
            url = f"{BASE_URL}?id={sid}"
            request = urllib.request.Request(url, method="DELETE")
            request.add_header("X-API-KEY", API_KEY)
            response = urllib.request.urlopen(request)
            print("\n------------------------------")
            print(response.read().decode())
            print("------------------------------")
        # EXIT
        elif choice == "5":
            print("\nThank You!")
            break
        else:
            print("Invalid Choice!")
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print("HTTP Error:", e.code)
        print("Message:", error_msg)
    except urllib.error.URLError:
        print("Server Not Running!")
    except Exception as e:
        print("Error:", e)