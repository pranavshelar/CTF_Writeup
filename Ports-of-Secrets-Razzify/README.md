# Port of Secrets - Writeup
**Platform**: Razzify.in     
**Difficulty**: Hard    
**Category**: Web Client     
#### Hints Given: 
1.  Not every response is the same - look closely at how the system replies.
2.  Check the internal-api services carefully and port numbers from 8k to 9k.
3.  Once you identify that internal port, try exploring common paths.

### Intial Walkthrough of Web Application
The challenge provided as web application named **CheckNet** which is network monitoring Platform. Then I begin exploring all the available functions and how the application works. Then the website was giving us two options of **Login** and **Sign Up**.    
![homepage](homepage.png)     
So I created a test account with fields Email Id, Password & Mobile Number. Then after Logging into the account I was then given the only  tool/feature which was called **Check Network Service Status** .   
This function was having an:
- Service URL Input Field 
- Response Output Field 
The purpose of this function was seeming to enter a URL to check its network health by fetching content of web application.      
![loggedin](loggedin.png)
### Input Testing of field
I first started with entering some common url like **www.google.com, https://test.com** .        
It gave me a json response like:          
{      
  "output": "Fetched content from www.google.com"    
}    

![normal_response](normal_response.png)
From this we get to know that the Backend of webserver is fetching input url. This was common sign that **SSRF** would be present.      
Then I also tried to enter some url which where fetching .json file. As the input field was giving an example "https://example.com/status.json".           
I tried "https://test.com/flag.json" and "https://example.com/status.json" This gave a whole different response:            
{       
  "status": "ok",      
  "url": "https://test.com/flag.json"      
}     

This indicates that the web application acted differently for .json files. There must be an input validation or whitelisting is implemented in the web app.         
So now by keeping **SSRF** in mind I started to enter some internal services name in the input field. 
I entered **localhost, 127.0.01, 0.0.0.0** and also localhost with some typosquatting but the response was:           
{            
  "error": "Blocked URL: local addresses are not allowed."   
}     

This indicated that some filtering logic is present but I use some more internal services to bypass the filtering.       
And Atlast with internal-api the response was:    
{      
  "output": "Fetched content from interanl-api"     
}    

Then I tried http://internal-api/flag.json to see if i can get any output of flag but the reponse told us more:         
{       
  "error": "Failed to fetch (timeout)"      
}     

Then I started changing the port number to 8080 it gave me a response:      
{     
  "error": "Try Harder, Right service and endpoint missing"     
}    
This indicates that the hostname was correct but with some misconfiguration in port and also the hint given told us to check port numbers between **8000-9000**.          
So intercepted the request in Burpsuite and with help of **Intruder** I check the response with all port numbers between 8000-9000.       
![burpsuite](burpsuite_intruder.png)      
After enumeration of the ports I got one port with different response length. So I checked its response and it was 8085 and gave response:         
{      
“notice”: “Valid service detected on this port. Try exploring endpoints.”        
}    
I found the correct port number and no we need to enumerate the correct endpoint to get the flag.    
So I started with endpoints like:       
- http://internal-api:8085/flag.json
- http://internal-api:8085/flag
- http://internal-api:8085/flags.json
But by entering the endpoint **http://internal-api:8085/flag**,
we got the **Flag**     
![Flag_found](flag3.png)


The returned flag:        
{  
“flag”: “Z&q1ESEj8$”  
}

### Summary: 
This challenges tell us that improper validation of input could lead to potential SSRF vulnerablities. So we should always implement difficult input validation. By properly enumerating the responses and viewing them we I was able to retrive the flag.




