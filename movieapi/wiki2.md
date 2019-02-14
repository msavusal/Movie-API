|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|Name of the attribute|Attribute type|Values that the type can take|Description of the attribute|Uniqueness, default...| keys and foreign keys|
|id|integer||Integer number||UNIQUE|
|user_id|integer||User ID key||UNIQUE|
|movie_id|integer||Movie ID key||UNIQUE|
|text|text(400)||Text up to 400||UNIQUE|
|timestamp|string(30)||String of characters (max display size 30)||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|
|category_id|integer||Category ID Key||UNIQUE|
|password|string(200)||String of characters (max display size 200)||UNIQUE|
|email|string(100)||E-mail address||UNIQUE|
|rating|integer||Integer between 1 and 10||UNIQUE|
|length|string||HH:MM:SS||UNIQUE|
|actor_id|integer||Actor ID key||UNIQUE|
|video_path|text(500)||Text url path of video||UNIQUE|
|isAdmin|binary||Admin ID||UNIQUE|
|name|string(100)||User name||UNIQUE|

**Comment**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|user_id|integer||User ID key||UNIQUE|
|movie_id|integer||Movie ID key||UNIQUE|
|text|text(400)||Text up to 400||UNIQUE|
|timestamp|string(30)||String of characters (max display size 30)||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|

**MovieCategory**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|movie_id|integer||Movie ID key||UNIQUE|
|category_id|integer||Category ID Key||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|

**Category**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|name|string(100)||User name||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|

**User**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|name|string(100)||User name||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|

**Review**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|user_id|integer||User ID key||UNIQUE|
|movie_id|integer||Movie ID key||UNIQUE|
|text|text(400)||Text up to 400||UNIQUE|
|rating|integer||Integer between 1 and 10||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|

**Movie**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|title|string(400)||Title of Movie||UNIQUE|
|length|string||HH:MM:SS||UNIQUE|
|rating|integer||Integer between 1 and 10||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|

**UserGroup**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer||Integer number||UNIQUE|
|user_id|integer||User ID key||UNIQUE|
|group_id|integer||Group ID key||UNIQUE|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||UNIQUE|
