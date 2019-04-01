# Setup instructions

- Install Kerberos and setup for lxplus by modifying your local ```/etc/krb5.conf``` file to include the following:  
```
[realms]
    CERN.CH = {
        default_domain = cern.ch
        kpasswd_server = cerndc.cern.ch
        admin_server = cerndc.cern.ch
        kdc = cerndc.cern.ch
    }

[domain_realm]
    cern.ch = CERN.CH
    .cern.ch = CERN.CH
```
see also https://groups.lal.in2p3.fr/comuti/2015/09/30/kerberos-and-afs-configuration-on-ubuntu/

- Copy into the file ```~/.ssh/config``` the following: 
```
Host *.cern.ch lxplus*
        User kparasch
        GSSAPITrustDns yes
        GSSAPIAuthentication yes
        GSSAPIDelegateCredentials yes
        ForwardX11 yes
        ForwardX11Trusted no
```
modifying the ```User``` variable as necessary.

Run ```kinit``` and ```aklog``` to enable afs access without asking password each time.
