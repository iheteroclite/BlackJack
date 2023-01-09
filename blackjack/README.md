## Blackjack - CLI (with a twist)!

    ` ____________  ____________
    /            \/            \
    |    Ace     ||    Jack    |
    |            ||            |
    |  ♣     ♣   ||  ♦     ♦   |
    |            ||            |
    |     ♣      ||     ♦      |
    \____________/\____________/`


Do you want to try your hand at beating the odds in blackjack? Or simulating your chances of getting caught cheating with a sleight of hand? This is the game for you!

In this game you will have the option to play with friends, multiple players using multiple decks, and if you want to, you can try to cheat. But watch out: you can get caught if the dealer sees you, or even in a random pat-down, or if the card you cheat with has already been played.
You can select your difficulty level by choosing different dealers, but the chance of being caught will always increase as the statistical liklihood of your success rate decreases - so try not to win every game.
Have fun!

### The Game

The goal in blackjack is to beat the dealer's score with a score of 21 or less.

#### Gameplay

Each player is dealt two cards, and the dealer is dealt two cards. Each player has a turn, in which they can ask for another card (**hit**), as many times as they like until they decide they like the hand they have so stop hiting (**stand**), **surrender** the hand (loose this round), or the cards in their hand score over 21 (**bust**). The next player then takes their turn. When every player has taken a turn it is then the dealer's turn.

#### Rules
* 10, Jack, Queen, and King cards are each worth 10
* Aces are worth either 1, or 11. The most standard is a player-choice ace. This means that the player can decide whether their Ace is worth 1 or 11. Other variants fix the ace value at 11, and a variant '21', used more frequently in younger agegroups, requires aces to be worth 1 (so it is impossible to get blackjack).
* A *blackjack* is the best possible hand, an opening deal with a ten and an ace, scoring blackjack, 21 in just 2 cards.
* Players do not compete against each other, only against the dealer
* The dealer's action is dictated by a fixed strategy, so the dealer will always follow these rules:
    * Hit if the hand value is less than 17
    * Stand if the hand value is 17 or more.

#### Win Conditions
* If a player goes **bust** they lose the round.
* If a player **surrenders** they lose the round.
* If a dealer goes **bust** all players who are still in the game (not **bust** or **surrendered**) win the round.
* If the player and dealer have the same hand value, there is a tie (**push**), which is named **push** because if players are betting on their hands, the dealer would push their stake back to them.
* Whoever has the highest hand value (player or dealer) then wins the round.
    * Blackjack wins agaianst 21.
* After each game, players can see their hand's score, and whether they won against the dealer (remember, it is possible to lose with a 21 if the dealer has blackjack).  
  
    `The dealer's score is: 20
    Player 1 scored 17, LOSES`

    `The dealer's score is: 21
    Player 1 scored blackjack, WINS BLACKJACK`

#### Probabilities

Each round this game will display probabilities.

The probabilities are:
* If the player got a win or blackjack this round: Probability of getting a win (even win or blackjack) this particular round.
* Probabiity of gettting the exact number of wins the player has in the exact number of rounds the player has played.
* Probability of getting at least the number of wins the player has, in the same number of rounds.

For example, *Player 1* has played 6 rounds, with 1 blackjack 1 win, and 5 losses. At the end of round 6 they see:

    `Player 1, over 6 rounds you have scored:
    Wins: 1 (16.7 %) with 1 blackjack (at 23.9 % chance)
                    [with 25.8 % chance of at least 1]
                    and 0 even payouts (at 6.0 % chance)
                    [with 100 % chance of at least 0]
    Losses: 5       Pushes: 0`

This means that *Player 1* has won ***16.7 %*** of the ***6*** rounds they have played. There was a ***23.9 %*** chance of them getting exactly ***1*** blackjack over these specific ***6*** rounds. There was a ***25.8 %*** chance of them getting 1 or more blackjacks over these ***6*** rounds (that's the chance of getting either 1, 2, 3, 4, 5, or 6 blackjacks, but not getting 0).
There was only a ***6.0 %*** chance of not getting no wins (exactly 0 wins). This gives an ***100 %*** chance of getting at least 0 wins (quite obviously, they must get 0 or more wins), so perhaps the player could improve their strategey for when to **hit** and when to **stand**.

This will allow you, the player to compare your strategy against a standard win percentage. If there was only a 10% chance of getting at least your wins (after a number of rounds), you are doing very well, perhaps your strategy is working. If there is a 50% chance of getting at least the number of wins you have got, then your strategy is average, and you will quickly see when you are doing worse than the average player as that percentage rises! The probability that you got at least as many wins as you have is also used to determine your chance of getting caught when cheating...

#### Cheating

Players have the option to cheat! This means that at the beginning of the game they can hide cards up their sleeve:

    `[?]  Player 1, Would you like to cheat?:
     \> Yes, sneak cards up my sleeve!
       Heavens no!
       Help me with Cheating
       Help me with Probability`

If you choose to cheat you can swap a cards in your hand with cards hidden up your sleeve. Every card which goes into your sleeve is marked, so the dealer if they
suspect you of cheating will have some probability of noticing it is marked.

Watch out, there are various ways the dealer might catch you:

* The card you played was a duplicate. It has already been played, and the dealer noticed.
* You look suspicious because you have a high rate of even wins (not blackjack)
* You look suspicious because you have a high rate of blackjack wins
* You are caught in a random patdown

You won't always get caught, whether you are caught is based on a probabalistic formula designed by the author @iheteroclite and derived from a binomial distribution mass function. Your liklihood of getting caught is very dependent on how good your dealer is at spotting you...

#### Dealer Choice (Difficulty Levels)

Pick a dealer at your peril!

    `Big Brother shouts 
    PLAYER 1, I SEE YOU CHEATING!
    You're so suspicious, getting so many blackjacks.
    GET OUT of my CASINO, Twinkletoes!`

Every game of blackjack is different - especially if you compare playing at home or in a Vegas casino, and you have a different chance of being caught if you're swapping cards. So this game gives you a choice of dealers:

    `[?]  Players, Select a Dealer (hardest first):
     \> Big Brother
       Casino Cat
       Sharp-Eyed Stacy
       Happy Harry
       Grandma Gertrude
       Blind Bob`

Each dealer has a different chance of catching you cheating, so if you want to just have a laugh pick `Grandma Gertrude` or `Blind Bob`, but for a more casino-ready player, challenge yourself with `Casino Cat` or even `Big Brother` - the eye in the sky! The hardest level, Big Brother will always catch you if you play a card which has already been played, and is more likely to catch you for every other reason.


### Getting started

#### Quickstart
If you have done this before:
- clone the repo:  
    `$ gh repo clone iheteroclite/BlackJack`  
- install requirements:   
    `$ pip3 install -r requirements.txt`  
- run the program:   
    `python3 blackjack.py`  

#### Detailed Setup Instructions
- Open a terminal and check you have Python 3 installed:  
    **Linux, Windows and MacOS:**  
    `$ python3 --version`  
    If you have Python 2 and Python 3 on the same system you will need to continue using `python3`, but you can check whether you have only Python 3 installed by:  
    `$ python --version`  
    If the output is **Python 3.x.x**, you only have Python 3 installed.  
    This program requires Python 3.8.x (e.g 3.8.2) or higher.  

- Clone this GitHub repo
    Get to the folder you want the repo to be cloned into using `cd` and optionally `mkdir`  
    In the folder you want the repo to be in:  
    `$ gh repo clone iheteroclite/BlackJack`  
    For this you will need the official GitHub `gh` CLI package installed on your local machine and have done some initial setup, see here for assistance:  
    https://cli.github.com/


- (Optional) Install a virtual environment
    - If you would only like to install the required python packages for this project in a virtual environment, rather than on your own machine, you will want to use Python's new venv package (or the virtualenv package).  
    - Install venv:  
        **Linux with apt**  
        `$ sudo apt install python3-venv`  
        **Linux with apt-get**  
        `$ sudo apt-get install python3-venv`  
        **Redhat Linux**  
        `$ yum install python3-venv`  
        **With npm**  
        `$ npm install python3-venv`  
    - Check venv is installed:  
        `$ venv --version`  
    - Create a virtual environment:  
        `$ python3 -m venv /path/to/enviroment`  
        Use the path of the directory where you have cloned the GitHub repo.  
    - Run your environment  
        From inside the project directory:  
        `$ source venv/bin/activate`  
        Here \<venv> is the name of the venv directory. It ocassionally has a different name, so to see files type:  
        `ls`  
        which is the UNIX command to list all files in a folder.  
- Install requirements:  
    `$ pip3 install -r requirements.txt`  

- If you have Python 3 and requirements installed:  
    - Open a terminal
    - `ls` to check you are in a folder showing the file `blackjack.py`  
    - Type  
        `$ python3 blackjack.py`
    - Play the game, have fun, and challenge yourself!
- If that doesn't work, check your setup and download Python 3 if needed:  
    - https://wiki.python.org/moin/BeginnersGuide/Download

- To run the unit tests:  
    - From the same terminal window, type  
        `$ python3 -m unittest discover test`.
- To run the flake8 tests:  
    - From the same terminal window, type `cd ..` to change to the parent directory
    - (Optional - Advanced) Include the flakes8 config at `/test/config.flake8` if you wish to use a standard configuration file
    - run:  
        `$ flake8 --config test/config.flake8 blackjack.py`
    - This will output either errors (with codes in red), and an error count, or will output `0` (which means there are no errors)
    - The config file `config.flake8` has per-file ignores, and these are commented to show reasoning

### Test Documentation
- Full test documentation list with justification for the test cases is available in the Documentation folder.


### Potential Extentions
A month ago I initially envisaged this game being ported to a Django app, with authenticated users equivalent to players, and stored gameplay data in a many-to-many
sql database (with a Django implementation of SQLLite). I had envisioned multiple players could play on the server (separate terminals), and see a Single Page Application with some beautiful animations and graphical representations of the cards.

This game could be very easily extended to also catch card counting (but as I do not know how unlikely your hand has to be for a casino to suspect you of cheating, this has not yet been programmed).

Another interesting extension could include the possibility for the dealer to accuse the wrong player of cheating. If Player 1 and Player 2 both play an Ace of Hearts, when playing with a single deck of cards, it is possible that the dealer might mistakenly accuse the wrong player of cheating.


### Probability Calculation

#### Important note on Probabilities

I, @iheteroclite, the author, am not a Statistician, I have read Physics (which is a poor approximation), and was surprised that the chance of drawing blackjack from a specific deck is not well-modelled (until I tried to model it). After pages of derivations and attempts at deriving a good hypergeometric density function (for which mine had an asymptope at 1, so was not useful for this game), I concluded that a good model would suffice. I have tested this model with Mathematica, and it seems to be a good model, the probability of blackjack: decreases as aces and tens in the deck decrease; increases as deck size decreases; is 0 when there are no aces or no tens; and approaches 0.5 when there are exactly 50/50 aces/tens. However, it is entirely possible that there may be unforseen limitations of the model I have used.

Probability of a blackjack is modelled using a binomial distribution mass function, with an alteration made to account for a varying probability of getting a blackjack each turn.

The probability of getting a blackjack is dependent on:
* How many 10s are in the deck
* How many aces are in the deck
* How many cards are in the deck

This probability is calculated using the formula:  

```math
P = \frac{aces}{N} \times \frac{tens}{N-1} \times 2
```

    where:
    aces = total number of aces in the deck
    tens = total number of tens in the deck
    N = total number of cards in the deck

So in a 52 card deck there are 4 aces and 16 tens. If you draw a card from a shuffled deck, there is a:  
chance of drawing an *ace* = 4/52 = 0.0769 = 7.7%  
chance of drawing a *ten* = 16/52 = 0.3077 = 30.8%   
chance of *blackjack* = 4/52 * 16/52 * 2 = 0.048 = 4.8%  

If 20 cards have been drawn from a 52 card deck, and none of them were an ace or 10, Jack, Queen, King, then there are still 4 aces and 16 10-value cards in the deck, but only 32 cards, so:  
chance of drawing an *ace* = 4/32 = 0.125 = 12.5%   
chance of drawing a *ten* = 16/32 = 0.5 = 50%  
chance of *blackjack* = 4/32 * 16/31 * 2 = 0.129 = 0.13  



In a binomial distribution, 1 - prob_win is the probability of a single loss. The probability mass function is:

```math

\displaystyle f(wins) = \begin{pmatrix}rounds\cr wins\cr\end{pmatrix} (p^{wins}) (1 - p)^{(rounds - wins)}

```

where:
p = prob_win, the fixed probability of a single win

This is used to calculate the chance of getting the amount of even wins
(wins) that the player has. Even wins means a win that pays out at even
odds (1:2), so any win that is not a natural/blackjack. It assumes that the
wins follow a binomial distribution.

The default probability of winning is for even wins, taken as a standard
0.4222 chance of winning, minus 0.048 chance of getting blackjack, so:
chance_win - chance_blackjack = chance_even_odds_win


The chance to get B blackjacks in R rounds is calculated as

```math
\displaystyle P(k) = \prod_{k=1}^{N} \quad p(k)  \times \prod_{k=1}^{N} (1 - p(k) ) * \begin{pmatrix}rounds\cr bjCount\cr\end{pmatrix}
```
  
The last term is rounds choose bjCount where bjCount is the number of blackjacks this turn.

To calculate the combinations, use the choose function:
```math
\displaystyle \frac{D!}{B! (D - B)!}
```
  
where:
B = number of blackjacks you have got so far (denoted bj_count)
D = the number of initial deals so far (denoted deck_count)

The chance to get at leat B blackjacks in R rounds is calculated as 1 (100%) minus the sum of the chances of getting less than B blackjacks.

#### Chance of being caught
I have normalised the distribution as:

```math
P(caught) = C_{dealer }  C_{max }  \sigma  \sqrt{2} \times erf( \frac{w-m}{ \sigma \sqrt{2} }) - erf( \frac{m}{ \sigma \sqrt{2} })
```
