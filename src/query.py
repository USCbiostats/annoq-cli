import argparse
import json
import shlex
import requests

from src.variables import VARIABLES


url = 'http://bioghost2.usc.edu:3403/annoq-test/_search'

def get_query(sources, chr, start, end): 

  query = {
    "_source":sources,
    "aggs":{
        "chr":{
          "filter":{
              "exists":{
                "field":"chr"
              }
          }
        },
        "pos_min":{
          "min":{
              "field":"pos"
          }
        },
        "pos_max":{
          "max":{
              "field":"pos"
          }
        },
        "pos":{
          "filter":{
              "exists":{
                "field":"pos"
              }
          }
        },
        "ref":{
          "filter":{
              "exists":{
                "field":"ref"
              }
          }
        },
        "alt":{
          "filter":{
              "exists":{
                "field":"alt"
              }
          }
        },
        "rs_dbSNP151":{
          "filter":{
              "exists":{
                "field":"rs_dbSNP151"
              }
          }
        }
    },
    "query":{
        "bool":{
          "filter":[
              {
                "term":{
                    "chr":chr
                }
              },
              {
                "range":{
                    "pos":{
                      "gte":start,
                      "lte":end
                    }
                }
              }
          ]
        }
    },
    "from":0,
    "size":50
  }
  
  return query

def search_chr(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--chr', required=True)
    parser.add_argument('--start', required=True)
    parser.add_argument('--end', required=True)

    try:
        parsed_args = parser.parse_args(shlex.split(' '.join(args)))
        print(f"Searching with chr: {parsed_args.chr}")
        chr = parsed_args.chr
        start = parsed_args.start
        end = parsed_args.end
        query = get_query(VARIABLES['config'], chr, start, end)
        main(query)
    except SystemExit:
        pass  # Ignore exit() call in argparse error handling


def main(query):
  response = requests.post(url, json=query)

  if response.status_code == 200:
      print('Request was successful!')
      print('Response data:\n', json.dumps(response.json(), indent=4))
  else:
      print('Request failed with status code:', response.status_code)


if __name__ == "__main__":
    pass