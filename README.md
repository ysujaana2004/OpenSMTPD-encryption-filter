# Secure Email with OpenSMTPD + GPG Encryption Filter

This project demonstrates how to configure a local email server using [OpenSMTPD](https://www.opensmtpd.org/) and extend its functionality with a custom **Python filter** that **automatically encrypts incoming emails using GPG**.

The idea is inspired by privacy-first services like ProtonMail, where messages are encrypted for users *at the server level*, provided they have a registered public key.

---

## Project Goals

- ✅ Set up OpenSMTPD to **receive mail locally** on macOS
- ✅ Create and manage **GPG keypairs**
- ✅ Build a **Python filter** that encrypts incoming messages using GPG
- ✅ Integrate the filter with OpenSMTPD's configuration
- ✅ Test the entire pipeline: sending → receiving → encryption verification

---

## Why This Project Matters

OpenSMTPD is a secure, lightweight mail server. Combined with GPG, it allows messages to be encrypted **in transit and at rest**, so that even if the server is compromised, no one can read your emails without your private key.

---

## Prerequisites

- macOS (tested on MacBook Air)
- Homebrew
- OpenSMTPD (`brew install opensmtpd`)
- GPG (`brew install gnupg`)
- Python 3
- Basic shell scripting and file permissions knowledge

---

## Project Structure

opensmtpd-gpg-filter/

  ├── filter-gpg.py              # Python encryption filter

  ├── smtpd.conf                 # OpenSMTPD configuration file

  ├── public_keys/               # Folder to store public keys

---

## Step-by-Step Setup

### 1. Install OpenSMTPD and GPG

https://github.com/OpenSMTPD/OpenSMTPD?tab=readme-ov-file 

Follow the steps on readme to set up OpenSMTPD

```bash
brew install opensmtpd gnupg
```

2. Set up local mail spool

```python
sudo mkdir -p /var/mail
sudo touch /var/mail/$(whoami)
sudo chown $(whoami) /var/mail/$(whoami)
sudo chmod 600 /var/mail/$(whoami)
```

3. Generate a GPG Key

```python
gpg --full-generate-key
```

- Select key type: RSA
- Key size: 2048 or 4096 bits (choose 4096)
- Validity: Choose 0 (no expiration)
- Provide name + email (can be fake if local)
- Keyphrase: make sure to choose something you will remeber

![Screenshot 2025-10-17 at 3.03.19 PM.png](attachment:47b00032-8457-4c72-8bec-89d5e7e52b88:Screenshot_2025-10-17_at_3.03.19_PM.png)

 Export Public Key:

```python
mkdir -p ~/.gnupg/public_keys
gpg --armor --export your-email@example.com > ~/.gnupg/public_keys/you.pub

```

4. Create the Encryption Filter

      Create a Python file `filter-gpg.py`:

```python
sudo nano ~/opensmtpd-filters/filter-gpg.py
#write the script
```

Make it executable 

```python
chmod +x ~/opensmtpd-filters/filter-gpg.py
```

5. Configure OpenSMTPD

```python
sudo nano /usr/local/etc/smtpd/smtpd.conf
#add the rules/commands
```

6. Start OpenSMTPD

```python
sudo pkill smtpd
```

Then run in debug mode:

```python
sudo smtpd -dv -f /usr/local/etc/smtpd/smtpd.conf
```

```python
#Sending a Test Email
#this command didn't work for me. It only deplayed the plain text and not the encrypted version 
echo "This is a secret email" | mail -s "Encrypted Test" yourusername
```

```python
#this works for encryption 
#
echo "This is a message to test the encryption using gpg on september 17th 2025" | gpg --encrypt --armor --recipient ysujaana2004@gmail.com
```

```python
echo "This better work" | \      
gpg --encrypt --armor --recipient ysujaana2004@gmail.com | \
mail -s "Encrypted Test" sujanayeasmin

#WORKED 
```

![Screenshot 2025-10-18 at 11.01.03 PM.png](attachment:561efd9c-efd3-43cb-b5aa-ffcfd4804b8f:Screenshot_2025-10-18_at_11.01.03_PM.png)

Open another tab in the terminal and check mail

```python
mail
```

If the filter worked, the email body should look like:

```python
-----BEGIN PGP MESSAGE-----
hQIMA2V...
...
-----END PGP MESSAGE-----

#Copy the entire encrypted text
```

```python
gpg --decrypt 

#paste the entire encrypted text and then paste it 

# Control+d
```

## What the Filter Does

- Collects message body line-by-line
- Encrypts the message using the recipient's GPG public key
- Replaces the plain text with an encrypted block
- Lets OpenSMTPD continue normal delivery

How to Test Encryption:

You can copy the message into a file `msg.asc` and decrypt:

How to Check Mail Daily:

```python
mail  #check mails

q    #exit our of mailbox 

# type 
      mail
 # again to check mail again
```

## Why Local Email + GPG?

- No need for domain setup or DNS
- Local testing is safer, faster
- GPG ensures only users with private keys can read their email

## Summary of GPG’s Role in this Project

| Goal | GPG helps because  |
| --- | --- |
| **Automatic encryption** | You can script it easily in filters |
| **User-level privacy** | Each user has their own public key |
| **Zero trust for server** | Even you (as the server admin) can't read their mail |
| **ProtonMail-style privacy** | It mimics ProtonMail’s "encrypt all received mail" model, but locally and self-hosted |

## Limitations & Next Steps

- Works only for **local delivery** (no external sending)
- GPG keys must be manually generated per user
- You can extend this to support multiple users by mapping public keys
- Optionally, configure Gmail as a relay for outbound mail (I tried to this but failed. Horribly)

## LINKS

- [OpenBSD](https://www.openbsd.org/)
- [OpenSMTPD github](https://github.com/OpenSMTPD/OpenSMTPD?tab=readme-ov-file)
- [OpenSMTPD project](https://www.opensmtpd.org/)
- [GnuPG](https://gnupg.org/)
- [Protonmail](https://github.com/ProtonMail)
- [Config file](https://man.openbsd.org/smtpd.conf)

###  Files:

- `README.md` — Clear overview (see below)
- `smtpd.conf` — Your working OpenSMTPD config
- `filter.c` or `filter.py` — If/when you write a custom filter
- `scripts/` — Any helper setup scripts you used
- `docs/` — Additional diagrams or step-by-step guides

Flow chart

```python
              You have their PUBLIC KEY
                   ↓
            Encrypt your message using it
                   ↓
    Encrypted Message (Unreadable to anyone else)
                   ↓
          Sent via email, stored locally
                   ↓
   Recipient uses their PRIVATE KEY to decrypt
                   ↓
          They can now read the message
```
