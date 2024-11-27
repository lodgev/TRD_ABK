db = connect("mongodb://localhost:27017/admin");


db = db.getSiblingDB("trd_database");


db.users.insertMany([
{
    _id: "f928c455-d2f3-4e30-bf58-178ae041e8c2",
    firstname: "John",
    lastname: "Doe",
    email: "john@doe.com",
    password: "$2y$10$3pJS/zU.28UtbDYMo/piHOQ3rGTp3Fa7eCx0teSw2cdSmnwzwzPi6"
}
]);


db.tasks.insertMany([
{
    _id: 7,
    content: "Faire du sport",
    createdAt: "18:43:54.669",
    completedAt: null,
    completed: false,
    updatedAt: null,
    user_id: "f928c455-d2f3-4e30-bf58-178ae041e8c2"
}
]);
