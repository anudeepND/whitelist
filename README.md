<p align="center">
  <img width="550" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/logo.png">
</p>    
      
<p align="center">  
  <a href="https://www.paypal.me/anudeepND"><img alt="Donate using Paypal" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"></a>
  &nbsp;&nbsp;
  <a href="https://liberapay.com/Anudeep/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>
</p>
         
         
# Commonly white listed domains for Pi-Hole (Compatible with Pi-Hole Docker Image).  
          
A robust collection of commonly white listed websites borrowed from various sources including Pi-Hole subreddit, Pi-Hole forum, Pi-Hole GitHub repository and more!
Add these domains to your Pi-Hole setup by running a script or manually and make your setup **trouble-free!**
                
Want to report a new domain? Want to report existing one? Feel free to file an <a href="https://github.com/anudeepND/whitelist/issues">issue</a>.
         
         
 <p align="center">
  <img height="630" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/whitelist.gif">
</p> 
         
* * *
         
## Main features:
       
- The entire repo is curated.
- New domains are added frequently.
- Supports Pi-Hole Docker installation.
- Comes with a simple install/uninstall scripts i.e you can add all domains with comments automatically at an instant.
- Domains are categorized and are included in 3 different files.
- All the domains will have comments to let you know about the domain.
- If you are a beginner to Pi-Hole, adding these sites will solve issues with host files that block legit websites. 
       
***
     
## Description
          
|      File Name     | Domain Count |                                                                                                                                                                Description                                                                                                                                                                | Update Frequency |                                             Raw Link                                            |
|:------------------:|:------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------:|:-----------------------------------------------------------------------------------------------:|
| whitelist.txt      | 188          | This file contain domains that are **safe** to whitelist i.e it does not contain any tracking or advertising sites. Adding this file fixes many problems like YouTube watch history, videos on news sites and so on. If you want to report additional domain feel free to file an [issue](https://github.com/anudeepND/whitelist/issues). | Occasionally     | [link](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt)      |
| referral-sites.txt | 72           | People who use services like Slickdeals and Fatwallet needs a few sites (most of  them are either trackers or ads) to be whitelisted to work properly. This file contains some analytics and ad serving sites like **doubleclick.net** and others. **If you don't know what these services are, stay away from this list.**               | Occasionally     | [link](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/referral-sites.txt) |
| optional-list.txt  | --           | This file contain domains that are needed to be whitelisted depending on the service you use. It may contain some tracking site but sometimes it's necessary to add bad domains to make a few services to work. Currently there is no script for this list, you have to add domains manually to your Pi-Hole.                             | Occasionally     | [link](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/optional-list.txt)  |    
             
***
           
## Installation
 
 Make sure you have **python3** installed on your machine. You can simply install it by using `sudo apt install python3`
      
***For whitelist.txt***     
```
git clone https://github.com/anudeepND/whitelist.git
sudo python3 whitelist/scripts/whitelist.py
```
             
***For referral-sites.txt***          
```
git clone https://github.com/anudeepND/whitelist.git
cd whitelist/scripts
sudo ./referral.sh
```

If you are using Pi-hole 5.0 or later, the comment field has a unique string - `qjz9zk` to uniquely identify the domains added by this script so the user can remove the domains without affecting other whitelisted sites. 

        
***For optional-list.txt***     
You can add it manually depending upon the service you use. 
           
 ***For Docker installation***           
 Access you running Pi-Hole container by `docker exec -it <container-ID> bash` and proceed with the steps given below:
```
git clone https://github.com/anudeepND/whitelist.git
sudo python3 whitelist/scripts/whitelist.py
```
If you keep the `/etc/pihole` on a volume outside the container you need to change pass the appropriate values to the variables based on your setup.
                   
**Note: You don't have to clone the repo every time you need to update whitelist file. Navigate to `whitelist/scripts` and run it again `sudo python3 whitelist.py`**         
***
   
## Uninstall
         
         
 <p align="center">
  <img height="630" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/uninstall.gif">
</p> 


As mentioned earlier, the unique string (`qjz9zk`) will come in handy while removing the domains from the database. It uses LIKE operator of the SQLite to match the wildcard string present in the comment section.

`SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%'`
This statement will remove the domain only if it is present in the exact whitelist section and having the string `qjz9zk`. Domains in the regex list will not be removed by this script.

The older version of the Pi-hole uses a simple text file to store the entries. In this case the script will match the domains present in your Pi-hole to the domains present in the GitHub repo and removes them accordingly.
           
**To remove the domains:**    
`sudo python3 uninstall.py`
        
***
     
## For Automated Update
```
cd /opt/
sudo git clone https://github.com/anudeepND/whitelist.git
```
Make the script to run the script at 1AM on the last day of the week

`sudo nano /etc/crontab`

Add this line at the end of the file:       
`0 1 * * */7     root    /opt/whitelist/scripts/whitelist.py`

CTRL + X then Y and Enter

```
sudo whitelist/scripts/whitelist.py
```
   
***     
      
### How do I determine an ad domain?
         
***Adam:ONE Assistant (Previously known as DNSthingy***
         
<a href="https://chrome.google.com/webstore/detail/adamone-assistant/fdmpekabnlekabjlimjkfmdjajnddgpc">This browser extension</a> will list all of the domains that are queried when a web page is loaded. You can often look at the list of domains and cherry pick the ones that appear to be ad-serving domains.     
        
      
***Using inbuilt Developer tool***     
          
For Chrome ctrl+shift+I will land you in Developer tools menu.
           
          
***Using an Android app*** 
     
[Net Guard](https://play.google.com/store/apps/details?id=eu.faircode.netguard) is an Android app that can be used to monitor any specific apps, works on unrooted devices too.   
        
             
***
   
### Donation

All donations are welcome and any amount of money will help me to maintain this project :)
<p align="center">  
  <a href="https://www.paypal.me/anudeepND"><img alt="Donate using Paypal" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"></a>
  &nbsp;&nbsp;
  <a href="https://liberapay.com/Anudeep/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>
</p>
   
### Licence
```
MIT License

Copyright (c) 2019 Anudeep ND <anudeep@protonmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
