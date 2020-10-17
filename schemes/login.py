post = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["email", "password"]
}

put = {
    "type": "object",
    "properties": {
        "password": {"type": "string"}
    },
    "required": ["password"]
}
