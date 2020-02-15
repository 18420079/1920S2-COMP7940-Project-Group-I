

# Cloud Computing Project 

LINE front end

## Design 

Chat bot server is running on Heroku and it's data store in redis server.

Chat bot have 2 response type:

*  Measurement against coronavirus: 
	User input keyword "Measure"
	Bot return question, such as "Are you get cold\ feel uncomfortable\ have fever", etc.
	User response "Yes" or "No"
	Finally Bot return "You have sign of coronavirus" or "You have not sign of coronavirus".

*  Finding Mask
	User input keyword "Mask"
	Bot return "Please input your district"
	User input district
	Bot return "Number of Mask in *district* is *Number*, are you need to order one?"
	User input "Yes" then Server Mask number minus one, or "No" to exit