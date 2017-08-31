# Connect4 AI

Bot that won second place in the Connect 4 competition, as part of the Fall '16
Elements of AI class

## Code structure

- board.py - Board representation using bitboards
- player.py - Alpha-beta Minimax search

- test.py
  - test_Q1()- test board representation
  - test_Q2()- perft (performance test) for given depth. Compares nodes expanded to known value
  - test_Q3()- tests if specific win situations work
  - manual_test()- tests bot vs human
  - time_test()- checks how long it takes to search to specific depth, and a comparison of the nodes expanded by vanilla
  minimax and alpha-beta minimax with optimizations
  
- manual.py- bot that allows manual input of moves. Used in manual_test()
- search.py- implements perft used in test_Q2()
- notes.txt - changelog, journal thingy
