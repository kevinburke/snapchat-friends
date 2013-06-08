# Server API

    GET /

Serve the homepage. unanswered questions:

- pick a user at random? 
- The most popular user? 
- Type a username to get started?


    GET /users/<username>
    Accept: */* or text/html

Draw the graph for a user

    GET /users/<username>
    Accept: prs.kevinburke.snapchat-v1+json

Sends back JSON like this:

{
    "links": [
        {source: 123, target: 224},
        {source: 123, target: 225},
        ...
    ],
    "users": [
        {
            name: "bobby",
            id: 123,
            score: 30444
        },
        ...
    ]
}
