# How to dump a request in firefox 
Sometimes dump of request that your device webUI does is required to debug a bug/implement a new feature for device that is not in our posession.
Here is HOWTO do it, in text and a youtube video.

## HOWTO

1. Open firefox
2. Navigate to required page in your modem webUI
3. Go to Settings (3 horizontal lines in right top corner) -> More tools -> Web Developer Tools
4. In web developer tools go to "Network" tab.
5. (Optional) Set URL filter if you know request URL you want to dump
6. Do required action in webUI
7. Find request in list of request (check its headers and body to confirm that it is required request)
8. Dump it by right clicking on the request and select "Save All As HAR", set the dump name to something sane.
9. Post the dump in issue thread or send it to dev email for analysis.

## Video HOWTO
https://youtu.be/DKKian-014E
