# Office Hours

## Getting Started
1. Create a Droplet on DigitalOcean. Select the following specs: 2 vCPUs, 2GB RAM, 60GB SSD.
2. SSH into the Droplet, and run:
   ```
   sudo apt update
   sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
   ```
3. Clone this repo in the `/home` directory.
4. Export your class roster from Gradescope, and copy it to `home/office-hours/data/`. The expected format is
   ```
   First Name,Last Name,SID,Email,Role,Section
   ```
5. Export the [Office Hours Staff Form](https://docs.google.com/spreadsheets/d/1Wn6h2tmi9SoQH9uGMbwoHEVriN5_zBFK5TA9VpunLVM/edit?usp=sharing) as a CSV. Delete the first row AND delete the first column.
6. Copy the staff CSV to the bottom of the roster CSV from step 4.
7. Create an [app password](https://support.google.com/accounts/answer/185833?hl=en) for the email address you'd like to use to send passcodes and notifications.
8. Create a `.env` file in `office-hours/` and populate it as follows (no quotes around the fields):
   ```
   SECRET_KEY=A PASSWORD FOR FLASK
   SENDER_EMAIL=EMAIL ADDRESS FROM STEP 7
   SENDER_PASSWORD=APP KEY FROM STEP 7
   ```
9. Run the following commands in order:
   ```
   cd office-hours
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   sudo ufw allow 5000
   python run.py
   ```
10. 
