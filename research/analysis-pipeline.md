We are trying to build our own banking-as-a-service API lawyer. We are a credit union that is building its own core and wants to focus on sponsor banking. As part of that process, we want to take all the API docs from the top providers, and runs analysis to identify first what are all of the decision points (as in what kind of design decisions do we need to make) and second do a compare and contrast analysis of each company’s API so that we can better understand how they each decided to address the fundamental endpoints and data structures all BaaS platforms have to expose. Let’s do this step by step, so don’t write any code yet. My first question is what is the best way to take all of the raw API documentation so that it can be ingested by an LLM.

wget --recursive --level=3 --no-parent \
     --wait=2 --random-wait \
     --user-agent="Mozilla/5.0 (compatible; research bot)" \
     --reject-regex=".*\.(css|js|png|jpg|gif|pdf)$" \
     --accept-regex=".*docs.*" \
     https://column.com/docs/

Tried using wget but the documentation info is injected using javascript so it is only able to retrieve a react shell

Used crawler.py script to retrieve pages from column. They are too large to directly give to an llm so we need a way to get only the relevant info.
Used extract_api_docs.py to clean up the files and make them small enough to give to an llm.
Created a validation script to ensure that we are collecting all the documentation data from each page.