import json

TOP_N_NEWS = 10


def generate_html(content, tag, replacement):
    return content.replace("<!--" + tag + "-->", replacement)


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()
        return file_content


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def build_paper(title, author, conference, year, pdf, tool, video, ppt, award):
    paper_content = "          <li>\n \
           <h4 class=""><strong>TITLE</strong>\n"
    paper_content = paper_content.replace("TITLE", title)
    if pdf != None:
        paper_content = paper_content + \
            "            <a href=\"PDF\"> <img src=\"images/pdf.png\" width=\"25\" height=\"25\"></a>\n".replace(
                "PDF", pdf)
    if tool != None:
        paper_content = paper_content + \
            "            <a href=\"TOOL\"> <img src=\"images/github.png\" width=\"25\" height=\"25\"></a>\n".replace(
                "TOOL", tool)
    if video != None:
        paper_content = paper_content + \
            "            <a href=\"VIDEO\"> <img src=\"images/video.png\" width=\"25\" height=\"25\"></a>\n".replace(
                "VIDEO", video)
    if ppt != None:
        paper_content = paper_content + \
            "            <a href=\"PPT\"> <img src=\"images/ppt.png\" width=\"25\" height=\"25\"></a>\n".replace(
                "PPT", ppt)
    paper_template = paper_content + "            </h4>\n\
            AUTHOR.\n\
          <p class=\"\">CONF, YEAR.</p>\n\
          </li>\n"
    paper_content = paper_template.replace("AUTHOR", author).replace(
        "CONF", conference).replace("YEAR", year)
    if award != None:
        paper_content = paper_content + \
            "            <p><span style=\"color:red\">"+award+"</span></p>"
    return paper_content


def build_paper_list(filter=None):
    with open('data/paper.json') as json_file:
        papers = json.load(json_file)
    paper_list_content = "<h3><strong>Selected Research Papers</strong></h3>\n\
        <ul class=\"\">\n"
    for paper in papers:
        if filter != None and not filter(paper):
            continue
        paper_content = build_paper(paper["title"], ", ".join(paper["authors"]),
                                    paper["conference"], str(paper["year"]),
                                    paper["pdf"], paper["tool"], paper["video"], paper["ppt"], paper["award"])
        paper_list_content = paper_list_content + paper_content
    paper_list_content = paper_list_content + "        </ul>"
    return paper_list_content


def build_student(name, image: str, degree, grade, direction, placement):
    student_content = "          <div class=\"col-md-2 col-sm-4 custom-column\">\n \
            <div class=\"thumbnail\">\n \
              <img class=\"img-circle student-img\" alt=\"...\"\n \
                src=\"IMG\">\n \
              <p class=\"header\">NAME</p>\n \
              <p class=\"b\">DEGREE GRADE</p>\n"
    image = f"./images/avatars/{image or 'cat.webp'}"

    student_content = student_content.replace("NAME", name).replace("IMG", image)\
                                     .replace("DEGREE", degree)
    if grade != "None":
        student_content = student_content.replace("GRADE", grade)
    else:
        student_content = student_content.replace(" GRADE", "")
    if direction != None:
        student_content = student_content + \
            "              <p class=\"b\">" + direction + "</p>\n"
    if placement != None:
        student_content = student_content + \
            "              <p class=\"b\">" + placement + "</p>\n"
    student_content += "            </div>\n \
          </div>\n"
    return student_content


def build_student_list(filter=None):
    with open('data/student.json') as json_file:
        students = json.load(json_file)
    student_list_content = "        <div class=\"row custom-row\">\n"
    # current students
    current_students = sorted(students["students"], key=lambda x: (
        x["degree"] == "Master", x["grade"]), reverse=False)
    for student in current_students:
        if filter != None and not filter(student):
            continue
        student_content = build_student(
            name=student["name"],
            image=student["image"],
            degree=student["degree"],
            grade=str(student["grade"]),
            direction=student["direction"],
            placement=None,
        )
        student_list_content = student_list_content + student_content
    student_list_content = student_list_content + "        </div>\n"
    return student_list_content


# def build_former_student_list(filter=None):
#     with open('data/student.json') as json_file:
#         students = json.load(json_file)
#     # Former students
#     student_list_content = ""
#     student_list_content = student_list_content + "        <br>\n \
#         <h3><strong>Former Students</strong></h3>\n \
#         <div class=\"row custom-row\">\n"
#     former_students = students["former_students"]
#     for student in former_students:
#         student_content = build_student(student["name"], student["image"], student["degree"],
#                                         str(student["grade"]), None, student["placement"],)
#         student_list_content = student_list_content + student_content
#     student_list_content = student_list_content + "        </div>\n"

#     return student_list_content

def build_former_student_list(filter=None):
    with open('data/student.json') as json_file:
        students = json.load(json_file)
    # Former students
    student_list_content = ""
    student_list_content = student_list_content + "        <br>\n \
        <h3><strong>Former Students</strong></h3>\n \
        <div class=\"row custom-row\">\n"
    former_students = students["former_students"]
    for student in former_students:
        if filter != None and not filter(student):
            continue
        student_content = build_student(student["name"], student["image"], student["degree"],
                                        str(student["grade"]), None, student["placement"],)
        student_list_content = student_list_content + student_content
    student_list_content = student_list_content + "        </div>\n"

    return student_list_content


# Build news


def build_news_list(filter=None):
    with open('data/news.json') as json_file:
        news_list = json.load(json_file)
    news_content_template = "              <li><strong>TIME</strong> NEWS_CONTENT</li>\n"
    news_list_content = "            <ul>"
    count = 0
    for news in news_list:
        if filter != None and not filter(news):
            continue
        count += 1
        if count > 10:
            break
        news_content = news_content_template.replace(
            "TIME", news["date"]).replace("NEWS_CONTENT", news["event"])
        news_list_content += news_content
    news_list_content += "            </ul>"
    return news_list_content


def build_index():
    def is_selected_paper_filter(paper):
        return paper["is_selected"] == True

    index_template_content = read_file("template/index.html")
    paper_content = build_paper_list(is_selected_paper_filter)
    content = generate_html(index_template_content,
                            "PAPER-LIST", paper_content)
    # student_content = build_student_list()
    # student_content += build_former_student_list()
    
    # content = generate_html(content, "STUDENT-LIST", student_content)
    ssc_news = build_news_list()
    content = generate_html(content, "NEWS-LIST", ssc_news)
    write_file("index.html", content)
    print("Build index page done!")


# Build ssc webpage
def build_ssc_page():
    def ssc_master_filter(student):
        return student["group"] == "SE" and student["degree"] == "Master"

    def ssc_phd_filter(student):
        return student["group"] == "SE" and student["degree"] == "Ph.D."

    def ssc_paper_filter(paper):
        return paper["field"] == "AI4SE"

    def ssc_news_filter(news):
        return news["field"] == "SE"
    
    def ssc_former_student_filter(student):
        return student["group"] == "SE"

    ssc_content = read_file("template/ssc.html")
    ssc_phd_content = build_student_list(ssc_phd_filter)
    ssc_content = generate_html(
        ssc_content, "PHD_STUDENT_AI4SE", ssc_phd_content)
    ssc_master_content = build_student_list(ssc_master_filter)
    ssc_content = generate_html(
        ssc_content, "MASTER_STUDENT_AI4SE", ssc_master_content)
    ssc_former_student_content = build_former_student_list(ssc_former_student_filter)
    ssc_content = generate_html(
        ssc_content, "FORMER_STUDENT_AI4SE", ssc_former_student_content)
    
    paper_content = build_paper_list(ssc_paper_filter)
    ssc_content = generate_html(ssc_content, "PAPER-LIST", paper_content)
    ssc_news = build_news_list(ssc_news_filter)
    ssc_content = generate_html(ssc_content, "NEWS-LIST", ssc_news)

    write_file("ssc.html", ssc_content)
    print("Build SSC page done!")


build_index()
build_ssc_page()
