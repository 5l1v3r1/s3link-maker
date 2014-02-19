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
import zipfile
import glob
import re
#from zipfile_infolist import print_info

access_key = 'AKIAISX6KZIZPHHMPAOQ'
secret_key = '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'

# -  Zip File 
#############




# - upload to S3
################

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 's3-us-west-2.amazonaws.com',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
os.system('clear')
for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
        name = bucket.name,
        created = bucket.creation_date,
        )

#bucket = conn.create_bucket(bucket_name,
 #       location=boto.s3.connection.Location.DEFAULT)


uploadbucket = raw_input("Enter a bucket to upload to: ")
#print uploadbucket

bucket = conn.get_bucket(uploadbucket)

#testfile = "test.txt"
#/home/ubuntu/data_in

#import os, sys
os.system('clear')
# Open a file
path = "/home/ec2-user/s3-linker/data_out/"
dirs = os.listdir( path )

# This would print all the files and directories
for file in dirs:
   print file

#os.listdir("/home/ubuntu/data_in")
filetoupload = raw_input("Which File do you want to upload: ")
#uploaddir = "/home/ubuntu/data_in/"


###############################################
#    ready for zip 
###############################################

m = re.search("zip", filetoupload)
if m is not None:
    print "found a zip file - not going into zip loop"
    zipFileName=filetoupload
else :
    zipFileName = os.path.splitext(finalready)[0] + '.zip'
    #zipFile = zipfile.ZipFile(zipFileName, "w")
    print "Creating zip archive..."
    zf = zipfile.ZipFile(path+zipFileName, mode='w')
    try:
        print "adding %s" % (filetoupload)
        zf.write(finalready)
    finally:
        print 'closing'
        zf.close()

#print
#print_info('zipfile_write.zip')
    
#os.system('clear')
###############################################



print 'Uploading %s to Amazon S3 bucket %s' % \
	(zipFileName, uploadbucket)

def percent_cb(complete, total):
    sys.stdout.write('#')
    sys.stdout.flush()

#fileuploadname = raw_input("enter name of file for server: ")

from boto.s3.key import Key
k = Key(bucket)
k.key = zipFileName #fileuploadname
k.set_contents_from_filename(path+zipFileName,
        cb=percent_cb, num_cb=10)

#os.system('clear')
####################
#conn = boto.connect_s3(
 #       aws_access_key_id = access_key,
  #      aws_secret_access_key = secret_key,
   #     host = 's3-eu-west-1.amazonaws.com',
    #    calling_format = boto.s3.connection.OrdinaryCallingFormat(),
     #   )
print ('\n')
for bucket in conn.get_all_buckets():
	print "{name}\t{created}".format(
	name = bucket.name,
	created = bucket.creation_date,
        )

#b = input("Enter your bucket:")

rawbucket = raw_input("Enter a bucket: ")
#print rawbucket
os.system('clear')
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

os.system('clear')

print "Your Link Is : %s" % (u)

sendtoaddress = raw_input('Send file to (email): ')

msg = MIMEMultipart()
msg['From'] = 'data@chewwok.com'
msg['To'] = sendtoaddress
msg['Subject'] = 'your data is ready for download'
#message = "Hello, here is the link for your data %s the link will expire in 5mins." % u
#message = "%s||\n%s||\n%s" % ('hello here is your link', u ,'this link will expire in 5mins")
message = "hello,\nthis is the link for your data.\n\n%s\n \nThe link will expire in %s \nThank you" % (u,expiredate)
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.mandrillapp.com',587)
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('d.m.holdaway@googlemail.com', 'ZP5xPlLoNKZ5PlmPR3gKGQ')

mailserver.sendmail('datasolutions',sendtoaddress,msg.as_string())

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
