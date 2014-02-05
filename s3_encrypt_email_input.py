import boto
import boto.s3.connection
from boto.s3.key import Key
import sys
#import shortuuid
import tinyurl
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import os

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

#b = input("Enter your bucket:")

rawbucket = raw_input("Enter a bucket: ")
print rawbucket

bucket = conn.get_bucket(rawbucket)

rs = bucket.list()
for key in rs:
	print key.name

filetosend = raw_input('Enter the file you wish to send: ') 

expiredate = input ('enter expiry time in seconds\n3600 - 1hr\n900 - 15mins\n300 - 5mins\n86400 - 1day\n604800 - 7 days\n: ')

encrypt_key = bucket.get_key(filetosend)
encrypt_url = encrypt_key.generate_url(expiredate, query_auth=True, force_http=True)
#print encrypt_url

u = tinyurl.create_one(encrypt_url)
print u 

sendtoaddress = raw_input('Send file to (email): ')

msg = MIMEMultipart()
msg['From'] = 'd.m.holdaway@gmail.com'
msg['To'] = sendtoaddress
msg['Subject'] = 'your data is ready for download'
#message = "Hello, here is the link for your data %s the link will expire in 5mins." % u
#message = "%s||\n%s||\n%s" % ('hello here is your link', u ,'this link will expire in 5mins")
message = "hello,\nthis is the link for your data.\n\n%s\n \nThe link will expire in %s \nThank you" % (u,expiredate)
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.gmail.com',587)
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('d.m.holdaway@gmail.com', '3upHEf2c')

mailserver.sendmail('d.m.holdaway@gmail.com',sendtoaddress,msg.as_string())

mailserver.quit()


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
