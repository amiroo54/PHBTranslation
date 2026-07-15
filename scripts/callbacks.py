import requests

def gp_callback(*gp, term):
    return f"{int(gp[0]) * 1806} میلیون تومان"

def sp_callback(*gp, term):
    return f"{int(gp[0]) * 1806/10} میلیون تومان"

def cp_callback(*gp, term):
    return f"{int(gp[0]) * 1806/100} میلیون تومان"


def lb_callback(*lb, term):
    if "کیلو" in term:
        weight = lb[0].replace("½", ".5")
        kilo = eval(weight) / 2.205 
        kilo = round(kilo, 1)
        return term.replace("%", f"{kilo}") 
    else:
        pass

