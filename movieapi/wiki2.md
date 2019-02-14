
**Comment**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|user_id|integer|NOT NULL|User ID key|UNIQUE|FOREIGN KEY|
|movie_id|integer|NOT NULL|Movie ID key|UNIQUE|FOREIGN KEY|
|text|text(400)||Text up to 400|||
|timestamp|string(30)||String of characters (max display size 30)|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS||||

**MovieCategory**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|movie_id|integer|NOT NULL|Movie ID key|UNIQUE|FOREIGN KEY|
|category_id|integer|NOT NULL|Category ID Key|UNIQUE|FOREIGN KEY|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**Category**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|name|string(100)||Category name|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**User**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|name|string(100)||User name|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**Review**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|user_id|integer|NOT NULL|User ID key|UNIQUE|FOREIGN KEY|
|movie_id|integer|NOT NULL|Movie ID key|UNIQUE|FOREIGN KEY|
|text|text(400)||Text up to 400|||
|rating|integer||Integer between 1 and 10|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**Movie**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|title|string(400)||Title of Movie|||
|length|string||HH:MM:SS|||
|rating|integer||Integer between 1 and 10|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**UserGroup**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|user_id|integer|NOT NULL|User ID key|UNIQUE|FOREIGN KEY|
|group_id|integer|NOT NULL|Group ID key|UNIQUE|FOREIGN KEY|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**Actor**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|user_id|integer|NOT NULL|User ID key|UNIQUE|FOREIGN KEY|
|name|string(100)||Actor name|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**MovieActor**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|actor_id|integer|NOT NULL|Actor ID key|UNIQUE|FOREIGN KEY|
|movie_id|integer|NOT NULL|Movie ID key|UNIQUE|FOREIGN KEY|
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**Trailer**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|user_id|integer|NOT NULL|User ID key|UNIQUE|FOREIGN KEY|
|movie_id|integer|NOT NULL|Movie ID key|UNIQUE|FOREIGN KEY|
|video_path|text(500)||Text url path of video|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||

**Group**

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Keys and foreign keys**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|id|integer|NOT NULL|Integer number|UNIQUE|PRIMARY KEY|
|name|string(100)||Group name|||
|isAdmin|boolean|NOT NULL|Admin group true/false|||
|created|timestamp||Timestamp YYYY-MM-DD HH:MM:SS|||
