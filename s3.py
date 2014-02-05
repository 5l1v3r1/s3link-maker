import boto
import boto.s3.connection
from boto.s3.key import Key
import sys
#import shortuuid
import tinyurl

access_key = 'AKIAJWEFINSQCVLNH6PA'
secret_key = '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'


conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 's3-eu-west-1.amazonaws.com',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

for bucket in conn.get_all_buckets():
	print "{name}\t{created}".format(
	name = bucket.name,
	created = bucket.creation_date,
        )

bucket = conn.get_bucket('2st-store')

rs = bucket.list()
for key in rs:
	print key.name

encrypt_key = bucket.get_key('960458045308-aws-billing-csv-2013-12.csv')
encrypt_url = encrypt_key.generate_url(300, query_auth=True, force_http=True)
#print encrypt_url

u = tinyurl.create_one(encrypt_url)
print u 
#bucket = ('2st-store')

#bucket = conn.get_bucket('s3-eu-west-1.amazonaws.com/2st-store')

#for key in bucket.list():
#	print "{name}\t{size}\t{modified}".format(
#	name = key.name,
#	size = key.size,
#	modified = key.last_modified,
 #    	)


#bucket = conn.get_bucket()
#bucket_entries = bucket.list(prefix='2st-store')

#for entry in bucket_entries:
 #   print entry
