"""Created when doing homework for Johns Hopkins Class.

   Statistical Reasoning for Public Health 1: Estimation, Inference, & Interpretation
   by John McGready, PhD, MS

   Examples are found in <biocode>/Test/kaplanmeier directory.

   Trivia from Lecture 5C: (11:51)
   Kaplan and Meier were not collaborators.  They serendipitously submitted
   manuscripts to the same journal at the same time regarding how to handle
   time-to-event data.  The Editor suggested that they meet up and write a
   paper together. Dr. Meier was from Johns Hopkins University.
"""

import sys
import collections as cx

class KaplanMeier():

  def __init__(self, data):
    # Event times are represented by positive numbers.
    # Censoring times are represented by negative numbers.
    self.data = data

  def get_cumulative_survival(self, PRT=None):
    """Stats 1: Lec. 5C: Time to Event Data: Graphical Summarization: Kaplan-Meier."""
    # S(t) = Proportion of population remaining event free (surviving) 
    # at least to time t or beyond.
    # 1. Order the data
    self.chk_sorted(self.data) # User must supply sorted data.
    data_queue = cx.deque(self.data)
    S = 1 # S(0) = 1, No participants have had the event at t=0.
    et_prev = None
    for et in self.data:
      # Start estimate at first (ordered) event time
      if et != et_prev:
        if data_queue and data_queue[0] < 0:
          # The probability (proportion) of survival (remaining event free)
          # does not change at censoring times.
          self.censor(data_queue, et, PRT)
        if et > 0:
          S = self.get_S(data_queue, et, S, PRT)
        et_prev = et
    return S
      
  def get_S(self, data_queue, t, S_prev, PRT):
    """Calculate the Survival Curve."""
    # Returns the estimated proportion of the original sample of 
    # participants who survived (did not have the event) by the
    # corresponding follow-up time.
    
    # From Stats 1 Lecture 5C: (12:00)
    #
    #        |<--- A(t) -->|   |<---- B(t) -------->|
    #
    # ^      / N(t) - E(t) \   ^
    # S(t) = | ----------- | * S(Previous Event Time)
    #        \     N(t)    /
    # ^
    # S(t) = (Proportion of people who did not have the event at time t) *
    #        (Proportion of original sample surviving (remaining event free) beyond time t
    #
    # A(t): Proportion surviving to time to who survive beyond time t (14:58)
    # B(t): Proportion of original sample surviving (remaining event free) beyond 
    #       previous event time before current, time t.
    #
    # S(t): Cumulative Survival: Proportion of Original Sample still event free at time=t
    # N(t): Number at risk of having the event at time=t
    # E(t): Number of people who had the event at time=t

    # The probability (proportion) of survival (remaining event free)
    # does not change at censoring times.

    # t=0: By defn all subjects are event free ("alive") at beginning of the study.
    if t == 0:
      return 1
    E = data_queue.count(t) # # who had event at time t
    N = len(data_queue)     # # at risj of having event at time t
    C = float(N - E)/N 
    S = C * S_prev
    if PRT is not None:
      PRT.write("{t:>3}=t S({S:4.2f}) = ([N({N})-E({E})/N({N})] = {C:4.2f}) * S_prev({Sp:4.2f}) {D}\n".format(
      t=t, N=N, E=E, Sp=S_prev, S=S, 
      #D=' '.join(map(str,data_queue)), 
      D="",
      C=C))
    for i in range(E):
      data_queue.popleft()
    return S

  def censor(self, data_queue, t, PRT):
    """Remove data censored at time t from queue."""
    E = data_queue.count(t if t<0 else -1*t)
    for i in range(E):
      data_queue.popleft()
    if PRT is not None:
      PRT.write("{:>3}=t             N({}) after censoring\n".format(t, len(data_queue)))

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

  @staticmethod
  def get_sorted(data):
    """Sorts data by even time and abs(censoring time)."""
    return [d for d in sorted(data, key=lambda d: abs(d))]

  def chk_sorted(self, data):
    """Checks that data is sorted by abs value."""
    lst_abs = [abs(d) for d in data]
    if lst_abs == sorted(lst_abs):
      return
    raise Exception("LIST IS NOT SORTED: {}".format(data))

  def prt_data_sorted(self, PRT=sys.stdout):
    PRT.write(", ".join(map(str, self.get_sorted(self.data))))
    
  

