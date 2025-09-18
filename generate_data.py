import json
import random
import copy

def generate_abnormal_data():
    with open("./data/test.json", "r", encoding="utf-8") as f:
        new_data = []
        datas = json.load(f)
        datas_new = random.sample(datas, 350)
        for data in datas_new:
            problem = data["problem"]
            solution = data["solution"]
            answer = data["answer"]

            problem_interval_mix = int(len(problem)*0.5)
            problem_interval_max = int(len(problem)*0.5)

            solution_interval_mix = int(len(solution)*0.5)
            solution_interval_max = int(len(solution)*0.5)

            answer_interval_mix = int(len(answer)*0.5)
            answer_interval_max = int(len(answer)*0.5)

            problem_cut_start_index = random.randint(0, problem_interval_mix)
            data["problem"] = problem[problem_cut_start_index:problem_cut_start_index+problem_interval_max]

            solution_cut_start_index = random.randint(0, solution_interval_mix)
            data["solution"] = solution[solution_interval_max:solution_cut_start_index+solution_interval_max]

            answer_cut_start_index = random.randint(0, answer_interval_mix)
            data["answer"] = answer[answer_cut_start_index:answer_cut_start_index + answer_interval_max]

            new_data.append(data)

        with open("./data/test_350_score.json", "w", encoding="utf-8") as f_w:
            f_w.write(json.dumps(new_data, indent=4, ensure_ascii=False))


def generate_dedup_data():
    with open("./data/test.json", "r", encoding="utf-8") as f:
        new_data = []
        datas = json.load(f)
        datas_new = random.sample(datas, 15)
        for _ in range(0, 350):
            data = random.choice(datas_new)
            data = copy.deepcopy(data)
            problem = data["problem"]
            solution = data["solution"]
            answer = data["answer"]

            problem_interval_mix = int(len(problem)*0.5)
            problem_interval_max = int(len(problem)*0.5)

            solution_interval_mix = int(len(solution)*0.5)
            solution_interval_max = int(len(solution)*0.5)

            answer_interval_mix = int(len(answer)*0.5)
            answer_interval_max = int(len(answer)*0.5)

            problem_cut_start_index = random.randint(0, problem_interval_mix)
            data["problem"] = problem[problem_cut_start_index:problem_cut_start_index+problem_interval_max]

            solution_cut_start_index = random.randint(0, solution_interval_mix)
            data["solution"] = solution[solution_cut_start_index:solution_cut_start_index+solution_interval_max]

            answer_cut_start_index = random.randint(0, answer_interval_mix)
            data["answer"] = answer[answer_cut_start_index:answer_cut_start_index + answer_interval_max]

            new_data.append(data)

        with open("./data/test_350_dep.json", "w", encoding="utf-8") as f_w:
            f_w.write(json.dumps(new_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    generate_abnormal_data()
    # generate_dedup_data()



