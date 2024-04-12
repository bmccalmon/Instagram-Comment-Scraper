#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys
import csv

def repair_likes(likes):
    fixed_likes = list()
    for i in range(len(likes)):
        if i >= len(likes) - 1:
            break
        if likes[i].text != "Reply" and likes[i].text != "See translation":
            fixed_likes.append(likes[i].text)
        else:
            if likes[i+1].text == "Reply":
                fixed_likes.append("0 likes")
    return fixed_likes

def extract_comments(post_file_path):
    with open(post_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    contents = soup.find_all('span', class_="_ap3a _aaco _aacu _aacx _aad7 _aade")
    likes = soup.find_all('span', class_="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye x1fhwpqd x1s688f x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj")

    likes = repair_likes(likes)

    paired_data = []
    for content, like in zip(contents, likes):
        paired_data.append([content.text, like])

    return paired_data

def export_to_csv(extracted_comments):
    header = ["Comment", "Likes"]
    data = extracted_comments
    filename = 'comments_output.csv'
    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerow(header) # 4. write the header
        csvwriter.writerows(data) # 5. write the rest of the data

def main():
    extracted_comments = extract_comments(sys.argv[1])
    print("NUMBER OF COMMENTS: " + str(len(extracted_comments)))
    export_to_csv(extracted_comments)
    for comment in extracted_comments:
        print("    • " + comment[0])
        #print("          LIKES: " + comment[1])
        print("            " + comment[1])
        pass

if __name__ == "__main__":
    main()
