

# Cloud Computing Project 

LINE front end

## Design 

Chat bot server is running on Heroku and it's data store in redis server.

Chat bot have 2 response type:

*  Measurement against coronavirus:
	1.	User input keyword "Measure"
	2.	Bot return a video of measure coronavirus.
	3.	Bot return message "More?"
	3.	User response "Yes" or "More"
	4.	if user response "Yes" or "More", return second video.

*  Finding Mask
	1.	User input keyword "Mask"
	2.	Bot return "Please input district"
	3.	User input district or *
	4.	Bot return "Addess of selling mask in *district* is *Address*"
