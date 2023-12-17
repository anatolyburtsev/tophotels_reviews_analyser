import json
from openai import OpenAI
from dotenv import load_dotenv


def answer_question(question: str, data: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system",
             "content": f"You are a hotel assistant for a major worldwide tourism company. You have access to all "
                        f"reviews for a given hotel. Each review has the following format: [date, positive things, "
                        f"negative things]. Providing response to customer please cite significant chunk of original "
                        f"review with date. Reviews: {data}"},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    load_dotenv()
    hotel_id = "al22319"
    with open(f"scores_{hotel_id}.json", 'r') as r:
        scores = json.load(r)

        q = "Жаловался ли кто-то на тараканов, мух или комаров?"
        print(answer_question(q, scores))
