|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|Name of the attribute|Attribute type|Values that the type can take|Description of the attribute|Uniquenes, default...| keys and foreign keys|
|id|integer||Integer number||PRIMARY KEY|
|user_id|integer||User ID key||FOREIGN KEY|
|movie_id|integer||Movie ID key||FOREIGN KEY|
|text|text(400)||Text up to 400|||
|timestamp|string(30)||String of characters (max display size 30)|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||
|category_id|integer||Category ID Key||FOREIGN KEY|
|password|string(200)|NOT NULL|String of characters (max display size 200)||
|email|string(100)|NOT NULL|E-mail address|||
|rating|integer||Integer between 1 and 10|||
|length|string||HH:MM:SS|||
|actor_id|integer||Actor ID key||FOREIGN KEY|
|video_path|text(500)||Text url path of video|||
|isAdmin|binary||Admin ID||||
