# Tool Retriever
This is the repository of Team 3 of AI Guild.

## Running the model
- git clone the repo into your local machine
- ensure python version is higher than 3.10(preferably version 3.12)
- run the following commands
- ``` bash
   cd tool_retriever
   ```
  Create a .env file in the root directory to store the Groq API Key
- ```bash
   touch .env
  ```
  Add the following line to the file.
- ```makefile
  GROQ_API_KEY="your_api_key"
  ```
  Install all requirements either in virtual environment or local machine.
- ``` bash 
  pip3 install -r requirements.txt
  ```
  Run the below script to load the model.
- ``` bash
  python3 model-1.py
  ```

* The UI should pop up like in the picture given below.
 ![Screenshot from 2024-10-18 23-07-29](https://github.com/user-attachments/assets/66374a90-5bae-4460-b3d0-9dc5021f5357)


* User can choose the prompting style of the LLM (either CoT or ToT) and can provide their query in the query box. The output will be displayed on the right hand window along with the reasoning of the LLM in the bottom right.
 ![Screenshot from 2024-10-18 23-11-35](https://github.com/user-attachments/assets/40980d0b-a1b2-41b9-87d0-a808d70bb249)

  
