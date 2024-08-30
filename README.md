# Debugging authentication issues

Adding the following line to /etc/ssh/sshd_config:
```
LogLevel DEBUG3
```

Restart the ssh server and connect to it with ssh:

sudo /etc/init.d/ssh restart
ssh localhost # should work if everything is configured OK

Check the log:
```
vladimir@xps:~/lsi/code/docs-debugging-ssh-authentication-issues$ journalctl -xeu ssh.service -q | tee /tmp/log
aug. 30 09:59:52 xps systemd[1]: Starting OpenBSD Secure Shell server...
░░ Subject: A start job for unit ssh.service has begun execution
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ A start job for unit ssh.service has begun execution.
░░ 
░░ The job identifier is 5440.
aug. 30 09:59:52 xps sshd[108736]: debug3: already daemonized
aug. 30 09:59:52 xps sshd[108736]: debug3: oom_adjust_setup
aug. 30 09:59:52 xps sshd[108736]: debug1: Set /proc/self/oom_score_adj from 0 to -1000
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 3 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 20830 on 0.0.0.0.
aug. 30 09:59:52 xps sshd[108736]: Server listening on 0.0.0.0 port 20830.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 4 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug3: sock_set_v6only: set socket 4 IPV6_V6ONLY
aug. 30 09:59:52 xps systemd[1]: Started OpenBSD Secure Shell server.
░░ Subject: A start job for unit ssh.service has finished successfully
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ A start job for unit ssh.service has finished successfully.
░░ 
░░ The job identifier is 5440.
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 20830 on ::.
aug. 30 09:59:52 xps sshd[108736]: Server listening on :: port 20830.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 5 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 10830 on 0.0.0.0.
aug. 30 09:59:52 xps sshd[108736]: Server listening on 0.0.0.0 port 10830.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 6 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug3: sock_set_v6only: set socket 6 IPV6_V6ONLY
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 10830 on ::.
aug. 30 09:59:52 xps sshd[108736]: Server listening on :: port 10830.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 7 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 830 on 0.0.0.0.
aug. 30 09:59:52 xps sshd[108736]: Server listening on 0.0.0.0 port 830.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 8 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug3: sock_set_v6only: set socket 8 IPV6_V6ONLY
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 830 on ::.
aug. 30 09:59:52 xps sshd[108736]: Server listening on :: port 830.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 9 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 22 on 0.0.0.0.
aug. 30 09:59:52 xps sshd[108736]: Server listening on 0.0.0.0 port 22.
aug. 30 09:59:52 xps sshd[108736]: debug2: fd 10 setting O_NONBLOCK
aug. 30 09:59:52 xps sshd[108736]: debug3: sock_set_v6only: set socket 10 IPV6_V6ONLY
aug. 30 09:59:52 xps sshd[108736]: debug1: Bind to port 22 on ::.
aug. 30 09:59:52 xps sshd[108736]: Server listening on :: port 22.
aug. 30 10:00:05 xps sshd[108736]: debug3: fd 11 is not O_NONBLOCK
aug. 30 10:00:05 xps sshd[108736]: debug1: Forked child 108780.
aug. 30 10:00:05 xps sshd[108736]: debug3: send_rexec_state: entering fd = 14 config len 3545
aug. 30 10:00:05 xps sshd[108736]: debug3: ssh_msg_send: type 0
aug. 30 10:00:05 xps sshd[108736]: debug3: send_rexec_state: done
aug. 30 10:00:05 xps sshd[108780]: debug3: oom_adjust_restore
aug. 30 10:00:05 xps sshd[108780]: debug1: Set /proc/self/oom_score_adj to 0
aug. 30 10:00:05 xps sshd[108780]: debug1: rexec start in 11 out 11 newsock 11 pipe 13 sock 14
aug. 30 10:00:05 xps sshd[108780]: debug1: inetd sockets after dupping: 4, 4
aug. 30 10:00:05 xps sshd[108780]: Connection from 127.0.0.1 port 58914 on 127.0.0.1 port 22 rdomain ""
aug. 30 10:00:05 xps sshd[108780]: debug1: Local version string SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
aug. 30 10:00:05 xps sshd[108780]: debug1: Remote protocol version 2.0, remote software version OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
aug. 30 10:00:05 xps sshd[108780]: debug1: compat_banner: match: OpenSSH_8.9p1 Ubuntu-3ubuntu0.10 pat OpenSSH* compat 0x04000000
aug. 30 10:00:05 xps sshd[108780]: debug2: fd 4 setting O_NONBLOCK
aug. 30 10:00:05 xps sshd[108780]: debug3: ssh_sandbox_init: preparing seccomp filter sandbox
aug. 30 10:00:05 xps sshd[108780]: debug2: Network child is on pid 108781
aug. 30 10:00:05 xps sshd[108780]: debug3: preauth child monitor started
aug. 30 10:00:05 xps sshd[108780]: debug3: privsep user:group 131:65534 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: permanently_set_uid: 131/65534 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: ssh_sandbox_child: setting PR_SET_NO_NEW_PRIVS [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: ssh_sandbox_child: attaching seccomp filter program [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: append_hostkey_type: ssh-rsa key not permitted by HostkeyAlgorithms [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: list_hostkey_types: rsa-sha2-512,rsa-sha2-256,ecdsa-sha2-nistp256,ssh-ed25519 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 20 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: SSH2_MSG_KEXINIT sent [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 20 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: SSH2_MSG_KEXINIT received [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: local server KEXINIT proposal [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: KEX algorithms: curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,sntrup761x25519-sha512@openssh.com,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group14-sha256,kex-strict-s-v00@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: host key algorithms: rsa-sha2-512,rsa-sha2-256,ecdsa-sha2-nistp256,ssh-ed25519 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: ciphers ctos: chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: ciphers stoc: chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: MACs ctos: umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: MACs stoc: umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: compression ctos: none,zlib@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: compression stoc: none,zlib@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: languages ctos:  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: languages stoc:  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: first_kex_follows 0  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: reserved 0  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: peer client KEXINIT proposal [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: KEX algorithms: curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,sntrup761x25519-sha512@openssh.com,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group14-sha256,ext-info-c,kex-strict-c-v00@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: host key algorithms: ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256 [preaut
aug. 30 10:00:05 xps sshd[108780]: debug2: ciphers ctos: chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: ciphers stoc: chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: MACs ctos: umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: MACs stoc: umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: compression ctos: none,zlib@openssh.com,zlib [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: compression stoc: none,zlib@openssh.com,zlib [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: languages ctos:  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: languages stoc:  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: first_kex_follows 0  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: reserved 0  [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: kex_choose_conf: will use strict KEX ordering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: kex: algorithm: curve25519-sha256 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: kex: host key algorithm: ssh-ed25519 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: expecting SSH2_MSG_KEX_ECDH_INIT [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 30 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: SSH2_MSG_KEX_ECDH_INIT received [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_sshkey_sign: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 6 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_sshkey_sign: waiting for MONITOR_ANS_SIGN [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 7 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 6
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_sign: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_sign: ssh-ed25519 KEX signature len=83
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 7
aug. 30 10:00:05 xps sshd[108780]: debug2: monitor_read: 6 used once, disabling now
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 31 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 21 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: ssh_packet_send2_wrapped: resetting send seqnr 3 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: ssh_set_newkeys: mode 1 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: rekey out after 134217728 blocks [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: SSH2_MSG_NEWKEYS sent [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: Sending SSH2_MSG_EXT_INFO [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 7 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: expecting SSH2_MSG_NEWKEYS [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 21 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: ssh_packet_read_poll2: resetting read seqnr 3 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: SSH2_MSG_NEWKEYS received [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: ssh_set_newkeys: mode 0 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: rekey in after 134217728 blocks [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: KEX done [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 5 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 6 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 50 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: userauth-request for user vladimir service ssh-connection method none [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: attempt 0 failures 0 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_getpwnamallow: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 8 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_getpwnamallow: waiting for MONITOR_ANS_PWNAM [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 9 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 8
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_pwnamallow: entering
aug. 30 10:00:05 xps sshd[108780]: debug2: parse_server_config_depth: config reprocess config len 3545
aug. 30 10:00:05 xps sshd[108780]: debug2: parse_server_config_depth: config  len 0
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_pwnamallow: sending MONITOR_ANS_PWNAM: 1
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 9
aug. 30 10:00:05 xps sshd[108780]: debug2: monitor_read: 8 used once, disabling now
aug. 30 10:00:05 xps sshd[108780]: debug2: input_userauth_request: setting up authctxt for vladimir [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_start_pam entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 100 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_inform_authserv: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 4 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: input_userauth_request: try method none [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: user_specific_delay: user specific delay 0.000ms [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: ensure_minimum_time_since: elapsed 1.910ms, delaying 5.073ms (requested 6.984ms) [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 100
aug. 30 10:00:05 xps sshd[108780]: debug1: PAM: initializing for "vladimir"
aug. 30 10:00:05 xps sshd[108780]: debug1: PAM: setting PAM_RHOST to "127.0.0.1"
aug. 30 10:00:05 xps sshd[108780]: debug1: PAM: setting PAM_TTY to "ssh"
aug. 30 10:00:05 xps sshd[108780]: debug2: monitor_read: 100 used once, disabling now
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 4
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_authserv: service=ssh-connection, style=, role=
aug. 30 10:00:05 xps sshd[108780]: debug2: monitor_read: 4 used once, disabling now
aug. 30 10:00:05 xps sshd[108780]: debug3: userauth_finish: failure partial=0 next methods="publickey,password" [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 51 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 50 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: userauth-request for user vladimir service ssh-connection method publickey [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: attempt 1 failures 0 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: input_userauth_request: try method publickey [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: userauth_pubkey: valid user vladimir querying public key rsa-sha2-512 AAAAB3NzaC1yc2EAAAADAQABAAABAQDgWCnAc+OeOMF9yR6jgb3hx4EHosZ0HiFnU4TEzi6e98DdE1TvtmKd7chVkw/kQrtq89IiqXasehXpR/SsbhvMEaxFrI+7rRRmtZ8FhI4HX00X0/QMJHXa9hH8qtRu/755R+qVrlVRJFIvxff3GjfYwRExQ8oH42IoUYjYoY0RSitDdJ9WtnPKLX8+uOtRyg7i35m4NavIUnGN7CPbdH7LRPsfiSo6Wo095AB+5QyD52/rOG5F7JExTV9Ee4UUNeiHLYC7pj5jDgLhEURQ5Z+ke3cANwmHTPenH+ZWfJGEgNtLhIdN8Pq+bv7jY/z2RiZLc9R499eQv1OjQnRY1pq9 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: userauth_pubkey: publickey test pkalg rsa-sha2-512 pkblob RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_key_allowed: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 22 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_key_allowed: waiting for MONITOR_ANS_KEYALLOWED [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 23 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 22
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_keyallowed: entering
aug. 30 10:00:05 xps sshd[108780]: debug1: temporarily_use_uid: 1000/1000 (e=0/0)
aug. 30 10:00:05 xps sshd[108780]: debug1: trying public key file /home/vladimir/.ssh/authorized_keys
aug. 30 10:00:05 xps sshd[108780]: debug1: fd 5 clearing O_NONBLOCK
aug. 30 10:00:05 xps sshd[108780]: debug1: /home/vladimir/.ssh/authorized_keys:1: matching key found: RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4
aug. 30 10:00:05 xps sshd[108780]: debug1: /home/vladimir/.ssh/authorized_keys:1: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
aug. 30 10:00:05 xps sshd[108780]: Accepted key RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4 found at /home/vladimir/.ssh/authorized_keys:1
aug. 30 10:00:05 xps sshd[108780]: debug2: check_authkeys_file: /home/vladimir/.ssh/authorized_keys: processed 1/5 lines
aug. 30 10:00:05 xps sshd[108780]: debug1: restore_uid: 0/0
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_keyallowed: publickey authentication test: RSA key is allowed
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 23
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 60 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: userauth_pubkey: authenticated 0 pkalg rsa-sha2-512 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: user_specific_delay: user specific delay 0.000ms [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: ensure_minimum_time_since: elapsed 1.609ms, delaying 5.375ms (requested 6.984ms) [preauth]
aug. 30 10:00:05 xps sshd[108780]: Postponed publickey for vladimir from 127.0.0.1 port 58914 ssh2 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: receive packet: type 50 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: userauth-request for user vladimir service ssh-connection method publickey-hostbound-v00@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: attempt 2 failures 0 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: input_userauth_request: try method publickey-hostbound-v00@openssh.com [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: userauth_pubkey: valid user vladimir attempting public key rsa-sha2-512 AAAAB3NzaC1yc2EAAAADAQABAAABAQDgWCnAc+OeOMF9yR6jgb3hx4EHosZ0HiFnU4TEzi6e98DdE1TvtmKd7chVkw/kQrtq89IiqXasehXpR/SsbhvMEaxFrI+7rRRmtZ8FhI4HX00X0/QMJHXa9hH8qtRu/755R+qVrlVRJFIvxff3GjfYwRExQ8oH42IoUYjYoY0RSitDdJ9WtnPKLX8+uOtRyg7i35m4NavIUnGN7CPbdH7LRPsfiSo6Wo095AB+5QyD52/rOG5F7JExTV9Ee4UUNeiHLYC7pj5jDgLhEURQ5Z+ke3cANwmHTPenH+ZWfJGEgNtLhIdN8Pq+bv7jY/z2RiZLc9R499eQv1OjQnRY1pq9 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: userauth_pubkey: publickey-hostbound-v00@openssh.com have rsa-sha2-512 signature for RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_key_allowed: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 22 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_key_allowed: waiting for MONITOR_ANS_KEYALLOWED [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 23 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 22
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_keyallowed: entering
aug. 30 10:00:05 xps sshd[108780]: debug1: temporarily_use_uid: 1000/1000 (e=0/0)
aug. 30 10:00:05 xps sshd[108780]: debug1: trying public key file /home/vladimir/.ssh/authorized_keys
aug. 30 10:00:05 xps sshd[108780]: debug1: fd 5 clearing O_NONBLOCK
aug. 30 10:00:05 xps sshd[108780]: debug1: /home/vladimir/.ssh/authorized_keys:1: matching key found: RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4
aug. 30 10:00:05 xps sshd[108780]: debug1: /home/vladimir/.ssh/authorized_keys:1: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
aug. 30 10:00:05 xps sshd[108780]: Accepted key RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4 found at /home/vladimir/.ssh/authorized_keys:1
aug. 30 10:00:05 xps sshd[108780]: debug2: check_authkeys_file: /home/vladimir/.ssh/authorized_keys: processed 1/5 lines
aug. 30 10:00:05 xps sshd[108780]: debug1: restore_uid: 0/0
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_keyallowed: publickey authentication: RSA key is allowed
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 23
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_sshkey_verify: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 24 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_sshkey_verify: waiting for MONITOR_ANS_KEYVERIFY [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 25 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 24
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_keyverify: publickey RSA signature using rsa-sha2-512 verified
aug. 30 10:00:05 xps sshd[108780]: debug1: auth_activate_options: setting new authentication options
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 25
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 102
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug1: do_pam_account: called
aug. 30 10:00:05 xps sshd[108780]: debug2: do_pam_account: auth information in SSH_AUTH_INFO_0
aug. 30 10:00:05 xps sshd[108780]: debug3: PAM: do_pam_account pam_acct_mgmt = 0 (Success)
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 103
aug. 30 10:00:05 xps sshd[108780]: Accepted publickey for vladimir from 127.0.0.1 port 58914 ssh2: RSA SHA256:GVffiXFtSVilSne/FCdy17xRIQ7EuzmQhARWFjKaen4
aug. 30 10:00:05 xps sshd[108780]: debug1: monitor_child_preauth: user vladimir authenticated by privileged process
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_get_keystate: Waiting for new keys
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 26
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_get_keystate: GOT new keys
aug. 30 10:00:05 xps sshd[108780]: debug1: auth_activate_options: setting new authentication options [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug2: userauth_pubkey: authenticated 1 pkalg rsa-sha2-512 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: user_specific_delay: user specific delay 0.000ms [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: ensure_minimum_time_since: elapsed 1.024ms, delaying 5.960ms (requested 6.984ms) [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_do_pam_account entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 102 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive_expect: entering, type 103 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_do_pam_account returning 1 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: send packet: type 52 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 26 [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_send_keystate: Finished sending state [preauth]
aug. 30 10:00:05 xps sshd[108780]: debug1: monitor_read_log: child log fd closed
aug. 30 10:00:05 xps sshd[108780]: debug3: ssh_sandbox_parent_finish: finished
aug. 30 10:00:05 xps sshd[108780]: debug1: PAM: establishing credentials
aug. 30 10:00:05 xps sshd[108780]: debug3: PAM: opening session
aug. 30 10:00:05 xps sshd[108780]: debug2: do_pam_session: auth information in SSH_AUTH_INFO_0
aug. 30 10:00:05 xps sshd[108780]: pam_unix(sshd:session): session opened for user vladimir(uid=1000) by (uid=0)
aug. 30 10:00:05 xps sshd[108780]: debug3: PAM: sshpam_store_conv called with 1 messages
aug. 30 10:00:05 xps sshd[108780]: debug3: PAM: sshpam_store_conv called with 1 messages
aug. 30 10:00:05 xps sshd[108780]: User child is on pid 108883
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_receive: entering
aug. 30 10:00:05 xps sshd[108780]: debug3: monitor_read: checking request 28
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_pty: entering
aug. 30 10:00:05 xps sshd[108780]: debug2: session_new: allocate (allocated 0 max 10)
aug. 30 10:00:05 xps sshd[108780]: debug3: session_unused: session id 0 unused
aug. 30 10:00:05 xps sshd[108780]: debug1: session_new: session 0
aug. 30 10:00:05 xps sshd[108780]: debug1: SELinux support disabled
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_request_send: entering, type 29
aug. 30 10:00:05 xps sshd[108780]: debug3: mm_answer_pty: tty /dev/pts/3 ptyfd 3
vladimir@xps:~/lsi/code/docs-debugging-ssh-authentication-issues$
```

# Debugging subsystem launch issues

There are cases where after successfull authentication a subsystem process e.g. netconf-subsystem is not started due to configuration file issues, unresolved executable shared library dependencies etc.
Debugging such issues requires starting sshd within gdb and investgating in case the log does not provide a clue:


... TBD ...  
