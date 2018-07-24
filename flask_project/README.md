### set up database on aws

1. create a postgresql on AWS RDS.
2. create a file .aws.dev.env and edit the DATABASE_URL
```
export APP_SETTINGS=DevelopmentConfig
export DATABASE_URL=postgres://<user>:<password>@<url>/<database_name>
```
3. make create-devawsdb