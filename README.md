This project is a GUI based autotagger which uses Microsoft azure cognitive services face api to identify a person in a given picture.

Subscription key needs to be changed in all the scripts.

Scripts to be run in this order:

1. Run add_group_and_person.py. This script will return a GroupID which will be used to run other scripts.
2. Run add_and_train_faces.py by providing GroupID as a argument.
3. Run Autotagger.py by providing GroupID as a argument.