from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def generate_variations(original_post):
    prompt = f"""
Create 4 alternative versions of this LinkedIn post.

1) Strong opening
2) Short and crisp
3) Emotional tone
4) Professional tone

Return each version separated by a blank line.
No preamble.

Original post:
{original_post}
"""
    response = llm.invoke(prompt)
    return response.content

def improve_hook(post):
    prompt = f"""
Rewrite only the opening of this LinkedIn post (first 2–3 lines) to make it more engaging and attention-grabbing.
Keep the rest of the post unchanged.
No preamble.

Post:
{post}
"""
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
If Language is Hinglish then it means it is a mix of Hindi and English. 
The script for the generated post should always be English.
'''

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\nExample {i+1}:\n\n{post_text}'
        if i == 1:
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))
