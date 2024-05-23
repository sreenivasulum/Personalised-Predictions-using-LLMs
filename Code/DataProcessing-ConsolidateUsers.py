## Aim : Consolidating Users:
# Finding the common users
# Finally for those common user extract relevent purchases and reviews of products of each domain
# From those user interacted products extract the meta data.
"""Steps:

1. Give the domain names 
    Select available domains from link :: https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023

2. Load the existing common users dataset 
    file :: common_users_dataset.jsonl
    data point schema :: 
        {
        user_id
        asin
        parent_asin
        timestamp
        verified_purchase
        title
        text
        domain
        }

3. For first domain
    Download the dataset from huggingface
    both reviews and meta data

4. For next domains

5. Download the dataset
    find common users
    save them in common_users_dataset.jsonl
    save related meta data in 


"""

#### With Sampling
## TODO: Continue with entire dataset

# libraries
import pandas 
import json
import tqdm
from datasets import load_dataset

# Domains:

domains = [
    'Books',
    'Cell_Phones_and_Accessories'
    'Electronics',
    'Movies_and_TV',
    'Software'
]

## First domain
first_domain = domains[0]

## Downloading the first domain
print("Downloading first domain ::",first_domain)
first_dataset_review = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_review_{}".format(first_domain), trust_remote_code=True)
# first_dataset_meta = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_meta_{}".format(first_domain), trust_remote_code=True)
print("Downloading completed !!!")


print("\n")
print("Extracting users from domain:: ",first_domain)

first_domain_users = set([])
for data_point in tqdm.tqdm(first_dataset_review):
    user = data_point['user_id']
    if user not in first_domain_users:
        first_domain_users.add(user)
print("Extracting complete !!!")
print("\n")

# initializing
common_users = []
common_users_data = []
common_users_filename = "CommonUsersDataset_.jsonl"

## iterating to other domains
for domain in domains[1:]:
    print("Downloading domain ::",domain)
    dataset_review = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_review_{}".format(domain), trust_remote_code=True)
    # dataset_meta = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_meta_{}".format(domain), trust_remote_code=True)
    print("Downloading completed !!!")

    print("\n")
    print("Extracting users from domain:: ",domain)
    domain_users = set([])

    for data_point in tqdm.tqdm(dataset_review):
        user = data_point['user_id']
        if user not in domain_users:
            domain_users.add(user)
    
    # finding the common users
    common_users_updated = first_domain_users & domain_users

    if first_domain == domains[0]:
        print("Filtering data from first domain :: ",first_domain)
        for datapoint in tqdm.tqdm(first_dataset_review): 
            if datapoint['user_id'] in common_users_updated:
                datapoint['domain'] = first_domain # Added domain for future reference
                common_users_data.append(datapoint)
        print("Completed !!")
        print("\n")
        
    print("Filtering data from the domain :: ",domain)
    for datapoint in tqdm.tqdm(dataset_review):
        
        if datapoint['user_id'] in common_users_updated:
            datapoint['domain'] = domain # Added domain for future reference
            common_users_data.append(datapoint)
    print("Completed !!")
    print("\n")

    ### done for the domain

    ## saving for the checkpoint ::
    print("Saving to check point")
    common_users_filename = common_users_filename.split(".")[0]

    if first_domain == domains[0]:
        common_users_filename += first_domain

    common_users_filename += domain
    common_users_filename += ".jsonl"
    print("Filename :: ",common_users_filename)
    with open(common_users_filename, 'w') as out:
        for ddict in common_users_data:
            jout = json.dumps(ddict) + '\n'
            out.write(jout)
    print("Completed !!!")

    ## initialization for next domain
    first_domain = domain
    first_domain_users = common_users_updated
    

print("Done !!! Hurray !!")