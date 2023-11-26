# Information about authentication
All the users in the database have a `type` field, and we assume that it's mapped to different users. Keeping that in mind, we have created our very own mapping for the system and it is as follows.
| Type (or Role) | Mapped User            |
|------|------------------------|
| 1    | Labratory Assistant    |
| 2    | Labratory Researcher   |
| 3    | Accountant             |
| 4    | Administrator          |

Hence, if you need to sign in as a Labratory Assitant, you may use the `login` and `password` of any user whose `role` is equal to 1. The same goes on for the others too.
