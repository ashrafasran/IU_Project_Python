from DataBase.user import USER
current_user:USER =None;

def login():
    global current_user
    print("-login-")
    email = input("Enter your email : ")
    user = USER.get(email)
    password=input("Enter your password : ")

    if password == user.password:
        current_user = user
        print("User login successfully.")
        return True
    else:
        print("your email or password is false.")
        return False

def register():
    global current_user
    print("-register-")
    name = input("Enter name: ")
    email = input("Enter email: ")

    while USER.email_exist(email):
        email = input("please enter another email: ")

    password = input("Enter password: ")
    user = USER(name=name, email=email, password=password)

    if user.save()==False :
        print(f"there is a problem in registration ")
        return False

    current_user = user
    print("User registered successfully.")
    return True

def logout():
    current_user=None

def get_current_user():
    return current_user