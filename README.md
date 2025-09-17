Build a small Python server/app that can: 
○ Take a sample customer call transcript (you can copy a short dialogue 
from anywhere or make one up). Accept a transcript as input (via endpoint 
or simple UI). 
○ Use the Groq API to: 
■ Summarize the conversation in 2–3 sentences. 
■ Extract the customer’s sentiment (positive / neutral / negative). 
○ Print the original transcript, the summary, and the sentiment. 
○ Save the output into a .csv file with 3 columns → Transcript | Summary | 
Sentiment. 
Example flow: 
● Input: “Hi, I was trying to book a slot yesterday but the payment failed…” 
● Output: Summary → “Customer faced a payment failure while booking a slot.”, 
Sentiment → “Frustrated/Negative”. 
● Save into call_analysis.csv
