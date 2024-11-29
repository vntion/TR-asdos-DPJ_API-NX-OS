import requests
import json
import os
import itertools
import sys
import time
import threading

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

switchuser = "admin"
switchpassword = "Admin_1234!"
token = ""

def animate_loading(message):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r' + message + ' ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def welcome_animation():
    print("=========================================")
    print("              Hallo user...              ")
    print("=========================================")
    time.sleep(1)
    print("  _    _       _      _     _       ")
    time.sleep(0.2)
    print(" | |  | |     | |    | |       ")
    time.sleep(0.2)
    print(" | |__| | __ _| |    | |      ___  ")
    time.sleep(0.2)
    print(" |  __  |/ _` | |  \ | |     / _ \ ")
    time.sleep(0.2)
    print(" | |  | | (_| | |___ | |____ ||_||  ")
    time.sleep(0.2)
    print(" |_|  |_|\__,_|__ __||_|____|\___/ ")
    time.sleep(1)


def goodbye_animation():
    print("                Gracias...               ")
    print("=========================================")
    time.sleep(1)
    print("  ____          _    _ ")
    time.sleep(0.2)
    print(" |  _ \        | |  | |")
    time.sleep(0.2)
    print(" | | | |  __ _ | |__| |")
    time.sleep(0.2)
    print(" | | | | / _` ||  __  |")
    time.sleep(0.2)
    print(" | |_| || (_| || |  | |")
    time.sleep(0.2)
    print(" |____/  \__,_||_|  |_|")
    time.sleep(1)



def erase():
    os.system('cls' if os.name == 'nt' else 'clear')

def titleNmenu():
    print("=========================================")
    print("Cisco NX-API Menu :")
    print("1. Read")
    print("2. Create")
    print("3. Delete")
    print("4. Exit")
    print("=========================================\n")

def subMenu1():
    print("=========================================")
    print("Interface Brief Menu :")
    print("1. Show All")
    print("2. Show VLan-name")
    print("3. Show Vlan-id")
    print("4. Hitung jumlah vlan")
    print("5. Exit")
    print("=========================================\n")

def login():
    global token
    url = "https://sbx-nxos-mgmt.cisco.com:443/api/aaaLogin.json"
    headers = {
        'Content-Type': 'text/plain'
    }

    payload = {
        "aaaUser": {
            "attributes": {
                "name": f"{switchuser}",
                "pwd": f"{switchpassword}"
            }
        }
    }

    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    response.raise_for_status()

    data = response.json()
    token = data['imdata'][0]['aaaLogin']['attributes']['token']

def readAll():
    url = "https://sbx-nxos-mgmt.cisco.com/ins"
    myheaders = {"content-type": "application/json"}
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show vlan brief",
            "output_format": "json",
        }
    }
    response = requests.post( 
        url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
    ).json()

    vlan_list = response["ins_api"]["outputs"]["output"]["body"][
        "TABLE_vlanbriefxbrief"
    ]["ROW_vlanbriefxbrief"]

    for vlan in vlan_list:
        print("Vlan Id : {}".format(vlan["vlanshowbr-vlanid"]))
        print("Vlan Status : {}".format(vlan["vlanshowbr-vlanstate"]))
        print("Vlan Name : {}".format(vlan["vlanshowbr-vlanname"]))
        print()

def readName():
    url = "https://sbx-nxos-mgmt.cisco.com/ins"
    myheaders = {"content-type": "application/json"}
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show vlan brief",
            "output_format": "json",
        }
    }
    response = requests.post( 
        url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
    ).json()

    vlan_list = response["ins_api"]["outputs"]["output"]["body"][
        "TABLE_vlanbriefxbrief"
    ]["ROW_vlanbriefxbrief"]

    for vlan in vlan_list:
        print("Vlan Name : {}".format(vlan["vlanshowbr-vlanname"]))
        print()

def readId():
    url = "https://sbx-nxos-mgmt.cisco.com/ins"
    myheaders = {"content-type": "application/json"}
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show vlan brief",
            "output_format": "json",
        }
    }
    response = requests.post( 
        url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
    ).json()

    vlan_list = response["ins_api"]["outputs"]["output"]["body"][
        "TABLE_vlanbriefxbrief"
    ]["ROW_vlanbriefxbrief"]

    for vlan in vlan_list:
        print("Vlan Id : {}".format(vlan["vlanshowbr-vlanid"]))
        print()

def countVlan():
    url = "https://sbx-nxos-mgmt.cisco.com/ins"
    myheaders = {"content-type": "application/json"}
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show vlan brief",
            "output_format": "json",
        }
    }
    response = requests.post( 
        url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
    ).json()

    vlan_list = response["ins_api"]["outputs"]["output"]["body"][
        "TABLE_vlanbriefxbrief"
    ]["ROW_vlanbriefxbrief"]

    count=0
    for vlan in vlan_list:
        count+=1

    print("Total Vlan : "+ str(count))

def post(no, name):
    url = f"https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/bd/bd-[vlan-{no}].json"
    headers = {
        'Content-Type': 'application/json', 
        'Cookie': f'APIC-cookie={token}'
    }
    payload = {
        "l2BD": {
            "attributes": {
                "fabEncap": f"vlan-{no}",
                "name": name
            }
        }
    }

    response = requests.request("POST", url, headers=headers, json=payload, verify=False)

    print(response.text)

def delete(no):
    url=f"https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/bd/bd-[vlan-{no}].json"
    headers = {
    'Cookie': f'APIC-cookie={token}'
    }
    payload = ""

    response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

    print(response.text)

def get_valid_int(prompt): 
    while True: 
        try: 
            return int(input(prompt)) 
        except ValueError: 
            print("Invalid input. Please enter a valid number.")

welcome_animation()

while True:
    login()

    erase()
    titleNmenu()
    choice = get_valid_int("Enter your choice : ")
    print("=========================================\n")

    if choice == 1:
        while True:
            subMenu1()
            choice2 = get_valid_int("Enter your choice : ")
            if choice2 == 1:
                readAll()
            elif choice2 == 2:
                readName()

            elif choice2 == 3:
                readId()

            elif choice2 == 4:
                countVlan()

            elif choice2 == 5:
                input("Press Enter to continue...")
                break;

    elif choice == 2:
        id = int(input("Masukkan id : "))
        nama = str(input("Masukkan name : "))
        post(id, nama)
        input("Press Enter to continue...")

    elif choice == 3:
        id = int(input("Masukkan id : "))
        delete(id)
        input("Press Enter to continue...")

    elif choice == 4:
        goodbye_animation()
        input("Press Enter to continue...")
        break;
    
    else:
        print("Invalid choice. Please try again.")
        input("Press Enter to continue...")






#before animated
# import requests
# import json
# import os

# requests.packages.urllib3.disable_warnings(
#     requests.packages.urllib3.exceptions.InsecureRequestWarning
# )

# switchuser = "admin"
# switchpassword = "Admin_1234!"
# token = ""

# def erase():
#     os.system('cls' if os.name == 'nt' else 'clear')

# def titleNmenu():
#     print("=========================================")
#     print("Cisco NX-API Menu :")
#     print("1. Read")
#     print("2. Create")
#     print("3. Delete")
#     print("4. Exit")
#     print("=========================================\n")

# def subMenu1():
#     print("=========================================")
#     print("Interface Brief Menu :")
#     print("1. Show All")
#     print("2. Show VLan-name")
#     print("3. Show Vlan-id")
#     print("4. Hitung jumlah vlan")
#     print("5. Exit")
#     print("=========================================\n")

# def login():
#     global token
#     url = "https://sbx-nxos-mgmt.cisco.com:443/api/aaaLogin.json"
#     headers = {
#         'Content-Type': 'text/plain'
#     }

#     payload = {
#         "aaaUser": {
#             "attributes": {
#                 "name": f"{switchuser}",
#                 "pwd": f"{switchpassword}"
#             }
#         }
#     }

#     response = requests.request("POST", url, headers=headers, json=payload, verify=False)
#     response.raise_for_status()

#     data = response.json()
#     token = data['imdata'][0]['aaaLogin']['attributes']['token']

# def readAll():
#     url = "https://sbx-nxos-mgmt.cisco.com/ins"
#     myheaders = {"content-type": "application/json"}
#     payload = {
#         "ins_api": {
#             "version": "1.0",
#             "type": "cli_show",
#             "chunk": "0",
#             "sid": "1",
#             "input": "show vlan brief",
#             "output_format": "json",
#         }
#     }
#     response = requests.post( 
#         url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
#     ).json()

#     vlan_list = response["ins_api"]["outputs"]["output"]["body"][
#         "TABLE_vlanbriefxbrief"
#     ]["ROW_vlanbriefxbrief"]

#     for vlan in vlan_list:
#         print("Vlan Id : {}".format(vlan["vlanshowbr-vlanid"]))
#         print("Vlan Status : {}".format(vlan["vlanshowbr-vlanstate"]))
#         print("Vlan Name : {}".format(vlan["vlanshowbr-vlanname"]))
#         print()

# def readName():
#     url = "https://sbx-nxos-mgmt.cisco.com/ins"
#     myheaders = {"content-type": "application/json"}
#     payload = {
#         "ins_api": {
#             "version": "1.0",
#             "type": "cli_show",
#             "chunk": "0",
#             "sid": "1",
#             "input": "show vlan brief",
#             "output_format": "json",
#         }
#     }
#     response = requests.post( 
#         url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
#     ).json()

#     vlan_list = response["ins_api"]["outputs"]["output"]["body"][
#         "TABLE_vlanbriefxbrief"
#     ]["ROW_vlanbriefxbrief"]

#     for vlan in vlan_list:
#         print("Vlan Name : {}".format(vlan["vlanshowbr-vlanname"]))
#         print()

# def readId():
#     url = "https://sbx-nxos-mgmt.cisco.com/ins"
#     myheaders = {"content-type": "application/json"}
#     payload = {
#         "ins_api": {
#             "version": "1.0",
#             "type": "cli_show",
#             "chunk": "0",
#             "sid": "1",
#             "input": "show vlan brief",
#             "output_format": "json",
#         }
#     }
#     response = requests.post( 
#         url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
#     ).json()

#     vlan_list = response["ins_api"]["outputs"]["output"]["body"][
#         "TABLE_vlanbriefxbrief"
#     ]["ROW_vlanbriefxbrief"]

#     for vlan in vlan_list:
#         print("Vlan Id : {}".format(vlan["vlanshowbr-vlanid"]))
#         print()

# def countVlan():
#     url = "https://sbx-nxos-mgmt.cisco.com/ins"
#     myheaders = {"content-type": "application/json"}
#     payload = {
#         "ins_api": {
#             "version": "1.0",
#             "type": "cli_show",
#             "chunk": "0",
#             "sid": "1",
#             "input": "show vlan brief",
#             "output_format": "json",
#         }
#     }
#     response = requests.post( 
#         url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword), verify=False,
#     ).json()

#     vlan_list = response["ins_api"]["outputs"]["output"]["body"][
#         "TABLE_vlanbriefxbrief"
#     ]["ROW_vlanbriefxbrief"]

#     count=0
#     for vlan in vlan_list:
#         count+=1

#     print("Total Vlan : "+ str(count))

# def post(no, name):
#     url = f"https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/bd/bd-[vlan-{no}].json"
#     headers = {
#         'Content-Type': 'application/json', 
#         'Cookie': f'APIC-cookie={token}'
#     }
#     payload = {
#         "l2BD": {
#             "attributes": {
#                 "fabEncap": f"vlan-{no}",
#                 "name": name
#             }
#         }
#     }

#     response = requests.request("POST", url, headers=headers, json=payload, verify=False)

#     print(response.text)

# def delete(no):
#     url=f"https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/bd/bd-[vlan-{no}].json"
#     headers = {
#     'Cookie': f'APIC-cookie={token}'
#     }
#     payload = ""

#     response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

#     print(response.text)

# def get_valid_int(prompt): 
#     while True: 
#         try: 
#             return int(input(prompt)) 
#         except ValueError: 
#             print("Invalid input. Please enter a valid number.")


# while True:
#     login()

#     erase()
#     titleNmenu()
#     choice = get_valid_int("Enter your choice : ")
#     print("=========================================\n")

#     if choice == 1:
#         while True:
#             subMenu1()
#             choice2 = get_valid_int("Enter your choice : ")
#             if choice2 == 1:
#                 readAll()
#             elif choice2 == 2:
#                 readName()

#             elif choice2 == 3:
#                 readId()

#             elif choice2 == 4:
#                 countVlan()

#             elif choice2 == 5:
#                 input("Press Enter to continue...")
#                 break;

#     elif choice == 2:
#         id = int(input("Masukkan id : "))
#         nama = str(input("Masukkan name : "))
#         post(id, nama)
#         input("Press Enter to continue...")

#     elif choice == 3:
#         id = int(input("Masukkan id : "))
#         delete(id)
#         input("Press Enter to continue...")

#     elif choice == 4:
#         input("Press Enter to continue...")
#         break;
    
#     else: 
#         print("Invalid choice. Please try again.")
#         input("Press Enter to continue...")
