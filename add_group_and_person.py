import create_person_group
import add_person_to_group


if __name__ == '__main__':

    persongroupID, GroupName = create_person_group.Group_create()

    print("Person group ID: {0}".format(persongroupID))
    while(True):

        add_person_to_group.add_person(persongroupID)

        user_input = input("Do you want to add another person? y or n")

        if user_input == "n":
            break
