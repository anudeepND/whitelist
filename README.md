## Commonly white listed domains for Pi-Hole.     
          
A robust collection of commonly white listed websites borrowed from various sources including Pi-Hole subreddit, Pi-Hole forum, Pi-Hole github repository and more!
Add these domains to your Pi-Hole setup by running a script or manually and make your setup **trouble-free!**
                
Want to report a new domain? Want to report exsisting one? Feel free to file an <a href="https://github.com/anudeepND/whitelist/issues">issue</a>.
         
* * *
         
### Main features:
       
- The entire repo is curated.
- New domains are added frequently.
- Comes with a shell script i.e you can add all domains automatically at an instant.
- Domains are categorised and are included in 3 different files.
- If you are a beginner to Pi-Hole, adding these sites resolves many problems. 
       
***
     
### Description
       
The repository has 3 different files containing different domains.      
       
***whitelist.txt***       
This file contain domains that are safe to whitelist i.e it does not contain any tracking or advertising sites. Adding this file fixes many problems like YouTube watch history, videos on news sites and so on...
        
***referral-sites.txt***      
People who use services like Slickdeals and Fatwallet needs a few sites (most of  them are ads) to be whitelisted to work properly. This file contains some analytics and ad serving sites, if you don't know what these services are stay away from this list.
           
***optional-list.txt***       
This file contain domains that are needed to be whitelisted depending on the service you use. It may contain some tracking site but sometimes it's necessary to add bad domains to make a few services to work.     
          
***
           
### Installation and Usage
         
***For whitelist.txt***     
```
git clone https://github.com/anudeepND/whitelist.git
cd whitelist/scripts
sudo chmod +x whitelist.sh
sudo ./whitelist.sh
```
             
***For referral-sites.txt***          
```
git clone https://github.com/anudeepND/whitelist.git
cd whitelist/scripts
sudo chmod +x referral.sh
sudo ./referral.sh
```
        
***For optional-list.txt***     
You can add it manually depending upon the service you use. 
          
***     
               
### How do I determine an ad domain?
         
***DNSthingy Assistant***
         
<a href="https://chrome.google.com/webstore/detail/dnsthingy-assistant/fdmpekabnlekabjlimjkfmdjajnddgpc">This browser extension</a> will list all of the domains that are queried when a web page is loaded. You can often look at the list of domains and cherry pick the ones that appear to be ad-serving domains.     
        
![Alt text](https://discourse.pi-hole.net/uploads/default/optimized/1X/6ce0e13813df930288677c87bf0fd5861c150898_1_690x320.png)
          
***Using inbuilt Developer tool***     
          
For Chrome ctrl+shift+I will land you in Developer tools menu.
![Alt text](http://i.imgur.com/44CHRLV.png)
       
***
     
### Licence
```
MIT License

Copyright (c) 2018 Anudeep ND <anudeep@protonmail.com>

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
