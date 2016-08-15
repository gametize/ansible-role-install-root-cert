# Ansible Role: Install Root CA Certificate

This ansible role will install the Root CA Certificate on the target hosts. Requires privileged access to work.

ELI5 why I need this:

  - I create a device certificate (e.g. www.example.com). My web server uses it for SSL.
  - Other machines trying to access to my web server will be sad 'cos the SSL certificate is self-signed and is not trusted yet. Bummer :(

So what is this ansible role for?

  - I can create a private key for my organization, and created a self-signed CA (Certificate Authority) certificate from this key
  - *With this ansible role, I can install this CA certificate into client machines *
  - I create a device certificate (e.g. www.example.com) signed with my CA certificate (and its private key), and use it for my web server
  - When my client machines visit my web server (www.example.com), the SSL certificate should be valid. Yay!
  - If the created private key is misused, bad things could happen (e.g. spoofing `google.com`). So keep the orangaization's private key secure!

This playbook is can be used on the following platforms:

  - CentOS 6, 7
  - Ubuntu 14.04, 16.04
  - Mac OS 10.12 (**not** idempotent, and not well-tested)


## Dependencies

This role requires the Root CA certificate.

## Variables

  - `install_root_cert_pem` The full path of the Root CA cert (`.pem`) on the local machine

## Usage

Example playbook:

```
---
- hosts: all
  become: yes
  vars:
    install_root_cert_pem: files/root_ca.pem
  roles:
    - gametize.install-root-cert
```

## Tests

Travis tests (`.travis.yml`) are set up according to this [article](http://www.jeffgeerling.com/blog/2016/how-i-test-ansible-configuration-on-7-different-oses-docker) by geerlingguy.

Gitlab CI tests are set up similarly, and can be run with [gitlab-runner](https://gitlab.com/gitlab-org/gitlab-ci-multi-runner). Example of running this locally:

    gitlab-ci-multi-runner exec shell test_centos7

#### Artifacts used in tests

The keys and certificates can be generated via the commands as follows. DO NOT use these settings for production!

```
$ ### Generate key and certificate for root CA
$ openssl genrsa -out root_ca.key 1024
$ openssl req -x509 \
    -subj '/C=SG/ST=Singapore/L=Singapore/O=Example Inc/OU=Example Inc Certificate Authority/CN=example.com' \
    -new -nodes -key root_ca.key -sha256 -days 1024 \
    -out root_ca.pem

$ ### Generate key and certificate for device
$ openssl genrsa -out localhost.key 1024    # generate key for device `localhost.key`
$ openssl req -new \
    -subj '/C=SG/ST=Singapore/L=Singapore/O=Example Inc/OU=Example Inc Testing Department/CN=localhost' \
    -new -nodes -key localhost.key -sha256 -days 1024 \
    -out localhost.csr

$ ### Sign the device certificate with Root CA certificate and key
$ openssl x509 -req \
    -in localhost.csr -CA root_ca.pem -CAkey root_ca.key \
    -CAcreateserial -out localhost.crt -days 1024 -sha256
$ cat localhost.crt localhost.key > localhost.pem
```

## License

MIT

## Author Information

LIM EnSheng (ensheng@gametize.com)
