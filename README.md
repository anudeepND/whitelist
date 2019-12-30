<p align="center">
  <img width="550" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/logo.png">
</p>    
      
<p align="center">  
  <a href="https://www.paypal.me/anudeepND"><img alt="Donate using Paypal" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"></a>
  &nbsp;&nbsp;
  <a href="https://liberapay.com/Anudeep/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>
</p>
         
         
## Commonly white listed domains for Pi-Hole (Compatible with Pi-Hole Docker Image).  
          
A robust collection of commonly white listed websites borrowed from various sources including Pi-Hole subreddit, Pi-Hole forum, Pi-Hole github repository and more!
Add these domains to your Pi-Hole setup by running a script or manually and make your setup **trouble-free!**
                
Want to report a new domain? Want to report exsisting one? Feel free to file an <a href="https://github.com/anudeepND/whitelist/issues">issue</a>.
         
         
 <p align="center">
  <img height="430" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/run.gif">
</p> 
         
* * *
         
### Main features:
       
- The entire repo is curated.
- New domains are added frequently.
- Supports Pi-Hole Docker installation.
- Comes with a shell script i.e you can add all domains automatically at an instant.
- Domains are categorised and are included in 3 different files.
- If you are a beginner to Pi-Hole, adding these sites resolves many problems. 
       
***
     
### Description
          
|      File Name     | Domain Count |                                                                                                                                                                Description                                                                                                                                                                | Update Frequency |                                             Raw Link                                            |
|:------------------:|:------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------:|:-----------------------------------------------------------------------------------------------:|
| whitelist.txt      | 194          | This file contain domains that are **safe** to whitelist i.e it does not contain any tracking or advertising sites. Adding this file fixes many problems like YouTube watch history, videos on news sites and so on. If you want to report additional domain feel free to file an [issue](https://github.com/anudeepND/whitelist/issues). | Occasionally     | [link](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt)      |
| referral-sites.txt | 72           | People who use services like Slickdeals and Fatwallet needs a few sites (most of  them are either trackers or ads) to be whitelisted to work properly. This file contains some analytics and ad serving sites like **doubleclick.net** and others. **If you don't know what these services are, stay away from this list.**               | Occasionally     | [link](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/referral-sites.txt) |
| optional-list.txt  | --           | This file contain domains that are needed to be whitelisted depending on the service you use. It may contain some tracking site but sometimes it's necessary to add bad domains to make a few services to work. Currently there is no script for this list, you have to add domains manually to your Pi-Hole.                             | Occasionally     | [link](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/optional-list.txt)  |    
             
***
           
### Installation and Usage
        
 ***For Docker installation***           
 Access you running Pi-Hole container by `docker exec -it <container-ID> bash` and proceed with the steps given below:
```
git clone https://github.com/anudeepND/whitelist.git
cd whitelist/scripts
./whitelist.sh
```
If you keep the `/etc/pihole` on a volume outside the container you need to change `PIHOLE_LOCATION`and `GRAVITY_UPDATE_COMMAND` variables based on your setup.
         
***For whitelist.txt***     
```
git clone https://github.com/anudeepND/whitelist.git
cd whitelist/scripts
sudo ./whitelist.sh
```
             
***For referral-sites.txt***          
```
git clone https://github.com/anudeepND/whitelist.git
cd whitelist/scripts
sudo ./referral.sh
```

**Note: You don't have to clone the repo every time you need to update whitelist file. Navigate to `whitelist/scripts` and run it again `sudo ./whitelist.sh`**
        
***For optional-list.txt***     
You can add it manually depending upon the service you use. 

***For Automated Update***
```
cd /opt/
sudo git clone https://github.com/anudeepND/whitelist.git
```
Make the script to run the script at 1AM on the last day of the week

`sudo nano /etc/crontab`

Add this line at the end of the file:       
`0 1 * * */7     root    /opt/whitelist/scripts/whitelist.sh`

CTRL + X then Y and Enter

```
sudo whitelist/scripts/whitelist.sh
sudo ./whitelist.sh
```
   
***     
               
### How do I determine an ad domain?
         
***Adam:ONE Assistant (Previously known as DNSthingy***
         
<a href="https://chrome.google.com/webstore/detail/adamone-assistant/fdmpekabnlekabjlimjkfmdjajnddgpc">This browser extension</a> will list all of the domains that are queried when a web page is loaded. You can often look at the list of domains and cherry pick the ones that appear to be ad-serving domains.     
        
<p align="center">
  <img width="600" height="500" src="https://raw.githubusercontent.com/anudeepND/blacklist/master/images/img1.jpeg">
</p>
      
***Using inbuilt Developer tool***     
          
For Chrome ctrl+shift+I will land you in Developer tools menu.
      
<p align="center">
  <img width="450" height="600" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/img2.jpeg">
</p>      
          
***Using an Android app*** 
     
[Net Guard](https://play.google.com/store/apps/details?id=eu.faircode.netguard) is an Android app that can be used to monitor any specific apps, works on unrooted devices too.   
        
<p align="center">
  <img width="500" height="400" src="https://raw.githubusercontent.com/anudeepND/whitelist/master/images/img3.jpeg">
</p>
             
***
   
### Donation

All donations are welcome and any amount of money will help me to maintain this project :)
<p align="center">  
  <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N6RDWAAZSW5T6&source=url"><img alt="Donate using Paypal" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"></a>
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
