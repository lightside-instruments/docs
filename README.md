Some mail hosting services like Amazons WorkMail are substituting the "Return-Path" mail address with a dynamic one e.g. Return-Path: <0100018b75f9efae-b35a598b-d7ef-408a-a2a8-5fea3b24bf4d-000000@mailfrom.lightside-instruments.com>. This is not acceptable for some receiving mail servers e.g. ietf.org

So this is how you can send a mail from the command line without relay SMTP server without switching your subscription. And here is the result - https://mailarchive.ietf.org/arch/msg/bmwg/PrMYslnP9y7TPXtfBJ-QD-6bsTY :

This worked on Ubuntu 22 jammy. 

Generate keys - notice the '-traditional' parameter that fixes a bug
```
openssl genrsa -out key1.private -traditional 2048
openssl rsa -in key1.private -out key1.pub -pubout
```
The keys part of the repository are provided as example and were used once for sending the reference message.


Create key1.txt DNS record from the contents of your key1.pub
```
$ cat key1.txt 
key1._domainkey	IN	TXT	( "v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApxGHaxYdZq5Z+UbuyIBQWBmFFzMeWF3aAWv8kOhG4OljNHWr6nBoeTVduxGof8v/A6VjjBO+eRDUP10qDafNTiCI9KnDOW8BuwFHzZEbmINbchXwKuba3JrqxZ88iBVt70I1KZ76UW2zQUKT9qTbhphcUHSgF55/tK6vT+2td5Dj0ztZreVWknwAXgTKPLWrAPahN2mXa8T+NawF7G1PO4VUqBAJL43GtVBigrY2XviDudidaixoR99hsNYSDpD/+byXgzsT2LqwRV2cYx/s+80OuJ1ZtG3f5eNXCCNGVQuuxMq5+Lh1E0gNeYZG76rzWBkT51cm34fhUhG8cLwrLwIDAQAB" )  ; ----- DKIM key key1 for itional
```

If you installed the DKIM public key record correctly you should be able to read it back with dig.
```
$ dig txt key1._domainkey.lightside-instruments.com any
...
;; ANSWER SECTION:
key1._domainkey.lightside-instruments.com. 3600	IN TXT "v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApxGHaxYdZq5Z+UbuyIBQWBmFFzMeWF3aAWv8kOhG4OljNHWr6nBoeTVduxGof8v/A6VjjBO+eRDUP10qDafNTiCI9KnDOW8BuwFHzZEbmINbchXwKuba3JrqxZ88iBVt70I1KZ76UW2zQUKT9qTbhphcUHSgF55/tK6vT+2td5Dj0ztZreVWknw" "AXgTKPLWrAPahN2mXa8T+NawF7G1PO4VUqBAJL43GtVBigrY2XviDudidaixoR99hsNYSDpD/+byXgzsT2LqwRV2cYx/s+80OuJ1ZtG3f5eNXCCNGVQuuxMq5+Lh1E0gNeYZG76rzWBkT51cm34fhUhG8cLwrLwIDAQAB"
```

Note that ietf.org will not accept mail from senders without fully qualified domain name.
So your hostname should be the same as the hostname of a permitted mail senderlisted in
the spf record e.g. bitraf.lightside-instruments.com

```
lightside-instruments.com. 594	IN	TXT	"v=spf1 include:amazonses.com include:bitraf.lightside-instruments.com ~all"
```

and you should be connecting from its IP address.

Send mail:
```
apt-get install python3-dkim
python3 sendmail.py
```
