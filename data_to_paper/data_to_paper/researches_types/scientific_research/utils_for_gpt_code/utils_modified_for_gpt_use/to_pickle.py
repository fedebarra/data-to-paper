import pickle
from typing import Dict

import pandas as pd
from pandas.core.frame import DataFrame

from data_to_paper.run_gpt_code.base_run_contexts import RegisteredRunContext
from data_to_paper.run_gpt_code.overrides.attr_replacers import AttrReplacer
from data_to_paper.run_gpt_code.overrides.types import PValue
from data_to_paper.run_gpt_code.types import RunIssue, CodeProblem, RunUtilsError

from .check_df_of_table import check_df_of_table_for_content_issues


def dataframe_to_pickle_with_checks(df: pd.DataFrame, path: str, *args,
                                    original_func=None, context_manager: AttrReplacer = None, **kwargs):
    """
    Save a data frame to a csv file.
    Check for content issues.
    """
    if hasattr(context_manager, 'prior_tables'):
        prior_tables: Dict[str, pd.DataFrame] = context_manager.prior_tables
    else:
        prior_tables = {}
        context_manager.prior_tables = prior_tables
    prior_tables[path] = df

    if args or kwargs:
        raise RunUtilsError(issue=RunIssue(
            issue="Please use `to_pickle(path)` with only the `path` argument.",
            instructions="Please do not specify any other arguments.",
            code_problem=CodeProblem.RuntimeError,
        ))

    if not isinstance(path, str):
        raise RunUtilsError(issue=RunIssue(
            issue="Please use `to_pickle(filename)` with a filename as a string argument in the format 'table_x'",
            code_problem=CodeProblem.RuntimeError,
        ))
    context_manager.issues.extend(check_df_of_table_for_content_issues(df, path, prior_tables=prior_tables))
    with RegisteredRunContext.temporarily_disable_all():
        original_func(df, path)


def get_dataframe_to_pickle_attr_replacer():
    return AttrReplacer(cls=DataFrame, attr='to_pickle', wrapper=dataframe_to_pickle_with_checks,
                        send_context_to_wrapper=True, send_original_to_wrapper=True)


def pickle_dump_with_checks(obj, file, *args, original_func=None, context_manager: AttrReplacer = None, **kwargs):
    """
    Save a Dict[str, Any] to a pickle file.
    Check for content issues.
    """
    if args or kwargs:
        raise RunUtilsError(issue=RunIssue(
            issue="Please use `dump(obj, file)` with only the `obj` and `file` arguments.",
            instructions="Please do not specify any other arguments.",
            code_problem=CodeProblem.RuntimeError,
        ))

    # Check if the object is a dictionary
    if isinstance(obj, DataFrame):
        raise RunUtilsError(issue=RunIssue(
            issue="Please use `pickle.dump` only for saving the dictionary."
                  "Use `df.to_pickle(filename)` for saving the table dataframes.",
            code_problem=CodeProblem.RuntimeError,
        ))

    if not isinstance(obj, dict):
        raise RunUtilsError(issue=RunIssue(
            issue="Please use `pickle.dump` only for saving the dictionary `obj`.",
            code_problem=CodeProblem.RuntimeError,
        ))

    # Check if the keys are strings
    if not all(isinstance(key, str) for key in obj.keys()):
        context_manager.issues.append(RunIssue(
            issue="Please use `dump(obj, filename)` with a dictionary `obj` with string keys.",
            code_problem=CodeProblem.RuntimeError,
        ))

    original_func(obj, file)


def get_pickle_dump_attr_replacer():
    return AttrReplacer(cls=pickle, attr='dump', wrapper=pickle_dump_with_checks,
                        send_context_to_wrapper=True, send_original_to_wrapper=True)
