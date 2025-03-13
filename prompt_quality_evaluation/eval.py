import json
import argparse
from typing import List, Dict, Any, Union
from openai import OpenAI
from prompt import comprehensive_zh_prompt
from parse_output import parse_json
from tqdm import tqdm
from loguru import logger

from config import QUESTIONS, ANSWER



def openai_post(
    messages: List[Dict[str, str]], api_key: str, api_url: str
) -> Union[Dict[str, Any], str]:
    """
    Sends a chat request to the OpenAI API and returns the parsed response.

    Args:
        messages (List[Dict[str, str]]): The chat messages to send.
        api_key (str): The API key for authentication.
        api_url (str): The API base URL.

    Returns:
        Union[Dict[str, Any], str]: Parsed JSON response if successful, otherwise an error message.
    """
    try:
        llm = OpenAI(api_key=api_key, base_url=api_url)
        model_name = llm.models.list().data[0].id

        response = llm.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            top_p=0.8,
        )

        json_response = parse_json(
            response.to_dict()["choices"][0]["message"]["content"]
        )
        return (
            json_response
            if isinstance(json_response, dict)
            else "Invalid JSON response"
        )

    except Exception as e:
        return f"Error: {str(e)}"


def calculate_score(
    api_key: str,
    api_url: str,
    score_threshold: int,
    data_path: str,
    abnormal_path: str,
    new_data_path: str,
) -> None:
    """
    Processes input data, evaluates scores via OpenAI API, and categorizes data
    into normal and abnormal based on the score threshold.

    Args:
        api_key (str): The API key for authentication.
        api_url (str): The API base URL.
        score_threshold (int): The threshold below which a score is considered abnormal.
        data_path (str): Path to the input JSON file.
        abnormal_path (str): Path to save the abnormal data.
        new_data_path (str): Path to save the normal data.

    Returns:
        None
    """

    count = 0
    abnormal_data = []
    new_data = []

    with open(data_path, "r", encoding="utf-8") as f:
        datas: List[Dict[str, Any]] = json.load(f)
        total_count = len(datas)
        for data in tqdm(datas, desc="Processing"):
            prompt = comprehensive_zh_prompt.format_map(
                {
                    "history": "",
                    "input": "\n".join([data.get(input_key, "") for input_key in QUESTIONS]),
                    "output": "\n".join([data.get(output_key, "") for output_key in ANSWER]),
                }
            )
            messages = [
                {"role": "system", "content": prompt},
                {"role": "usr", "content": "按照以上要求开始评估"},
            ]
            res = openai_post(messages, api_key, api_url)

            if isinstance(res, dict):
                print(res)
                data.update(res)
                if res.get("score", 1) < score_threshold:
                    abnormal_data.append(data)
                    count += 1
                else:
                    new_data.append(data)   
            else:
                data.update({"error_info": str(res)})
                abnormal_data.append(data)
                count += 1

    with open(abnormal_path, "w", encoding="utf-8") as f_a, open(
        new_data_path, "w", encoding="utf-8"
    ) as f_n:
        json.dump(abnormal_data, f_a, indent=4, ensure_ascii=False)
        json.dump(new_data, f_n, indent=4, ensure_ascii=False)

    logger.info(
        f"本次共检测了 {total_count} 条数据, 评分低于 {score_threshold} 的数据有 {count} 条"
    )
    logger.info("异常检出率为：{:.2%}".format(count / total_count))


def main():
    parser = argparse.ArgumentParser(description="Run anomaly detection scoring.")
    parser.add_argument("--api_key", type=str, required=True, help="API key for authentication")
    parser.add_argument("--api_url", type=str, required=True, help="API URL endpoint")
    parser.add_argument("--score_threshold", type=int, default=7, help="Threshold for anomaly score (1-10)")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the input data file")
    parser.add_argument("--save_abnormal_data_path", type=str, required=True, help="Path to save abnormal data")
    parser.add_argument("--save_new_data_path", type=str, required=True, help="Path to save normal data")
    
    args = parser.parse_args()
    
    calculate_score(
        args.api_key,
        args.api_url,
        args.score_threshold,
        args.data_path,
        args.save_abnormal_data_path,
        args.save_new_data_path,
    )


if __name__ == "__main__":
    main()



