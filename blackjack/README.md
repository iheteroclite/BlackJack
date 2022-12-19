## Blackjack Tech Test - Starter Code

This code is offered as a potential starting point for completing the BBC Software Engineering Graduate Scheme tech test.
You do **not** have to use this starter code.


### Getting started

- Ensure you can run the provided code. 
    - If you have Python 3 installed:
        - Open a terminal window and navigate to the folder containing this README.
        - Type `python3 blackjack.py`
        - Look for a welcome message in the console.
    - If that doesn't work, check your setup and download Python 3 if needed:
        - https://wiki.python.org/moin/BeginnersGuide/Download
- Ensure you can run the unit tests.
    - From the same terminal window, type `python3 -m unittest discover test`.
    - Python should find and run the one provided failing test.
    

### Adding to the starter code

- A great place to start is by making that first test pass.
    - Clue- the provided Deck class has an array of cards, and it's empty!
- A TDD (test-driven development) approach can be useful:
    - write a failing test that describes what you want your code to do
        - e.g. 'a deck should have 52 cards'
    - modify the code that you're testing so that the test passes
        - e.g. the deck actually *has* 52 cards!
- You can add more test files:
    - keep them in the `test/` directory
    - make sure they have filenames beginning with `test`
    - make sure test methods within those files also begin with `test`
- You can add more source files:
    - keep them in the `src/` directory
- You can use any approach you want
    - The provided code hints at an object-oriented approach (since we have a Deck class)
    - if you wanted to extend this approach, you might want to create classes for Hand, Card, Dealer, etc.
    
### Completing the task

- Remember, the task is to write code that accurately scores a hand of blackjack, *not* to make a whole game
- This means you *don't* need to have a running program to complete this test
    - You can just prove your code works with unit tests
- You can *choose* to make a running program that demonstrates that your code works
    - If you want to do this, you should extend the `play` method of `blackjack.py`
    - This method is the entry point when you do `python3 blackjack.py`.
