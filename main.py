import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to 
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "porter-planner-firebase-adminsdk-wvwwg-cd7d5d21e2.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.Certificate("porter-planner-firebase-adminsdk-wvwwg-cd7d5d21e2.json")
    firebase_admin.initialize_app(cred)

    # Get reference to database
    db = firestore.client()
    return db

def add_new_dino(db):
    '''
    Prompt the user for a new item to add to the inventory database.  The
    item name must be unique (firestore document id).  
    '''
    while True:
        collection = input("Herbivore or Carnivore: ")
        if collection == "Herbivore" or collection == "Carnivore":
            break

        print(f"\n{collection} is not an option, please try again.")

    name = input("Dinosaur: ")

    try: size = float(input("New Size (feet): "))
    except:
        print("You need to type in a number.\n")
        add_new_dino(db)
    
    try:
        weight = float(input("New Weight (tons): "))
    except:
        print("You need to type in a number.\n")
        add_new_dino(db)

    # Check for an already existing Dino by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection(collection).document(name).get()
    if result.exists:
        print("Item already exists.")
        return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"Size" : size,
            "Weight" : weight}
    db.collection(collection).document(name).set(data) 

def update_dino(db):
    '''
    Prompt the user to add quantity to an already existing item in the
    inventory database.  
    '''
    while True:
        collection = input("Herbivore or Carnivore: ")
        if collection == "Herbivore" or collection == "Carnivore":
            break

        print(f"\n{collection} is not an option, please try again.")

    name = input("Dinosaur: ")

    try: new_size = float(input("New Size (feet): "))
    except:
        print("You need to type in a number.\n")
        update_dino(db)
    
    try:
        new_weight = float(input("New Weight (tons): "))
    except:
        print("You need to type in a number.\n")
        update_dino(db)

    # Check for an already existing Dino by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection(collection).document(name).get()
    if not result.exists:
        print("Invalid Dinosaur")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new size and weight and then save the 
    # updated dictionary to Firestore.
    data["Size"] = new_size
    data["Weight"] = new_weight
    db.collection(collection).document(name).set(data)

def search_dinos(db):
    '''
    Search the database in multiple ways.
    '''

    print("Select Query")
    print("1) Show All Dinosaurs")        
    print("2) Show Big Dinosaurs")
    print("3) Show Small Dinosaurs")
    choice = input("> ")
    while True:
        collection = input("Herbivore or Carnivore: ")
        if collection == "Herbivore" or collection == "Carnivore":
            break

        print(f"\n{collection} is not an option, please try again.")

    print()

    #     results = db.collection(collection).where("popular","==",True). \
    #                                          where("qty","<=", 5).get()

    if choice == "1":
        results = db.collection(collection).get()
    elif choice == "2":
        results = db.collection(collection).where("Weight",">=",2).get()
    elif choice == "3":
        results = db.collection(collection).where("Weight", "<",2).get()
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    print("")
    print("Search Results")
    print(f"{'Name':<20}  {'Size (feet)':<10}  {'Weight (tons)':<10}")
    for result in results:
        item = result.to_dict()
        print(f"{result.id:<20}  {item['Size']:<10}  {item['Weight']:<10}")
    print()   

def delete_dino(db):
    while True:
        collection = input("Herbivore or Carnivore: ")
        if collection == "Herbivore" or collection == "Carnivore":
            break

        print(f"\n{collection} is not an option, please try again.")

    name = input("Dinosaur to be deleted: ")
    db.collection(collection).document(name).delete()

def main():
    db = initialize_firestore()
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New Dinosaur")
        print("2) Update Dinosaur")
        print("3) Search Dinosaurs")
        print("4) Delete Dinosaur")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_dino(db)
        elif choice == "2":
            update_dino(db)
        elif choice == "3":
            search_dinos(db)       
        elif choice == "4":
            delete_dino(db)                     

if __name__ == "__main__":
    main()
