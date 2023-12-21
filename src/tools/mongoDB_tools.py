import pymongo
from bson import ObjectId

def object_file(file_id):
    id_file=ObjectId(file_id)
    return (id_file)


def find_file(files, file_id_object): 
    information = files.find_one({"_id":file_id_object})
    return information

def update_status(files,file_id_object,modification): 
    update = {"$set": {"status": modification}}
    resultat = files.update_one({"_id": file_id_object}, update)
    return resultat

