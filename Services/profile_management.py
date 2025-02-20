
from DataBase.user import USER
from Services.auth import get_current_user


def run_profile_management():
    while (user_input :=input(
        f'''
--Profile management--
    Hi, {get_current_user().name}
    press 1 to update your name
    press 2 to update your password
    press 0 to go back
    Enter your selection:
    '''
    )) != "0":
        try:
            match user_input:
                case "1":
                       name = input("Enter new name: ")
                       get_current_user().update(name=name)
                       print("Name updated successfully.")

                case "2":
                    new_password = input("Enter your new password : ")
                    get_current_user().update(password=new_password)
                    print("password updated successfully.")

        except Exception as e:
            print(f"ERROR: {e}")