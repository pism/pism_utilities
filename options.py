#!/usr/bin/env python

"""Helper functions for generating common command-line options used in
PISM runs.

"""

__version__ = "0.1"

from collections import OrderedDict
import os

def spatial_ts(outfile, exvars, step, start=None, end=None, split=None, odir=None):
    """
    Return dict to generate spatial time series

    Returns: OrderedDict
    """

    # check if list or comma-separated string is given.
    try:
        exvars = ",".join(exvars)
    except:
        pass

    params_dict = OrderedDict()
    if split is True:
        outfile, ext = os.path.splitext(outfile)
        params_dict["extra_split"] = ""
    if odir is None:
        params_dict["extra_file"] = "ex_" + outfile
    else:
        params_dict["extra_file"] = os.path.join(odir, "ex_" + outfile)
    params_dict["extra_vars"] = exvars

    if step is None:
        step = "yearly"

    if start is not None and end is not None:
        times = "{start}:{step}:{end}".format(start=start, step=step, end=end)
    else:
        times = step

    params_dict["extra_times"] = times

    return params_dict


def scalar_ts(outfile, step, odir=None, **kwargs):
    """
    Return dict to create scalar time series

    Returns: OrderedDict
    """

    params_dict = OrderedDict()
    if odir is None:
        params_dict["ts_file"] = "ts_" + outfile
    else:
        params_dict["ts_file"] = os.path.join(odir, "ts_" + outfile)

    if step is None:
        step = "yearly"
    else:
        times = step
    params_dict["ts_times"] = times

    return params_dict


def snap_shots(outfile, times, odir=None):
    """
    Return dict to generate snap shots

    Returns: OrderedDict
    """

    params_dict = OrderedDict()
    if odir is None:
        params_dict["save_file"] = "save_" + outfile.split(".nc")[0]
    else:
        params_dict["save_file"] = os.path.join(odir, "save_" + outfile.split(".nc")[0])

    params_dict["save_times"] = ",".join(str(e) for e in times)
    params_dict["save_split"] = ""
    params_dict["save_force_output_times"] = ""

    return params_dict

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.

    Returns: OrderedDict
    """
    result = OrderedDict()
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def uniquify(seq, idfun=None):
    """
    Remove duplicates from a list, order preserving.
    From http://www.peterbe.com/plog/uniqifiers-benchmark
    """

    if idfun is None:

        def idfun(x):
            return x

    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def stress_balance(stress_balance, additional_params_dict):
    """
    Generate stress balance params

    Returns: OrderedDict
    """

    accepted_stress_balances = ("sia", "ssa+sia")

    if stress_balance not in accepted_stress_balances:
        print(("{} not in {}".format(stress_balance, accepted_stress_balances)))
        print(("available stress balance solvers are {}".format(accepted_stress_balances)))
        import sys

        sys.exit(0)

    params_dict = OrderedDict()
    params_dict["stress_balance"] = stress_balance
    if stress_balance in ("ssa+sia"):
        params_dict["options_left"] = ""
        params_dict["cfbc"] = ""
        params_dict["kill_icebergs"] = ""
        params_dict["part_grid"] = ""
        params_dict["part_redist"] = ""
        params_dict["sia_flow_law"] = "gpbld"
        params_dict["pseudo_plastic"] = ""
        params_dict["tauc_slippery_grounding_lines"] = ""

    return merge_dicts(additional_params_dict, params_dict)


def hydrology(hydro, **kwargs):
    """
    Generate hydrology params

    Returns: OrderedDict
    """

    params_dict = OrderedDict()
    if hydro in ("null"):
        params_dict["hydrology"] = "null"
    elif hydro in ("diffuse"):
        params_dict["hydrology"] = "null"
        params_dict["hydrology_null_diffuse_till_water"] = ""
    elif hydro in ("routing"):
        params_dict["hydrology"] = "routing"
    elif hydro in ("steady"):
        params_dict["hydrology"] = "steady"
    elif hydro in ("routing_coupled"):
        params_dict["hydrology"] = "routing"
    elif hydro in ("distributed"):
        params_dict["hydrology"] = "distributed"
        params_dict["basal_yield_stress.add_transportable_water"] = "true"
    elif hydro in ("distributed_coupled"):
        params_dict["hydrology"] = "distributed"
        params_dict["basal_yield_stress.add_transportable_water"] = "true"
    else:
        print(("hydrology {} not recognized, exiting".format(hydro)))
        import sys

        sys.exit(0)

    return merge_dicts(params_dict, kwargs)


def calving(calving, **kwargs):
    """
    Generate calving params

    Returns: OrderedDict
    """

    params_dict = OrderedDict()
    if calving in ("thickness_calving", "hayhurst_calving"):
        params_dict["calving"] = calving
    elif calving in ("vonmises_nofloat_calving"):
        params_dict["calving"] = "vonmises_calving,float_kill".format(calving)
    elif calving in ("eigen_calving", "vonmises_calving"):
        params_dict["calving"] = "{},thickness_calving".format(calving)
    elif calving in ("hybrid_calving"):
        params_dict["calving"] = "eigen_calving,vonmises_calving,thickness_calving"
    elif calving in ("float_kill", "float_kill,ocean_kill", "vonmises_calving,ocean_kill", "eigen_calving,ocean_kill"):
        params_dict["calving"] = calving
    else:
        print(("calving {} not recognized, exiting".format(calving)))
        import sys

        sys.exit(0)
    if "frontal_melt" in kwargs and kwargs["frontal_melt"] is True:
        params_dict["calving"] += ",frontal_melt"
        # need to delete the entry
        del kwargs["frontal_melt"]
    return merge_dicts(params_dict, kwargs)
