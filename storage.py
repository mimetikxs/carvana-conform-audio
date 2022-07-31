import boto3
from botocore.errorfactory import ClientError

class Storage:
    def __init__(self, bucket, force_upload):
       self.bucket = bucket
       self.s3 = boto3.client('s3')
       self.force_upload = force_upload

    
    def check_bucket(self):
        response = self.s3.list_buckets()
        print(f"Checking bucket: {self.bucket}", end = " ")
        for b in response['Buckets']:
            if b['Name'] == self.bucket:
                print("[OK]")
                return True

        print("[FAIL]")
        return False


    def upload_file(self, file_name, object_name):
        try:
            if not(self.force_upload) and self.exists(object_name):
                print("[SKIP]")
                return False

            self.s3.upload_file(file_name, self.bucket, object_name)
            print("[OK]")
        except Exception as e:
            print("[FAIL]")
            raise RuntimeError(e)
        return True

    def download_file(self, object_name, file_name):  
        try:
            self.s3.download_file(self.bucket, object_name, file_name)
            print("[OK]")
        except Exception as e:
            print("[FAIL]")
            return False
        return True

    def exists(self, object_name):
        try:
            res = self.s3.head_object(Bucket=self.bucket, Key=object_name)
        except ClientError:
            return False
        return True