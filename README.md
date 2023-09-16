# X3T2
## Server Routes
  - GET, POST `/api/shelter`
- MyFriend: `/friend/<:username>`
  - GET, POST, DELETE `/api/friends/<string:username>`

- `/` - Home

- Login: `/api/login`
  - POST: {username, password} to login user
- Register: `/api/register` 
  - POST: {email, username, password} to create a new user
- Logout: `/api/logout`
  - DELETE: {} to logout user
- Profile: `/api/profile` (login required)
  - GET: {first_name, last_name, profile_url, city, bio} to display user/owner information
  - POST: {user_id, first_name, last_name, profile_url, city, bio} to create owner after registration
  - PATCH: {profile_url, city, bio} to edit profile information
- Friends: `/api/friends` (login required)
  - GET: {first_name, last_name, profile_url, city, bio} for viewing friends
  - POST: {username} for adding friend from existing owner
- Pets: `/api/pets` (login required)
  - GET: { name, factor, strain:{name, emoji} } for viewing pets
  - POST: { name, factor, strain:{name, emoji} } for adding new pet
- Friend: `/api/friends/<string:username>` (login required)
  - GET: {username, profile_url, first_name, last_name, bio} for viewing friend owners
  - DELETE: {} to remove friend owner
- Pet: `/api/pets/<int:id>` (login required)
  - GET: {name, factor, strain, happiness, health, hunger} to view pet
  - DELETE: {} to unadopt pet
  - PATCH: {happiness, health, hunger} to update pet
- Threads: `/api/threads`
  - GET: {friendname, }
- Shelter: `/api/shelter`
  - GET
  - POST
