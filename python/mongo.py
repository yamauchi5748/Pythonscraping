import pymongo

class Mongo():
    
    def __init__(self, ip, port, db_name, collection_name):
        #mongodb へのアクセスを確立
        client = pymongo.MongoClient(ip, port)

        # データベースを作成
        db = client[db_name]

        # コレクションを作成
        self.co = db[collection_name]

    def insert(self, model):
        self.co.insert_many(model)



