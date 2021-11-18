0. Run flask db init
Alembic maintains a migration repository. This command create a repo to manage every related to database migrations

1. Run flask db migrate
It  populates the migration script with the changes necessary to make the database schema match the application models

2. Run flask db upgrade
This applies the migration to the actual database





Notes:
1) when deploy, make a unique secret key
2）for google login for it to work locally
export OAUTHLIB_RELAX_TOKEN_SCOPE = 1
export OAUTHLIB_INSECURE_TRANSPORT=1
 





Questions:
ProfileResource: """TO-DO: might need to check if the info being passed in empty"""
Routes.py: register """TO-DO: check colloquial_name name as well"""
    1) Should we include colloquial_name name or just username?
    2) Endpoint "/profile/<id>" would it make sense not to use ID but username etc