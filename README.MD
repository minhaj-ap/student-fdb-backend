there are 2 models, user and feedback.

USER Flow:

- USER login to his account
- If no account create one and pass jwt with refresh and access token
- Allow user to create, read, edit and delete his feedback
- Feedbacks are selcted with user_id with the user.id
- A feedback will contain subject (text) category (text with dropdwon) message (text), rating (integer from 1 to 5).
- Whille creating a feedback an id , timestamp and the user id and status set to pending should also be kept.
- While editing a feedback the status should be setted to pending again if changed also the user id validates to allow edit
- Categories are hardcoded into ['academics','infrastructure','extra-curricular activities']

ADMIN Flow:

- ADMIN login to his account where validation is is_staff = True
- Able to modify the status of feedbakcs.
- Status options are hardcoded to ['pending','reviewed','resolved']

AUTH

- Admin created form terminal as super user with 
name:admin
email:admin@gmail.com
passowrd:admin

- User are created with username and password
- 2 tokens are passed refresh and access token with user details
- if admin is_staff will be true  for front end validation