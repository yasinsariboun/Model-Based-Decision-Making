from __future__ import (unicode_literals, print_function, absolute_import,
                        division)


from ema_workbench import (Model, MultiprocessingEvaluator,
                           ScalarOutcome, IntegerParameter, optimize, Scenario)
from ema_workbench.em_framework.optimization import EpsilonProgress
from ema_workbench.util import ema_logging
from ema_workbench import Constraint
from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(6)
#we base reference values on mean worst case damage scenario
    reference_values = {'discount rate 0': 4.5, 'discount rate 1': 2.5, 'discount rate 2': 3.5, 'A.0_ID flood wave shape': 41,
                        'A.1_Bmax': 129, 'A.1_pfail': 0.024, 'A.1_Brate': 1.5,
                        'A.2_Bmax': 291, 'A.2_pfail': 0.59, 'A.2_Brate': 10,
                        'A.3_Bmax': 196, 'A.3_pfail': 0.68, 'A.3_Brate': 10,
                        'A.4_Bmax': 240, 'A.4_pfail': 0.41, 'A.4_Brate': 10,
                        'A.5_Bmax': 107, 'A.5_pfail': 0.60, 'A.5_Brate': 1.5}
    scen1 = reference_values

    constraints = [Constraint("Max_death_rate", outcome_names='Expected Number of Deaths 0',
                             function=lambda x: max(0, x - 0.001)),
                   Constraint("Max_death_rate", outcome_names='Expected Number of Deaths 1',
                              function=lambda x: max(0, x - 0.001)),
                   Constraint("Max_death_rate", outcome_names='Expected Number of Deaths 2',
                              function=lambda x: max(0, x - 0.001))
                   ]
    # for key in model.uncertainties:
    #     name_split = key.name.split('_')
    #
    #     if len(name_split) == 1:
    #         scen1.update({key.name: reference_values[key.name]})
    #
    #     else:
    #         scen1.update({key.name: reference_values[name_split[1]]})

    ref_scenario = Scenario('reference', **scen1)
    print(ref_scenario)

    convergence_metrics = [EpsilonProgress()]
    #initial epsilon was 1e3 = 1000
    espilon = [50000, 50000, 0.00001]

    nfe = 25000 # proof of principle only, way to low for actual use

    with MultiprocessingEvaluator(model) as evaluator:
        results, convergence = evaluator.optimize(nfe=nfe, searchover='levers',
                                                  epsilons=espilon,
                                                  convergence=convergence_metrics,
                                                  reference=ref_scenario,
                                                  constraints=constraints)

    # fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True)
    # fig, ax1 = plt.subplots(ncols=1)
    # ax1.plot(convergence.epsilon_progress)
    # ax1.set_xlabel('nr. of generations')
    # ax1.set_ylabel('$\epsilon$ progress')
    # sns.despine()
    # print(results)

    results.to_csv('optimize_median_deaths.csv')
    convergence.to_csv('convergence_median_deaths.csv')