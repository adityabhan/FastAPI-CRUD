Relationships Summary
Table	Relationship Type
Person → Department	Many-to-One
Department → Person	One-to-Many
Todo → Person	Many-to-Many (via TodoMapping)

# Initialize dev environment for non containerized development

1) Clone git repo.
2) Setup dev environment.
    python -m venv myenv
3) Install dependencies.
    pip install -r requirements.txt


# Build and run backend

docker build -t fast_api:1.0 .

docker run -it -p 8000:8000 fast_api:1.0

Go to http://localhost:8000/docs to access Swagger Documentation.

Open Points:
1) email validator for Person is not working as expected.