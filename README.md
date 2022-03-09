# How to See What Is Up
You can go [directly](https://www.google.com), and check out the docs. Just add /docs to the end of the url.
But as most of the API functionality requires authentication, better way is to use Postman
and add
```
pm.environment.set("jwt_token", pm.response.json().access_token) 
```
to the Tests section under {{URL}}/login
That way you are autehnicated and can create, view, like the posts and other things that require logging in


# Stuff I learned about
---
* FastAPI
* Postman, Heroku
* OAuth2 and Authenication tokens
* PosgreSQL / Sqlalchemy / Alembic
* Password hashing
* And more..
