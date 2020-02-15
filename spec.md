

# Cloud Computing Project 

LINE front end

## Design 

Chat bot server is running on Heroku and it's data store in redis server.

Chat bot have 2 response type:

*  Measurement against coronavirus:
	1.	User input keyword "Measure"
	2.	Bot return question, such as "Are you get cold\ feel uncomfortable\ have fever", etc.
	3.	User response "Yes" or "No"
	4.	Finally Bot return "You have sign of coronavirus" or "You have not sign of coronavirus".

*  Finding Mask
	1.	User input keyword "Mask"
	2.	Bot return "Please input your district"
	3.	User input district
	4.	Bot return "Number of Mask in *district* is *Number*, are you need to order one?"
	5.	User input "Yes" then Server Mask number minus one, or "No" to exit
