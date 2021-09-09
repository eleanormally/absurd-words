# absurd-words
A system and website to score the absurdity and uselessness of words in English, with other languages possibly to come.


# API Routes 

- ### `/getWord/`
  - Returns score and datapoints for any given word
  - Accepts parameter `calculate` as a boolean
    - If true will use external sources to calculate score
    - If false will only use records within database
  - Example Use: `/getWord/absurd`

- ### `/words`
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
        - `humour`
        - `humourInverse`
        - `util`
        - `utilInverse`
      - default `score`




# Scoring System

Simplified Equation: <br>
&emsp; <img src="https://latex.codecogs.com/gif.latex?u*%281&plus;%5Cfrac%7B-h&plus;q&plus;%5Cfrac%7Ba%7D%7B2%7D%7D%7B100%7D%29">
<br>
&emsp; where `h` is the phonemic humour value, `q` is the ambiguity value, `a` is the calculated abundance, and `u` is the word utilization. 

Full Equation:<br><br>
<img src="https://latex.codecogs.com/gif.latex?-log%28%5Cfrac%7B%5Csum%20f_i%7D%7By%7D%20%29*%281&plus;%5Cfrac%7B%5Cfrac%7B%5Csum%20p_i*log_2%28p_i%29%7D%7Bl%7D&plus;q&plus;%20%5Cfrac%7Blog%281&plus;h_1%29%20&plus;%20%5Cfrac%7B1%7D%7B2%7Dlog%281&plus;h_2%29%7D%7B2%7D%20%7D%7B100%7D%29">

## Phonemic Humour

Phonemic humour is calculated as described in Reference #1, calculating Shannon entropy for unigram letter frequency. To acquire letter frequency I am using the top 100000 most frequently used words in english according to Rachael Tatman's analysis of the Google Web Trillion Word Corpus (Ref. #2)

&emsp; <img src="https://latex.codecogs.com/gif.latex?-%5Cfrac%7B%5Csum%20p_i%20*%20log_2%28p_i%29%7D%7Bl%7D"><br>
where `pi` is the probablility of a letter being present in a word and l is the number of letters in the word.
## Word Utilization

Word utilization is calculated using Google NGram Viewer (Ref. #3), and is based average frequency from 1990 (or as recent as the word has been observed) to 2019. This is to adjust for inflated word frequency that can appear through trends which are even more prevalent with the internet. 

&emsp; <img src="https://latex.codecogs.com/gif.latex?-log%28%5Cfrac%7B%5Csum%20f_i%7D%7By%7D%29"> 
<br> &emsp; where `f` is the set of word frequencies for each year, and `y` is the total number of years.
## Word Ambiguity

This is based on the number of definitions as given by Wordnet (Ref. #4)

Represented as `q` in equation.

## Related Word Abundance

Relative word abundance suggests a more important word, so the Synset of a given word has its 2 layers of its hyponyms counted as given by Wordnet (Ref. #4). A large number of hyponyms suggests that its meaning is applicable to many other words, increasing its importance and decreasing its absurdity. 

<img src="https://latex.codecogs.com/gif.latex?log%281&plus;h_1%29%20&plus;%20%5Cfrac%7B1%7D%7B2%7Dlog%281&plus;h_2%29"> <br>
Where `h1` is the number of single edge related hyponyms, and `h2` is the number of double edge related hyponyms.


# Referenced Works

1. Westbury, C., et al. Telling the world’s least funny jokes: On the quantification of humor as entropy.
Journal of Memory and Language (2015), http://dx.doi.org/10.1016/j.jml.2015.09.001

2. Tatman, Rachael English Word Frequency, 1/3 Million Most Frequent English Words on the Web  (2017), https://www.kaggle.com/rtatman/english-word-frequency

3. Google, http://books.google.com/ngrams

4. Princeton University "About WordNet." https://wordnet.princeton.edu/. Princeton University. 2010. 