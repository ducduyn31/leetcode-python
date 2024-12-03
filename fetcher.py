import json
from dataclasses import dataclass
from typing import List, Optional

import requests

PROBLEMS_URL = "https://leetcode.com/api/problems/algorithms/"
GRAPHQL_URL = "https://leetcode.com/graphql"
QUESTION_QUERY_STRING = """
query questionData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        content
        stats
        codeDefinition
        sampleTestCase
        metaData
    }
}
"""
QUESTION_QUERY_OPERATION = "questionData"


@dataclass
class CodeDefinition:
    value: str
    text: str
    default_code: str


@dataclass
class Problem:
    title: str
    title_slug: str
    content: str
    code_definition: List[CodeDefinition]
    sample_test_case: str
    difficulty: str
    question_id: int
    return_type: str


@dataclass
class Stat:
    question_id: int
    question_article_slug: Optional[str]
    question_title: Optional[str]
    question_title_slug: Optional[str]
    question_hide: bool
    total_acs: int
    total_submitted: int
    frontend_question_id: int
    is_new_question: bool


@dataclass
class Difficulty:
    level: int

    def __str__(self) -> str:
        return {1: "Easy", 2: "Medium", 3: "Hard"}.get(self.level, "Unknown")


@dataclass
class StatWithStatus:
    stat: Stat
    difficulty: Difficulty
    paid_only: bool
    is_favor: bool
    frequency: int
    progress: int


@dataclass
class Problems:
    user_name: str
    num_solved: int
    num_total: int
    ac_easy: int
    ac_medium: int
    ac_hard: int
    stat_status_pairs: List[StatWithStatus]


def get_problems() -> Optional[Problems]:
    response = requests.get(PROBLEMS_URL)
    if response.status_code != 200:
        return None
    data = response.json()
    return Problems(
        user_name=data["user_name"],
        num_solved=data["num_solved"],
        num_total=data["num_total"],
        ac_easy=data["ac_easy"],
        ac_medium=data["ac_medium"],
        ac_hard=data["ac_hard"],
        stat_status_pairs=[
            StatWithStatus(
                stat=Stat(
                    question_id=item["stat"]["question_id"],
                    question_article_slug=item["stat"]["question__article__slug"],
                    question_title=item["stat"]["question__title"],
                    question_title_slug=item["stat"]["question__title_slug"],
                    question_hide=item["stat"]["question__hide"],
                    total_acs=item["stat"]["total_acs"],
                    total_submitted=item["stat"]["total_submitted"],
                    frontend_question_id=item["stat"]["frontend_question_id"],
                    is_new_question=item["stat"]["is_new_question"],
                ),
                difficulty=Difficulty(item["difficulty"]["level"]),
                paid_only=item["paid_only"],
                is_favor=item["is_favor"],
                frequency=item["frequency"],
                progress=item["progress"],
            )
            for item in data["stat_status_pairs"]
        ],
    )


def get_problem(frontend_question_id: int) -> Optional[Problem]:
    problems = get_problems()
    if not problems:
        print("Failed to fetch problems.")
        return None
    for problem_stat in problems.stat_status_pairs:
        if problem_stat.stat.frontend_question_id == frontend_question_id:
            if problem_stat.paid_only:
                return None

            query = {
                "operationName": QUESTION_QUERY_OPERATION,
                "variables": {"titleSlug": problem_stat.stat.question_title_slug},
                "query": QUESTION_QUERY_STRING,
            }
            response = requests.post(GRAPHQL_URL, json=query)
            if response.status_code != 200:
                print(
                    f"Failed to fetch problem {problem_stat.stat.frontend_question_id}."
                )
                return None
            data = response.json()["data"]["question"]
            return Problem(
                title=problem_stat.stat.question_title or "Unknown",
                title_slug=problem_stat.stat.question_title_slug or "unknown",
                code_definition=[
                    CodeDefinition(
                        value=code_def["value"],
                        text=code_def["text"],
                        default_code=code_def["defaultCode"],
                    )
                    for code_def in json.loads(data["codeDefinition"])
                ],
                content=data["content"],
                sample_test_case=data["sampleTestCase"],
                difficulty=str(problem_stat.difficulty),
                question_id=problem_stat.stat.frontend_question_id,
                return_type=json.loads(data["metaData"])["return"]["type"],
            )
    return None
