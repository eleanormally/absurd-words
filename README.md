# absurd-words
A system and website to score the absurdity and uselessness of words in English, with other languages possibly to come.


# API Routes 

- ### `/getWord/`
  - Returns score and datapoints for any given word
  - Accepts parameter `calculate` as a boolean
    - If true will use external sources to calculate score
    - If false will only use records within database
  - Example Use: `/getWord/absurd`

- ### `/topWords`
  - Paramters
    - `results`
      - integer up to 50, number of results to return
      - default 20
    - `startIndex`
      - integer, which value to start from (for getting further loaded results)
      - default 0
    - `sortMethod`
      - string, options:
        - `score`
        - `scoreInverse`
        - `a-z`
        - `z-a`
      - default `score`
