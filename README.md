# News_Board_Service

is an application that is used to provide announcements on mobile applications / websites. In this service we can make announcements. In the announcement sometimes there are several files that can be given as additional files / attachments. We can also edit the news and download files of the news

## Requests

1. Login
2. Logout
3. Get All News
4. Get News by ID
5. Download File By ID
6. Add News
7. Edit News (Edit News Content)
8. Edit News (Add Files in News)
9. Edit News (Delete File)
10. Delete News

### Request #1: Login

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/login**</span>

```json
{
  "username": "janeDoe",
  "password": "QchpCEKOIsVhOXVj"
}
```

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Login Success!"
}
```

#### Username and Password not found/ defined

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Your Username and Password are Not Defined"
}
```

<br>

### Request #2: Logout

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/logout**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Logged out successfully!"
}
```

<br>

### Request #3: Get All News

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/news**</span>

#### Responses:

#### Success

```json
{
  "status": "success",
  "data": [
    {
      "id_news": 3,
      "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
      "files": [
        {
          "id_file": 17,
          "filename": "-509922067_RangkaianListrik.pdf"
        }
      ]
    },
    {
      "id_news": 4,
      "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
      "files": [
        {
          "id_file": 15,
          "filename": "-755999555_RangkaianListrik.pdf"
        },
        {
          "id_file": 20,
          "filename": "-1984285980.pdf"
        }
      ]
    }
  ]
}
```

#### No News Available

```json
{
  "status": "error",
  "message": "There are still no news"
}
```

<br>

### Request #4: Get News by ID

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/news/`<int:news_id>`**</span>

#### Responses:

#### Success

```json
{
    "status": "success",
    "id_news": 1,
    "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
    "files": [
        {
            "id_file": 17,
            "filename": "509922067.pdf",
        }
        {
            "id_file": 18,
            "filename": "reportingTest.pdf"
        }

        }
    ]
}
```

#### News with `<int:news_id>` Not Found || Has been deleted || Has Been Archived

```json
{
  "status": "error",
  "message": "News not found"
}
```

<br>

### Request #5: Download File By ID

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/file/`<int:file_id>`**</span>

#### Responses:

#### Success

#### File with `<int:file_id>` Not Found || Has been deleted

```json
{
  "status": "error",
  "message": "News not found"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

<br>

### Request #6: Add News

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/news/add**</span>

Form-Data

1. type = text --> key = content
2. type = file --> key = file (can be multiple)

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "News added successfully!"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

#### There are news with the same content

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Create new content!!"
}
```

<br>

### Request #7: Edit News (Edit News Content)

![PUT](https://badgen.net/badge/Method/PUT/blue)<span style="padding:10px">**/news/edit/content/`<int:news_id>`**</span>

#### Responses:

#### Success

```json
{
  "status": "success",
  "message": "Content edited successfully"
}
```

#### News with `<int:news_id>` Not Found || Has been deleted || Has Been Archived

```json
{
  "status": "error",
  "message": "News not found"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

<br>

### Request #8: Edit News (Add Files in News)

![PUT](https://badgen.net/badge/Method/PUT/blue)<span style="padding:10px">**/news/add/files/`<int:news_id>`**</span>

#### Responses:

#### Success

```json
{
  "status": "success",
  "message": "Files added to news successfully! "
}
```

#### News with `<int:news_id>` Not Found || Has been deleted || Has Been Archived

```json
{
  "status": "error",
  "message": "News not found"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

<br>

### Request #9: Edit News (Delete File)

![DELETE](https://badgen.net/badge/Method/DELETE/red)<span style="padding:10px">**/file/`<int:file_id>`**</span>

#### Responses:

#### Success

```json
{
  "status": "error",
  "message": "News deleted successfully"
}
```

#### News with `<int:news_id>` Not Found || Has been deleted || Has Been Archived

```json
{
  "status": "error",
  "message": "News not found"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

<br>

### Request #10: Delete News

![DELETE](https://badgen.net/badge/Method/DELETE/red)<span style="padding:10px">**/news/`<int:news_id>`**</span>
<br>

#### Responses:

#### Success

```json
{
  "status": "success",
  "message": "File deleted successfully"
}
```

#### News with `<int:news_id>` Not Found || Has been deleted || Has Been Archived

```json
{
  "status": "error",
  "message": "News not found"
}
```
