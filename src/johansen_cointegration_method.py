from statsmodels.tsa.vector_ar.vecm import coint_johansen
import numpy as np
import pandas as pd
import more_itertools
import itertools

def johansen_test(df: pd.DataFrame) -> list:    
    
    # Create all combinations of stocks regardless of order of appearance 
    all_pairs = list(itertools.combinations(df.columns.tolist(), 2))

    cointegrating_pairs = []
    
    cointegration_pairs = []

    for i, (sid_1, sid_2) in enumerate(all_pairs):

        pair_closes = df[[sid_1, sid_2]].dropna()

        # The second and third parameters indicate constant term, with a lag of 1.
        # See Chan, Algorithmic Trading, chapter 2.
        result = coint_johansen(pair_closes, 0, 1)

        # the 90%, 95%, and 99% confidence levels for the trace statistic and maximum
        # eigenvalue statistic are stored in the first, second, and third column of
        # cvt and cvm, respectively
        confidence_level_cols = {
            90: 0,
            95: 1,
            99: 2
        }
        confidence_level_col = confidence_level_cols[95]

        trace_crit_value = result.cvt[:, confidence_level_col]
        eigen_crit_value = result.cvm[:, confidence_level_col]

        # The trace statistic and maximum eigenvalue statistic are stored in lr1 and lr2;
        # see if they exceeded the confidence threshold

        # if np.all(result.lr1[0] >= trace_crit_value[0]) and np.all(result.lr2[0] >= eigen_crit_value[0]):
        # not checking for eigenvalue

        if np.all(result.lr1[0] >= trace_crit_value[0]):

            # Append the cointegrating pair as a list [sid_1, sid_2]
            cointegrating_pairs.append([sid_1, sid_2])
            cointegration_pairs.append([sid_1, sid_2])
            
    return cointegration_pairs
