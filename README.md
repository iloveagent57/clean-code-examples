# clean-code-examples
Let's pretend for a moment that we have the power to periodically provide adequate funding to the MBTA.

(I can dream, damn it.)

Suppose there's a magical API endpoint through which we can deliver such funds.  We'd like to make POST
requests to this endpoint, record somewhere that we have made this transaction, check the status of
our transation, and then display a receipt for our generous funding.

We have multiple things to do.  We also want to demonstrate here two code smells:
1) Functions should only do "one thing".
2) Functions should only descend one level of abstraction.
