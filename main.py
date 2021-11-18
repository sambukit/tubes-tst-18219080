import json
from fastapi import FastAPI,HTTPException,Body,Depends
from auth.auth_handler import signJWT, get_password_hash, verify_password
from auth.auth_bearer import JWTBearer

with open("database.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()
app.currentUID = 0

# New user signup (not included)
# @app.post('/user')
# async def new_user(username: str, password: str):
#     hashed_password = get_password_hash(password)
#     with open("user.json", "r") as read_user_file:
#         user_data = json.load(read_user_file)
#     user_id = len(user_data)+1
#     newdata = {'userID': user_id, 'username': username, 'password' : hashed_password}
#     user_data.append(newdata)
#     with open("user.json", "w") as write_user_file:
#         json.dump(user_data, write_user_file)
#     write_user_file.close()
#     return signJWT(username)

@app.get('/readme')
async def readme():
    return {"message": "Terdapat dua user yang bisa dipakai. 1. username: abcd | password: abcd 2. username: username | password: password "}

@app.post('/login')
async def user_login(username: str, password: str):
    tempUID = 0
    db_password = "abc"
    with open("user.json", "r") as read_user_file:
        user_data = json.load(read_user_file)
    for user in user_data:
        if user['username'] == username:
            tempUID = user['userID']
            db_password = user['password']
    if db_password != "abc":
        if verify_password(password, db_password):
            app.currentUID = tempUID
            return signJWT(username)
        else:
            return("Login gagal karena kesalahan username atau password")
    else:
        return("Login gagal karena kesalahan username atau password")

@app.get('/forum/p/{forum_id}', dependencies=[Depends(JWTBearer())])
async def read_forum(forum_id: int):
    output = []
    for item in data['forum']:
        if item['forumID'] == forum_id:
            outdata={'Title': item['title'], 'Discussion' : item['discussion']}
            print(outdata)
            output.append(outdata)
            for reply in data['reply']:
                if reply['forumID'] == forum_id:
                    outdata={'From': reply['userID'], 'Message' : reply['message']}
                    print(outdata)
                    output.append(outdata)
            return output

    raise HTTPException(
        status_code=404, detail=f'Forum with specified ID not found'
    )

@app.post('/forum/p/{forum_id}', dependencies=[Depends(JWTBearer())])
async def reply_forum(message: str, forum_id: int):
    reply_id = len(data['reply'])+1
    newdata = {'replyID': reply_id, 'userID' : app.currentUID, 'message' : message, 'forumID': forum_id}
    if(reply_id >= 1):
        data['reply'].append(newdata)
        with open("database.json", "w") as write_file:
            json.dump(data, write_file)
        write_file.close()
        return newdata
        
@app.put('/forum/p/{forum_id}', dependencies=[Depends(JWTBearer())])
async def update_forum(forum_id: int, new_title: str, new_discussion: str):
    for item in data['forum']:
        if item['forumID'] == forum_id:
            if item['userID'] == app.currentUID:
                item['title'] = new_title
                item['discussion'] = new_discussion
                read_file.close()    
                with open("database.json", "w") as write_file:
                    json.dump(data, write_file)
                write_file.close()
                return {'message':'Data changed successfully'}
    raise HTTPException(
        status_code=403, detail=f'You are not the author of this post or post is not found'
    )
    

@app.delete('/forum/p/{forum_id}', dependencies=[Depends(JWTBearer())])
async def delete_forum(forum_id: int):
    for item in data['forum']:
        if item['forumID'] == forum_id:
            if item['userID'] == app.currentUID:
                data['forum'].remove(item)
                read_file.close()    
                with open("database.json", "w") as write_file:
                    json.dump(data, write_file)
                write_file.close()
                return {'message':'Data deleted successfully'}
    raise HTTPException(
        status_code=403, detail=f'You are not the author of this post'
    )
    
@app.get('/catalog', dependencies=[Depends(JWTBearer())])
async def read_catalog():
    output = []
    for item in data['catalog']:
        outdata={'name': item['name'], 'images' : item['images'], 'price' : item['price']}
        print(outdata)
        output.append(outdata)
    return output

@app.get('/catalog/{catalog_id}', dependencies=[Depends(JWTBearer())])
async def product_details(catalog_id: int):
    for item in data['catalog']:
        if item['itemID'] == catalog_id:
            return {'Name' : item['name'], 'Images': item['images'], 'Price':item['price'], 'Description': item['desc'], 'Available Size':item['size'], 'Link':item['redirectLink']}
    raise HTTPException(
        status_code=404, detail=f'Product with specified ID not found'
    )