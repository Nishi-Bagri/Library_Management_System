TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": (
                "Search books in the library by title."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Book title to search."
                    }
                },
                "required": ["query"]
            }
        }
    },   

    {
        "type": "function",
        "function": {
            "name": "available_books",
            "description": "List all books currently available in the library.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_by_author",
            "description": "Search books by author name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "author": {
                        "type": "string",
                        "description": "Author name to search."
                    }
                },
                "required": ["author"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_by_category",
            "description": "Search books by category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name to search."
                    }
                },
                "required": ["category"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "book_details",
            "description": "Get complete details of a specific book.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Exact title of the book."
                    }
                },
                "required": ["title"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "library_information",
            "description": (
                "Answer questions about library policies, borrowing rules, "
                "renewal policy, fine policy, library timings, contact "
                "information and password reset."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": (
                            "The library topic requested by the user. "
                            "Examples: fine, borrow, renew, timings, "
                            "contact, password."
                    )
                }
            },
            "required": ["topic"]
            }
        }
    }, 
    {
        "type": "function",
        "function": {
            "name": "recommend_books",
            "description": (
                "Recommend available books based on a category."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": (
                            "Book category for recommendations."
                        )
                    }
                },
                "required": ["category"]
            }
        }
    },
]