# How it started
Some mail hosting servidces like Amazons WorkMail are substituting the ReplyTo mail address with a dynamic one. This is not acceptable for some receiving mail servers e.g. ietf.org

So this is how you can send a mail without switching your subscription:

Generate keys - notice the '-traditional' parameter that fixes a bug
```
openssl genrsa -out key1.private -traditional 2048
openssl rsa -in key1.private -out key1.pub -pubout
```
This does not work due to the '-traditional' parameter bug
```
opendkim-genkey -s key1 -d lightside-instruments.com -traditional -b 2048
```
Generate key1.private key1.txt
```
$ cat key1.txt 
key1._domainkey	IN	TXT	( "v=DKIM1; h=sha256; k=rsa; "
	  "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAplkotPLTpbwqGwPZ9w6y"
"Ktuwq3NWLxmfsI6dzxyVd05/h/PmU28RUH4qsys/FbKWR49cGhBmBgBrLFuOyvRP"
"9abJuiLJgjXR2DvIz9WFqnZOsl8JxPu1CUlV3cj7wQiL99dLK71PRBVBOZBppSLU"
"ARxObYDhlPsPIbhjlHDBNvJTvQ//LeJecTMVf22hKxOXtBolB1LvGtWi91pCmw0m"
"5Yng4/3Ppp5JnuEb6avgIwwNlIUTkKfVu4UQZ9HXFi6/JTh318q+2IDTKCz/Zjds"
"37qOsvs+Hy2VmSLekw6b/9An/6CjyGqW2IEFP+pTgKowidAeDJViI4NrskuRu4sf"
"kQIDAQAB" )  ; ----- DKIM key key1 for itional
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
