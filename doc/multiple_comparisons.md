# Multiple Comparison Issue 

* [Multiple Comparison Issue in Pictures](#Multiple Comparison Issue in Pictures)
* [Multiple Comparison Issue Explained](#Multiple Comparison Issue Explained)

## Multiple Comparison Issue in Pictures
![XKCD Jelly Beans](significant.png)

## Multiple Comparison Issue Explained

From Geoffrey Brent, Melbourne, Victoria, Australia

Be careful what you ask for ;-)

The key concept here is that **"probability of X being true,
given the information that Y is true"** is not the same as
**"probability of Y being true, given that X is true"**.

For example: let's suppose I have a pile of 10000 coins in
front of me. I know that 9999 of them are normal, unbiased
coins, with 'heads' on one side and 'tails' on the other.
The other one is a trick coin with heads on both sides. I
want to find the trick coin. 

Because I'm a statistician, instead of doing this the
sensible way and checking both sides of the coin, I decide
to use a random test. I'm going to take each coin, toss it 5
times, and see what comes up. If it comes up tails even
once, I'll identify it as a normal coin; if all 5 trials
come up heads (HHHHH), I'll declare it to be a trick coin -
it passes my "trick coin" test.

Clearly, if I test the trick coin, I'm guaranteed to
identify it as a trick coin. 

But if I test a normal coin, what is the probability that
I'll mistakenly identify it as the trick coin? Well, for an
unbiased coin, the chance of coming up HHHHH is 1/2 x 1/2 x
1/2 x 1/2 x 1/2 = 1/32, or about **3%**. This is the
**"significance level"** for the test I'm using: the **probability
for any one normal coin that I'll mistakenly ID it as
double-headed**. It's also known as the **"false positive rate"**
or **"p-value"**. 

So let's say I test all 10000 of those coins. I will
correctly flag the trick coin. But when I test the normal
coins, my error rate is 1/32, so I will flag about 9999/32
or 312 of them as trick coins.

In other words: I've identified 313 "trick coins" but only
one of them is a genuine trick coin. The other 312 are just
normal coins that happened to come down heads 5 times in a
row.

So: given that a coin is normal, the chance it'll pass my
"trick coin" test (i.e. my test makes a mistake) is only 3%.
If I describe that as "3% error rate", that sounds pretty
good!

But, given that a coin passes my "trick coin" test, the
chance that it's a normal coin (i.e. my test has made a
mistake) is 312/313, or 99.7%. (This measure is the **"false
discovery rate"**.) An error rate of 99.7% doesn't sound so
good!

The surveysystem.com explanation confuses these two measures
of reliability. It's a very common mistake, but depressing
to see it coming from a research company!

The underlying problem here is that in many, many types of
experiments, p-values aren't a very good measure of accuracy
(and even when they are, they need careful interpretation)
but they are very convenient to calculate. In the example
above, the only thing I need to know in order to get the
p-value is the behaviour of a normal coin. I don't need to
know anything at all about trick coins.

False discovery rates are often much more important, but
they're hard to calculate. To get the false discovery rate
above, I needed to know how a trick coin behaves (in this
case I've assumed all trick coins are two-headed - but what
if some of them are two-tailed, or if there are weighted
coins that come up heads two times out of three?) And I also
needed to know how common they are in the population; if
there were 1000 trick coins instead of just one, the false
discovery rate would be around 25% instead of 99.7%.

In many types of experiment, you simply don't have the
information you need in order to calculate something like
the false discovery rate. 

So people use the measure that's easiest to calculate, and
then very often they misinterpret what it actually means.

More info:
https://en.wikipedia.org/wiki/Sensitivity_and_specificity

***Sensitivity***: ***True Positive Rate*** (complementary to the ***False Negative rate***)    
***Specificity***: ***True Negative Rate*** (complementary to the ***False Positive rate***)



