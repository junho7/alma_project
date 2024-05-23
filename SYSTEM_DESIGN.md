1. Database
- I chose MondoDB. The schema-less nature of MongoDB provides flexibility, especially when dealing with potentially evolving data structures like lead information. MongoDB's scalability is also a benefit if you expect a large number of leads.
- Database has two collections for consistency and clarity. One for leads and the other for users.

2. Auth
- I use JWT for authentication. Because JWT is a standard for secure token-based authentication.
- Used hashed password for enhanced security.

3. API
- Endpoints are split into two routers, users and leads. It's consistent to Model structure.
- App module has models, routers, and utils submodules. Well-organized folder structure helps collaboration and maintenance easier.