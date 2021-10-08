# absurd-words
A system and website to score the absurdity and uselessness of words in English, with other languages possibly to come.
[Website](https://heph3astus.github.io/absurd-words)

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
&emsp; <img src="http://latex2png.com/pngs/b901e6f8d8c842adc50155376ff51146.png">
<br>
&emsp; where `h` is the phonemic humour value, `q` is the ambiguity value, `a` is the calculated abundance, and `u` is the word utilization.

Full Equation:<br><br>
<img src="http://latex2png.com/pngs/a7e3e6e731285563ba0ba1646b1b1cee.png">

## Phonemic Humour

Phonemic humour is calculated as described in Reference #1, calculating Shannon entropy for unigram letter frequency. To acquire letter frequency I am using the top 100000 most frequently used words in english according to Rachael Tatman's analysis of the Google Web Trillion Word Corpus (Ref. #2)

&emsp; <img src="http://latex2png.com/pngs/8ab8e7d2fca87995a1bada1974c6caae.png"><br>
where `pi` is the probablility of a letter being present in a word and l is the number of letters in the word.
## Word Utilization

Word utilization is calculated using Google NGram Viewer (Ref. #3), and is based average frequency from 1990 (or as recent as the word has been observed) to 2019. This is to adjust for inflated word frequency that can appear through trends which are even more prevalent with the internet.

&emsp; <img src="http://latex2png.com/pngs/8bbe575c6421101365179f396009d94d.png">
<br> &emsp; where `f` is the set of word frequencies for each year, and `y` is the total number of years.
## Word Ambiguity

This is based on the number of definitions as given by Wordnet (Ref. #4)

Represented as `q` in equation.

## Related Word Abundance

Relative word abundance suggests a more important word, so the Synset of a given word has its 2 layers of its hyponyms counted as given by Wordnet (Ref. #4). A large number of hyponyms suggests that its meaning is applicable to many other words, increasing its importance and decreasing its absurdity.

<img src="log(1+h_1)+\frac{1}{2}log(1+h_2)"> <br>
Where `h1` is the number of single edge related hyponyms, and `h2` is the number of double edge related hyponyms.


# Referenced Works

1. Westbury, C., et al. Telling the world’s least funny jokes: On the quantification of humor as entropy.
Journal of Memory and Language (2015), http://dx.doi.org/10.1016/j.jml.2015.09.001

2. Tatman, Rachael English Word Frequency, 1/3 Million Most Frequent English Words on the Web  (2017), https://www.kaggle.com/rtatman/english-word-frequency

3. Google, http://books.google.com/ngrams

4. Princeton University "About WordNet." https://wordnet.princeton.edu/. Princeton University. 2010.
