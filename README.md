# zero-knowledge-proof
This application is focused on building a zero knowledge proof of ownership of an LLM, without revealing the parameters used in the model.
It takes model parameters as input, stores them in an encrypted format and runs the model internally. The result is then compared with the output we got. 
If these results match, it means we ran the exact model without changing the weights, therefore we proved our ownership of the model

# Input
Right now, (as of 14/01/26) we are generating a very small model locally and using that to test the system.
Once frontend is done, the user will provide the model weights.