### Commonly whitelisted domains

These domains are borrowed from various sources including reddit, GitHub and other forums.
You can request additional domains via <a href="https://github.com/anudeepND/whitelist/issues">Issues</a> tab.

If you're using pi-hole, you can quickly add these sites to your whitelist.txt, to do this: 

• `sudo -s` 

•`curl -sS https://raw.githubusercontent.com/anudeepND/whitelist/master/whitelist.txt >> /etc/pihole/whitelist.txt`


##### How do I determine an ad domain?

##### a). DNSthingy Assistant

<a href="https://chrome.google.com/webstore/detail/dnsthingy-assistant/fdmpekabnlekabjlimjkfmdjajnddgpc">This browser extension</a> will list all of the domains that are queried when a web page is loaded. You can often look at the list of domains and cherry pick the ones that appear to be ad-serving domains.


![Alt text](https://discourse.pi-hole.net/uploads/default/optimized/1X/6ce0e13813df930288677c87bf0fd5861c150898_1_690x320.png)
 
 
 
##### b). Using inbuilt Developer tool
For Chrome ctrl+shift+I will land you in Developer tools menu.
![Alt text](http://i.imgur.com/44CHRLV.png)

##### Note:
Some deals sites like Slickdeals and Fatwallet needs ad sites to work correctly, you can use `referral-sites.txt`to whitelist some domains.  
To add them quickly to whitelist:  
•`sudo -s`  
•`curl -sS https://raw.githubusercontent.com/anudeepND/whitelist/master/referral-sites.txt >> /etc/pihole/whitelist.txt`
