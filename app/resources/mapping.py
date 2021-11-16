mapping = {
    "mapping": {
    "properties" : {
        "APSC Electives" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                }
            }
        },
        "Campus" : {
            "type" : "keyword"
        },
        "Code" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
                }
            }
        },
        "Course Description" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
                }
            }
        },
        "Course Level" : {
            "type" : "long"
        },
        "Department" : {
            "type" : "keyword"
        },
        "Division" : {
            "type" : "keyword"
        },
        "Name" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
                }
            }
        },
        "Pre-requisites" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
                }
            }
        },
        "Term" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
                }
            }
        },
        "UTSC Breadth" : {
            "type" : "text",
            "fields" : {
                "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
                }
            }
        }
    }
    }
}