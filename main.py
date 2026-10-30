import sqlite3
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app=FastAPI()


conn=sqlite3.connect("Test.db",check_same_thread=False)
cursor=conn.cursor()
# cursor.execute('''
#     create table if not exists items(
#         item_id integer primary key autoincrement,
#         name text not null,
#         des text
#     )
#     ''')
# conn.commit()

class item(BaseModel):
    name:str
    des:str

@app.post("/items/create")
def create_item(i:item):
    try:
        cursor.execute("insert into items(name,des) values(?,?)",(i.name,i.des))
        conn.commit()
        return {"message":"items stored successfully...!"}
    except Exception as e:
        return HTTPException(status_code=400,detail=f"unable to store {e}")
@app.get("/items/read")
def read():
    try:
        cursor.execute("select * from items")  
        rows=cursor.fetchall()
        return [{"id":r[0],"name":r[1],"des":r[2]} for r in rows]
    except Exception as e:
            return HTTPException(status_code=400,detail=f"unable to read{e}")

@app.get("/item/readone/{name}")
def read_one(name:str):
     try:
          cursor.execute("select * from items where name=?",(name,))
          row=cursor.fetchone()
          if row is None:
             raise HTTPException(status_code=404,detail="item not found")
          return {"id":row[0],"name":row[1],"description":row[2]}
     except Exception as e:
            return HTTPException(status_code=400,detail=f"unable to read{e}")   
@app.put("/item/update/{item_id}")
def update_item(item_id:int,i:item):
     try:
          cursor.execute("update items set name=?,des=? where item_id=?",(i.name,i.des,item_id))
          conn.commit()
          return {"message":"items updated successfully...!"}
     except Exception as e:
                 return HTTPException(status_code=400,detail=f"unable to update{e}")  

@app.delete("/items/delete/{name}")
def delete_item(name:str):
     try:
          cursor.execute("Delete from items where name =?",(name,))
          conn.commit()
          return{"message":"item deleted successfully...!"}
     except Exception as e:
                      return HTTPException(status_code=400,detail=f"unable to delete{e}")  
     
