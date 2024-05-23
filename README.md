## Instruction

0. Set up pyenv and pipenv with python 3.12.0
1. `pipenv shell`
2. `pipenv install`
3. Launch SMTP server to test email feature
- `python3 smtp_server.py`
- You can see the confirmation email is printed in this console when you submit a new lead
4. `fastapi run`

## Test

### Preparation
0. Setup MongoDB
- database: alma
- collections: users, leads
- If your MongoDB has different url than `mongodb://localhost:27017`, you need to specify it in `.env`
- Here is a sample `.env`
```
ADMIN_EMAIL_ADDRESS=admin@alma.com
ATTORNEY_EMAIL_ADDRESS=attorney@alma.com
SECRET_KEY=W@ueKuV+diK]M|%*7nzzhm+Ap4N&uBz!%.,lDPwbho[Ut/:ZjNVHRl/<DKU#4s!
DATABASE_URL=mongodb://localhost:27017
SMTP_URL=localhost
SMTP_PORT=8025
```
1. Signup to test Auth
- In Postman, `POST http://127.0.0.1:8000/signup`
- In Body, set form-data with following format
```
username:test@email.com
password:random_password
```

2. Get token to test Auth
- In Postman, `POST http://127.0.0.1:8000/token`
- In Body, set form-data with the same credential when you signed up above.
- Then you will get the token as follows
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHRvcm5leV9ncm91cEBhbG1hLmNvbSIsImV4cCI6MTcxNjQ0Mjg5Mn0.hQX0pL5saaWrXOcbw2j0eVQuDup59kGGMdoQUXlBM20",
    "token_type": "bearer"
}
```


### How to test "Creating a lead"
- In Postman, `POST http://127.0.0.1:8000/submit_lead`
- In Body, set form-data with following format
```
first_name:John
last_name:Doe
email:test@email.com
resume:Fullstack engineer
```
- When you submit the request, you can see the email request is printed on SMTP server you launched above 
- Here is a sample message printed
```
Message data:
 Content-Type: multipart/mixed; boundary="===============7219657247909981784=="
MIME-Version: 1.0
From: admin@alma.com
To: test@email.com, attorney@alma.com
Subject: Lead Submission Confirmation

--===============7219657247909981784==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Dear John,

Thank you for submitting your form.

First name: John
Last name: Doe
email: test@email.com
Resume/CV: Fullstack engineer

Sincerely,
The Alma Team
--===============7219657247909981784==--
```

### How to test `Getting leads`
- In Postman, `GET http://127.0.0.1:8000/get_leads`
- In Authorization, select Bearer Token as Auth Type.
- Set Token with the one you got above
- Here is a sample response. You need `_id` for the next test 
```
{
    "leads": [
        {
            "_id": "664e155425407fc84f3ecf1a",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@email.com",
            "resume": "Fullstack engineer"
        },
```


### How to test `Updating state of lead`
- In Postman, `PUT http://127.0.0.1:8000/reach_out/664e155425407fc84f3ecf1a`
- In Authorization, select Bearer Token as Auth Type.
- Set Token with the one you got above
- Make sure you put the `_id` you got above into the url
- Here is a sample response
```
{
    "message": "Lead 664eba5ae23803add29056cd marked as REACHED_OUT"
}
```