

# Cloud Computing Project 

We would develop a LINE front end chatbot of this project which used to share public health care information of coronavirus currently. Because chatbot is only sharing public data thus there is not provide private service, such as Ordering mask, record personal status, etc. Instead of, we provide video of measure coronavirus and each district mask count.

## Design 

Chat bot server is running on Heroku and it's data store in redis server.

Chat bot have 2 response type:

*  Measurement against coronavirus:
	1.	User input keyword "Measure"
	2.	Bot send request to server and search for video title match with the keyword. 
	3.	Bot return a video of measure coronavirus.
	4.	Bot return message "More?"
	6.	User response "Yes" or "More", "No" or ignore message
	7.	If user response "Yes" or "More", Bot will send request to server to search second video.
	8.	If user response "No", Bot will return message "Thanks for watching and take care!"

*  Finding Mask:
	1.	User input keyword "Mask"
	2.	Bot return "Please input district"
	3.	User input district or * 
	4. 	If user input district Bot send request to server and search for shop address that categorised under input distict.
	5.	If user input * then bot return all the shop address which still have mask.
	6.	Bot return "Addess of selling mask in *district* is *Address* with *amount* of Box in stock"
	7.	IF user input district, bot return "Do you want to search for other district?"
	7. 	If user input "Yes", then repeat step2. If user input "No", Bot return "Thanks for the query and take care!"
	
* Unknown input (e.g. video, image, undefined word, etc.)
	1.	Bot return "Please input "Measure" or "Mask" to getting service"
	

