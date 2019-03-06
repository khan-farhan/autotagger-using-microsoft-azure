"""
Person group id needs to be provided. Run the script as "python3 add_and_train_Faces.py groupID"

"""

import add_face_to_person
import train_persongroup
import check_train_status
import sys

persongroupID = str(sys.argv[1])

if __name__ == '__main__':

    while(True):
        add_face_to_person.add_face(persongroupID)
        user_input = input("Do you want to add another person's face? y or n")
        if user_input == "n":
            break

    train_persongroup.train(persongroupID)

    check_train_status.check_status(persongroupID)
