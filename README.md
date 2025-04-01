# LLM-TSP
Project on querying an LLM to generate a random TSP in a given (real world) geography. 

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

conda env create -f environment.yml
conda activate tsp
```

### 2. Create a hidden.env file 

For this project, we used two API keys, one for OpenAI and one for GoogleMaps. Set up a file with the name 'hidden.env' and set it up with the following values defined: 

OPENAI_API_KEY = ""

maps_API_KEY = ""

Ensure you add in your keys. 

### 3. Run the notebook of your choice. 

There are currently two working versions of this project. 

1. basic.ipynb
   
A very basic version that uses birds-eye distance (as determined by GPT-4).

2. main.ipynb
   
A more interesting version that incorporates the GoogleMaps API to get more accurate information on distances and times for various forms of transport, as well as information from GPT-4. This includes a "priority" choice that allows a person to choose between time and distance as the distance metric for the graph. 

There is also an incomplete more complicated version: 

3. wip.ipynb
