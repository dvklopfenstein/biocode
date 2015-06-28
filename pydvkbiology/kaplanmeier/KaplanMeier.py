"""Created when doing homework for Johns Hopkins Class.

   Statistical Reasoning for Public Health 1: Estimation, Inference, & Interpretation
   by John McGready, PhD, MS

   Examples are found in <biocode>/Test/kaplanmeier directory.

   Trivia from Lecture 5C:
   Kaplan and Meier were not collaborators.  They serendipitously submitted
   manuscripts to the same journal at the same time regarding how to handle
   time-to-event data.  The Editor suggested that they meet up and write a
   paper together.
"""

import sys
import collections as cx

class KaplanMeier():

  def __init__(self, data):
    # Event times are represented by positive numbers.
    # Censoring times are represented by negative numbers.
    self.data = data

  def get_cumulative_survival(self):
    """Stats 1: Lec. 5C: Time to Event Data: Graphical Summarization: Kaplan-Meier."""
    # S(t) = Proportion of population remaining event free (surviving) 
    # at least to time t or beyond.
    # 1. Order the data
    orig = self.get_sorted(self.data)
    data_queue = cx.deque(orig)
    S = 1 # S(0) = 1
    for et in self.get_sorted(self.data):
      # Start estimate at first (ordered) event time
      if data_queue[0] < 0:
        self.censor(data_queue, et)
      if et > 0:
        S = self.get_S(data_queue, et, S)
      
  def get_S(self, data_queue, t, S_prev):
    """Calculate the Survival Curve."""
    # Returns the estimated proportion of the original sample of 
    # participants who survived (did not have the event) by the
    # corresponding follow-up time.
    
    # From Stats 1 Lecture 5C:
    #
    # ^      / N(t) - E(t) \   ^
    # S(t) = | ----------- | * S(Previous Event Time)
    #        \     N(t)    /
    # ^
    # S(t) = (Proportion of people who did not have the event at time t) *
    #        (Proportion of original sample surviving (remaining event free) beyond time t

    # S(t): Cumulative Survival: Proportion of Original Sample still event free at time=t
    # N(t): # at risk of having the event at time=t
    # E(t): # of people who had the event at time=t

    # The probability (proportion) of survival (remaining event free)
    # does not change at censoring times.

    # t=0: By defn all subjects are event free ("alive") at beginning of the study.
    if t == 0:
      return 1
    E = data_queue.count(t) # # who had event at time t
    N = len(data_queue)     # # at risj of having event at time t
    S = float(N - E)/N * S_prev
    print "{:>3}=t {:>2}=N {:>2}=E {:6.3f} {:6.3f} {}".format(
      t, N, E, S_prev, S, data_queue)
    for i in range(E):
      data_queue.popleft()
    return S

  def censor(self, data_queue, t):
    """Remove data censored at time t from queue."""
    E = data_queue.count(t if t<0 else -1*t)
    #print t, E
    for i in range(E):
      data_queue.popleft()

  def get_events(self):
    """Return events."""
    return [d for d in self.data if d > 0]

  def get_followuptimes(self):
    """Return follow-up times."""
    return [abs(d) for d in self.data]

  def get_IR(self, time=None):
    """Calculate "Incidence Rate" in the follow-up period."""
    # IR = (# events)/(total follow-up time)
    return len(self.get_events)/sum(self.get_followuptimes())

  def get_sorted(self, data):
    """Sorts data by even time and abs(censoring time)."""
    return [d for d in sorted(data, key=lambda d: abs(d))]

  def prt_data_sorted(self, PRT=sys.stdout):
    PRT.write(", ".join(map(str, self.get_sorted(self.data))))
    
  

