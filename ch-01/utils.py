import oci
from ads import set_auth
import pandas as pd
import os
import re
import glob

# get the list of objects in the bucket
# works for num_objects <= 1000
# need to add pagination
def get_objects_list(namespace, bucket_name, rps):
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=rps)

    resp = object_storage.list_objects(namespace, bucket_name)

    # extract only the names
    list_files = []
    
    if len(resp.data.objects) > 0:
        for obj in resp.data.objects:
            list_files.append(obj.name)
    
    return list_files

# copy from bucket to local dir
def copy_object_from_oss(f_name, dir_name, namespace, bucket_name, rps):
    CHUNK_SIZE = 1024 * 1024
    
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=rps)
    
    get_obj = object_storage.get_object(namespace, bucket_name, f_name)
    
    path_name = dir_name + "/" + f_name
    
    with open(path_name, 'wb') as f:
        for chunk in get_obj.data.raw.stream(CHUNK_SIZE, decode_content=False):
            f.write(chunk)
            
    print(f"Copy {f_name} done!")
            
# copy a file from a local dir to a bucket of OSS
def copy_object_to_oss(f_name, dir_name, namespace, bucket_name, rps):
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=rps)
    
    path_name = dir_name + "/" + f_name
    
    with open(path_name, 'rb') as f:
        obj = object_storage.put_object(namespace, bucket_name, f_name, f)
        
    print(f"Copy {f_name} done!")

#
# massive copy
#
def copy_list_objects_from_oss(list_files, dir_name, namespace, bucket_name, rps):
    # dir_name is the local dir where to copy to
    for f_name in list_files:
        copy_object_from_oss(f_name, dir_name, namespace, bucket_name, rps)

def copy_list_objects_to_oss(list_files, dir_name, namespace, bucket_name, rps):
    for f_name in list_files:
        copy_object_to_oss(f_name, dir_name, namespace, bucket_name, rps)
