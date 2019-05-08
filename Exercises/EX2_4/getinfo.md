### Track information [GET]

+ Relation: self
+ Request

    + Headers

            Accept: application/vnd.mason+json

+ Response 200 (application/vnd.mason+json)

    + Body

            {
                "title": "Image",
                "disc_number": 1,
                "track_number": 1,
                "length": "00:04:26",
                "artist": "Scandal",
                "@controls": {
                    "author": {
                        "href": "/api/artists/scandal/"
                    },
                    "albums-by": {
                        "href": "/api/artists/scandal/albums/"
                    },
                    "self": {
                        "href": "/api/artists/scandal/albums/Hello World/1/1/"
                    },
                    "profile": {
                        "href": "/profiles/track/"
                    },
                    "up": {
                        "href": "/api/artists/scandal/albums/Hello World/"
                    },
                    "edit": {
                        "href": "/api/artists/scandal/albums/Hello World/1/1/",
                        "title": "Edit this track",
                        "encoding": "json",
                        "method": "PUT",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "description": "Track title",
                                    "type": "string"
                                },
                                "disc_number": {
                                    "description": "Disc number",
                                    "type": "integer",
                                    "default": 1
                                },
                                "track_number": {
                                    "description": "Track number on disc",
                                    "type": "integer"
                                },
                                "length": {
                                    "description": "Track length",
                                    "type": "string",
                                    "pattern": "^[0-9]{2}:[0-5][0-9]:[0-5][0-9]$"
                                }
                            },
                            "required": ["title",
                            "track_number",
                            "length"]
                        }
                    },
                    "mumeta:delete": {
                    "href": "/api/artists/scandal/albums/Hello World/1/1/",
                    "title": "Delete this track",
                    "method": "DELETE"
                    }
                },
                "@namespaces": {
                    "mumeta": {
                    "name": "/musicmeta/link-relations#"
                    }
                }
            }

+ Response 404 (application/vnd.mason+json)

    + Body

            {
                "resource_url": "/api/artists/scandal/albums/Hello World/1/2/",
                "@error": {
                    "@message": "Track not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error-profile/"
                    }
                }
            }


### Various artists track information [GET]

+ Relation: self
+ Request

    + Headers

            Accept: application/vnd.mason+json

+ Response 200 (application/vnd.mason+json)

    + Body

            {
                "title": "Exördium",
                "disc_number": 1,
                "track_number": 1,
                "length": "00:03:00",
                "artist": "Emperor",
                "@controls": {
                    "author": {
                        "href": "/api/artists/emperor/"
                    },
                    "albums-by": {
                        "href": "/api/artists/emperor/albums/"
                    },
                    "self": {
                        "href": "/api/artists/VA/albums/Thorns vs Emperor/1/1/"
                    },
                    "profile": {
                        "href": "/profiles/track/"
                    },
                    "up": {
                        "href": "/api/artists/VA/albums/Thorns vs Emperor/"
                    },
                    "edit": {
                        "href": "/api/artists/VA/albums/Thorns vs Emperor/1/1/",
                        "title": "Edit this track",
                        "encoding": "json",
                        "method": "PUT",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "description": "Track title",
                                    "type": "string"
                                },
                                "disc_number": {
                                    "description": "Disc number",
                                    "type": "integer",
                                    "default": 1
                                },
                                "track_number": {
                                    "description": "Track number on disc",
                                    "type": "integer"
                                },
                                "length": {
                                    "description": "Track length",
                                    "type": "string",
                                    "pattern": "^[0-9]{2}:[0-5][0-9]:[0-5][0-9]$"
                                }
                            },
                            "required": ["title",
                            "track_number",
                            "length"]
                        }
                    },
                    "mumeta:delete": {
                    "href": "/api/artists/VA/albums/Thorns vs Emperor/1/1/",
                    "title": "Delete this track",
                    "method": "DELETE"
                    }
                },
                "@namespaces": {
                    "mumeta": {
                    "name": "/musicmeta/link-relations#"
                    }
                }
            }

+ Response 404 (application/vnd.mason+json)

    + Body

            {
                "resource_url": "/api/artists/VA/albums/Thorns vs Emperor/1/2/",
                "@error": {
                    "@message": "Track not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error-profile/"
                    }
                }
            }
