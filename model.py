"""Win-probability model for Faceoff.

Kept deliberately simple and swappable: replace win_prob() with an
Impact Rating–based model and nothing else in the app has to change.
"""

HOME_EDGE = 0.035   # league-average home-ice bump
PRIOR_GP = 20       # games of 0.500 prior to regress early-season noise


def _strength(pct, gp):
    return (pct * gp + 0.5 * PRIOR_GP) / (gp + PRIOR_GP)


def win_prob(home, away, table):
    """Probability the home team wins, using log5 on regressed point %."""
    ph = _strength(*table.get(home, (0.5, 0)))
    pa = _strength(*table.get(away, (0.5, 0)))
    p = (ph * (1 - pa)) / (ph * (1 - pa) + pa * (1 - ph))
    return round(min(0.95, max(0.05, p + HOME_EDGE)), 3)
