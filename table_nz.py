import pandas as pd
from IPython.display import display
import csv

Ku = int(input("Please enter a value for proportional gain : "))
# then we are increasing our Kp until Oscillations turn into neutral stability

Tu = float(input("Please enter a value for period : "))  # time of Oscillation in seconds

data = {'Control Type': ['PID (classic)', 'P', 'PI', 'PD',
                         'Lessen Integration', 'Some Overshoot', 'No Overshoot'],
        'Кр': [0.6 * Ku, 0.5 * Ku, 0.45 * Ku, 0.8 * Ku, 0.7 * Ku, Ku / 3, 0.2 * Ku],
        'Ti': [Tu / 2, '-', Tu / 1.2, '-', 2 * Tu / 5, Tu / 2, Tu / 2],
        'Td': [Tu / 8, '-', '-', Tu / 8, 3 * Tu / 20, Tu / 3, Tu / 3],
        'Ki = Кр/Ti': [1.2 * Ku / Tu, '-', 0.54 * Ku / Tu, '-', 1.75 * Ku / Tu,
                       (2 / 3) * Ku / Tu, (2 / 5) * Ku / Tu],
        'Kd = Td*Kp': [0.075 * Ku * Tu, '-', '-', 0.1 * Ku * Tu, 0.105 * Ku * Tu,
                       (1 / 9) * Ku / Tu, (1 / 15) * Ku / Tu]
        }

df = pd.DataFrame(data)
df.to_csv('nz_calculating.csv', sep=',')
display(df)
