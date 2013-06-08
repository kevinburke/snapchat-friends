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
    "Links": [
        {Source: 123, Target: 224},
        {Source: 123, Target: 225},
        ...
    ],
    "Users": [
        {
            Name: "bobby",
            Id: 123,
            Score: 30444
        },
        ...
    ]
}
