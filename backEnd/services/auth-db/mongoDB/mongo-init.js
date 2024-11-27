db = connect("mongodb://localhost:27017/admin");



db = db.getSiblingDB("trd_users");


db.users.insertMany([
{
    _id: "f928c455-d2f3-4e30-bf58-178ae041e8c2",
    firstname: "John",
    lastname: "Doe",
    email: "john@doe.com",
    password: "$2y$10$3pJS/zU.28UtbDYMo/piHOQ3rGTp3Fa7eCx0teSw2cdSmnwzwzPi6"
}
]);